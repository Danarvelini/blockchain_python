# Blockchain with Python

Repository created with the intention to simulate a blockchain with Transactions, Blocks, Proof of Work, and a consensus mechanism.

## Requirements

- Python 3.7+
- Flask
- Requests
- Hashlib
- JSON
- UUID
- Time
- Urllib

## Features

- Create a new blockchain node with a unique ID
- Register other nodes to the network
- Resolve conflicts with other nodes
- Mine new blocks
- Add new transactions
- Validate the chain
- View the chain

## Usage

1. Run the application: `python app.py`
2. Access the API endpoints:
    - `/chain`: Get the current chain
    - `/transactions/new`: Add a new transaction
    - `/mine`: Mine a new block
    - `/nodes/register`: Register a new node
    - `/nodes/resolve`: Resolve conflicts with other nodes

### API Public

I made this API publicly available using this host: <https://blockchain-simulation-python.onrender.com>

If you would like to test that public API, please update the host as specified above.

## Example

Here's some examples of how to use the API:

### Register a new node

```bash
curl -X POST -H "Content-Type: application/json" -d '{"nodes": ["http://localhost:5001"]}' <http://localhost:5000/nodes/register>
```

### Add a new transaction

```bash
curl -X POST -H "Content-Type: application/json" -d '{"origin": "Alice", "destination": "Bob", "amount": 10}' <http://localhost:5000/transactions/new>
```

### Mine a new block

```bash
curl -X GET <http://localhost:5000/mine>
```

### Get the current chain

```bash
curl -X GET <http://localhost:5000/chain>
```
