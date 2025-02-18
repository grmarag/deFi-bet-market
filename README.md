# DeFi-AI-agent

**Decentralized Prediction Market & AI-Enhanced Decision Engine on Ethereum**

DeFi-AI-agent is an innovative platform that fuses decentralized finance (DeFi) with cutting-edge AI insights to power a trustless prediction market. Built on Ethereum, it enables users to bet on binary outcomes while leveraging advanced AI-driven analytics for smarter decision making.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Docker Deployment](#docker-deployment)
- [Testing](#testing)
- [Technologies](#technologies)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

DeFi-AI-agent brings together the transparency of blockchain with the analytical power of AI to create a next-generation prediction market. Users can place bets on binary outcomes (yes/no) regarding various events, and the system aggregates these bets to form market insights. Additionally, integrated AI components help analyze trends and potentially enhance prediction accuracy.

Whether you're a blockchain enthusiast or an AI aficionado, DeFi-AI-agent provides a robust example of modern decentralized application development using state‑of‑the‑art technologies.

---

## Features

- **Blockchain-Powered:** Utilizes Ethereum smart contracts for secure, immutable transactions.
- **Decentralized Prediction Market:** Users bet on outcomes, and the market aggregates collective wisdom.
- **AI-Enhanced Insights:** Integrated AI components offer additional analysis to support decision making.
- **Smart Contract Integration:** Solidity contracts ensure trustless and transparent execution.
- **RESTful API:** A FastAPI-based API facilitates seamless interaction with the prediction market.
- **Modern Development Stack:** Built with Python, Web3.py, and managed using Poetry.
- **Containerized Deployment:** Dockerfile provided for easy containerization and deployment.
- **Comprehensive Testing:** Automated tests with pytest ensure reliability and robustness.

---

## Getting Started

### Prerequisites

- **Python 3.9+**
- **Poetry** for dependency management ([Installation Guide](https://python-poetry.org/docs/))
- **Ethereum Node Provider:** Use a local network (like Ganache) or a public testnet/mainnet.
- **Docker** (optional, for containerized deployment)

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/defi-ai-agent.git
   cd defi-ai-agent
   ```

2. **Install Dependencies**

   Use Poetry to install the required packages:

   ```bash
   poetry install
   ```

3. **Configure Environment**

   Set your Ethereum provider URL (if different from the default):

   ```bash
   export ETH_PROVIDER_URL="http://127.0.0.1:8545"
   ```

---

## Usage

### Running the API Server

Start the FastAPI server using Uvicorn:

```bash
poetry run uvicorn src.api:app --reload
```

Access the interactive API documentation by navigating to [http://localhost:8000/docs](http://localhost:8000/docs).

### Deploying the Smart Contract

Deploy the Prediction Market smart contract by running the deployment script:

```bash
poetry run python scripts/deploy.py
```

Follow the prompts to input your deployer address, private key, and market question.

### Interacting with the Market

Once deployed, you can interact with the following endpoints:

- **/deploy**: Deploy a new prediction market.
- **/bet**: Place bets on the market.
- **/close**: Close betting on the market.
- **/resolve**: Resolve the market outcome.
- **/withdraw**: Withdraw winnings post-resolution.
- **/market**: Retrieve current market details.

---

## Docker Deployment

To run DeFi-AI-agent in a containerized environment, follow these steps:

1. **Build the Docker Image**

   ```bash
   docker build -t defi-ai-agent .
   ```

2. **Run the Docker Container**

   ```bash
   docker run -p 8000:8000 defi-ai-agent
   ```

Your API will be available at [http://localhost:8000](http://localhost:8000).

---

## Testing

Ensure everything is working correctly by running the automated tests:

```bash
poetry run pytest
```

The tests simulate blockchain interactions using EthereumTesterProvider, verifying that both the smart contract and the API function as expected.

---

## Technologies

- **Blockchain:** Ethereum, Solidity
- **Backend:** Python, FastAPI, Uvicorn
- **Smart Contract Interaction:** Web3.py, py-solc-x
- **AI Components:** (Integrate your preferred AI/ML libraries as needed)
- **Containerization:** Docker
- **Testing:** Pytest, EthereumTesterProvider
- **Dependency Management:** Poetry

---

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your enhancements. For major changes, open an issue first to discuss your proposed modifications.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

Happy coding with **DeFi-AI-agent** – where decentralized finance meets intelligent decision-making!
