# DeFi-Bet-Market

**Decentralized Prediction Market & AI-Enhanced Decision Engine on Ethereum**

DeFi-Bet-Market is an innovative platform that fuses decentralized finance (DeFi) with advanced AI analytics to power a trustless prediction market. Built on Ethereum, it allows users to bet on binary outcomes while leveraging AI-driven insights to inform smarter decision-making.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture & Project Structure](#architecture--project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Running the API Server](#running-the-api-server)
  - [Deploying the Smart Contract](#deploying-the-smart-contract)
  - [Interacting with the Market](#interacting-with-the-market)
- [Docker Deployment](#docker-deployment)
- [Testing](#testing)
- [Contributing](#contributing)
- [Roadmap](#roadmap)
- [License](#license)

---

## Overview

DeFi-Bet-Market integrates blockchain transparency with AI-powered analytics to create a next-generation decentralized prediction market. Users can place bets on yes/no outcomes regarding various events, while the system aggregates bets and uses AI components to enhance prediction accuracy. Whether you are a blockchain enthusiast or an AI aficionado, this project demonstrates modern decentralized application development using state‑of‑the‑art technologies.

---

## Features

- **Blockchain-Powered:** Secure and immutable transactions via Ethereum smart contracts.
- **Decentralized Prediction Market:** Bet on binary outcomes with aggregated market insights.
- **AI-Enhanced Decision Engine:** Leverage integrated AI for additional analysis and trend insights.
- **Smart Contract Integration:** Solidity contracts ensure trustless and transparent execution.
- **RESTful API:** FastAPI-based backend for seamless interaction.
- **Modern Development Stack:** Developed with Python, Web3.py, and managed via Poetry.
- **Containerized Deployment:** Docker configuration for simplified deployment.
- **Automated Testing:** Comprehensive tests using pytest and EthereumTesterProvider.

---

## Architecture & Project Structure

The project is structured to clearly separate concerns between the smart contracts, backend API, frontend interface, and testing framework.

```
deFi-bet-market/
├── pyproject.toml               # Poetry configuration and dependency management
├── README.md                    # Project documentation (this file)
├── Dockerfile                   # Containerization instructions
├── contracts/
│   └── PredictionMarket.sol     # Solidity smart contract for prediction markets
├── frontend/
│   └── index.html               # Web-based interface for interacting with the market
├── scripts/
│   └── deploy.py                # CLI script to deploy smart contracts
├── src/
│   ├── __init__.py
│   ├── api.py                   # FastAPI server exposing REST endpoints
│   ├── config.py                # Configuration variables (e.g., Ethereum provider URL)
│   └── market.py                # Python wrapper for smart contract interaction
└── tests/
    └── test_market.py           # Automated tests for contract functionality
```

---

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.12** (or a compatible version between 3.12 and 4.0)
- **Poetry** for dependency management ([Installation Guide](https://python-poetry.org/docs/))
- **Ethereum Node Provider:**  
  - **Ganache:** A personal blockchain for Ethereum development. Ganache is highly recommended for local testing and development.  
  - Alternatively, use a local blockchain simulator (like Ganache CLI or Ganache UI) or connect to a public testnet/mainnet.
- **Docker** (optional, for containerized deployment)

---

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/defi-bet-market.git
   cd defi-bet-market
   ```

2. **Install Dependencies:**

   Use Poetry to install the required packages:

   ```bash
   poetry install
   eval $(poetry env activate)
   ```

---

## Configuration

The project uses environment variables to configure the Ethereum provider. By default, it connects to a local node:

```bash
export ETH_PROVIDER_URL="http://127.0.0.1:7545"
```

If you're using **Ganache** (either via the CLI or UI), ensure it is running on the above URL. You can also update the URL to match your Ganache configuration if it differs.

---

## Usage

### Running the API Server

Start the FastAPI server using Uvicorn:

```bash
poetry run uvicorn src.api:app --reload
```

Access the interactive API documentation at [http://localhost:8000/docs](http://localhost:8000/docs).

### Deploying the Smart Contract

Deploy the Prediction Market smart contract by running the deployment script:

```bash
poetry run python scripts/deploy.py
```

When prompted, provide:
- **Deployer Address**
- **Deployer Private Key**
- **Market Question**

**Note:** If you are developing locally, running Ganache will simulate a blockchain environment. Ensure Ganache is active on your specified ETH_PROVIDER_URL before deploying.

### Interacting with the Market

Once deployed, you can interact with the market through the following endpoints:

- **POST /api/deploy:** Deploy a new prediction market.
- **POST /api/bet:** Place a bet on the market (provide vote and wager details).
- **POST /api/close:** Close the market for further bets.
- **POST /api/resolve:** Resolve the market outcome.
- **POST /api/withdraw:** Withdraw winnings after market resolution.
- **GET /api/market/{market_address}:** Retrieve details for a specific market.
- **GET /api/markets:** List all deployed markets.

The frontend interface available in `frontend/index.html` also allows you to deploy markets, place bets, and manage market actions with a user-friendly UI.

---

## Docker Deployment

To run DeFi-Bet-Market in a containerized environment, follow these steps:

1. **Build the Docker Image:**

   ```bash
   docker build -t defi-bet-market .
   ```

2. **Run the Docker Container:**

If your Ganache RPC server is running on your host machine at http://127.0.0.1:7545, you can run the container and pass the updated ETH_PROVIDER_URL as follows:

   ```bash
   docker run -e ETH_PROVIDER_URL="http://host.docker.internal:7545" -p 8000:8000 defi-bet-market
   ```

Your API server will be accessible at [http://localhost:8000](http://localhost:8000).

---

## Testing

Automated tests are written using pytest and the EthereumTesterProvider to simulate blockchain interactions. To run the tests, execute:

```bash
poetry run pytest
```

These tests verify that the smart contract functions correctly and that the API endpoints behave as expected. For local development, you can also use Ganache to manually test interactions before running the automated suite.

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and ensure all tests pass.
4. Submit a pull request with a clear description of your changes.

For major modifications, consider opening an issue first to discuss your proposed changes.

---

## Roadmap

- **Enhanced AI Analytics:** Integrate additional AI/ML libraries for deeper market insights.
- **User Authentication:** Add secure user management and authentication.
- **Improved UI/UX:** Refine the frontend interface for a smoother user experience.
- **Extended Testing:** Increase test coverage for edge cases and contract security.

Feel free to suggest additional features or improvements through issues or discussions.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

Happy coding with **DeFi-Bet-Market** – where decentralized finance meets intelligent decision-making!