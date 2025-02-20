from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import os
from pydantic import BaseModel
from src.market import PredictionMarket
from src.config import ETH_PROVIDER_URL, CONTRACTS_DIR
from web3 import Web3

app = FastAPI()

frontend_path = Path(__file__).resolve().parent.parent / "frontend"
if not frontend_path.exists():
    raise RuntimeError(f"Directory '{frontend_path}' does not exist")

# Mount static files
app.mount("/static", StaticFiles(directory=str(frontend_path), html=True), name="static")

# Serve the index.html on the root path.
@app.get("/")
def read_index():
    return FileResponse(frontend_path / "index.html")

# Create an API router with prefix /api.
api_router = APIRouter()

w3 = Web3(Web3.HTTPProvider(ETH_PROVIDER_URL))
if not w3.is_connected():
    raise Exception("Web3 is not connected. Check your ETH_PROVIDER_URL.")

# Global dictionary to store deployed markets.
markets = {}

# Helper function to convert non-JSON-serializable types
def convert_bytes(obj):
    if hasattr(obj, "hex"):
        try:
            return obj.hex()
        except Exception:
            pass
    if isinstance(obj, (bytes, bytearray)):
        return obj.hex()
    # If the object behaves like a dictionary.
    elif isinstance(obj, dict) or hasattr(obj, "items"):
        return {k: convert_bytes(v) for k, v in dict(obj).items()}
    # If it's a list or tuple.
    elif isinstance(obj, (list, tuple)):
        return [convert_bytes(item) for item in obj]
    else:
        return obj

# Request models.
class DeployRequest(BaseModel):
    question: str
    deployer_address: str
    private_key: str

class BetRequest(BaseModel):
    market_address: str
    vote: bool
    amount_wei: int
    voter_address: str
    private_key: str

class ActionRequest(BaseModel):
    market_address: str
    address: str
    private_key: str

class ResolveRequest(BaseModel):
    market_address: str
    outcome: bool
    owner_address: str
    private_key: str

@api_router.post("/deploy")
def deploy_market(request: DeployRequest):
    contract_path = os.path.join(CONTRACTS_DIR, "PredictionMarket.sol")
    try:
        abi, bytecode = PredictionMarket.compile_contract(contract_path)
        market = PredictionMarket(w3, abi=abi, bytecode=bytecode)
        contract_address = market.deploy(
            question=request.question,
            deployer_address=request.deployer_address,
            private_key=request.private_key
        )
        markets[contract_address] = market
        return {"contract_address": contract_address, "question": request.question}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@api_router.post("/bet")
def place_bet(request: BetRequest):
    market = markets.get(request.market_address)
    if not market or not market.contract:
        raise HTTPException(status_code=400, detail="Market not deployed or not found")
    try:
        receipt = market.bet(
            voter_address=request.voter_address,
            private_key=request.private_key,
            vote=request.vote,
            amount_wei=request.amount_wei
        )
        serialized_receipt = convert_bytes(receipt)
        return {"transaction_receipt": serialized_receipt}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@api_router.post("/close")
def close_bets(request: ActionRequest):
    market = markets.get(request.market_address)
    if not market or not market.contract:
        raise HTTPException(status_code=400, detail="Market not deployed or not found")
    try:
        receipt = market.close_bets(
            owner_address=request.address,
            private_key=request.private_key
        )
        serialized_receipt = convert_bytes(receipt)
        return {"transaction_receipt": serialized_receipt}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@api_router.post("/resolve")
def resolve_market(request: ResolveRequest):
    market = markets.get(request.market_address)
    if not market or not market.contract:
        raise HTTPException(status_code=400, detail="Market not deployed or not found")
    try:
        receipt = market.resolve(
            owner_address=request.owner_address,
            private_key=request.private_key,
            outcome=request.outcome
        )
        serialized_receipt = convert_bytes(receipt)
        return {"transaction_receipt": serialized_receipt}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@api_router.post("/withdraw")
def withdraw(request: ActionRequest):
    market = markets.get(request.market_address)
    if not market or not market.contract:
        raise HTTPException(status_code=400, detail="Market not deployed or not found")
    try:
        receipt = market.withdraw(
            user_address=request.address,
            private_key=request.private_key
        )
        serialized_receipt = convert_bytes(receipt)
        return {"transaction_receipt": serialized_receipt}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@api_router.get("/market/{market_address}")
def get_market_details(market_address: str):
    market = markets.get(market_address)
    if not market or not market.contract:
        raise HTTPException(status_code=400, detail="Market not deployed or not found")
    try:
        details = market.get_details()
        return details
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@api_router.get("/markets")
def list_markets():
    market_list = []
    for address, market in markets.items():
        try:
            details = market.get_details()
            market_list.append({
                "contract_address": address,
                "question": details.get("question"),
                "betsOpen": details.get("betsOpen"),
                "resolved": details.get("resolved"),
                "totalYes": details.get("totalYes"),
                "totalNo": details.get("totalNo")
            })
        except Exception:
            pass
    return market_list

# Include all API routes under the /api prefix.
app.include_router(api_router, prefix="/api")