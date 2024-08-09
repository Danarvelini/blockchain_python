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

### API Public (Disabled for now)

I made this API publicly available using this host: <https://blockchain-simulation-python.onrender.com> 

If you would like to test that public API, please update the host as specified above.

## Example

Here's some examples of how to use the API:

### Get the current chain

```bash
curl --request GET \
  --url https://blockchain-simulation-python.onrender.com/chain \
  --header 'User-Agent: insomnia/9.3.2'
```

### Add a new transaction

```bash
curl --request POST \
  --url https://blockchain-simulation-python.onrender.com/transactions/new \
  --header 'Content-Type: application/json' \
  --header 'User-Agent: insomnia/9.3.2' \
  --data '{
 "origin": "Anyone",
 "destination": "Someone",
 "amount": 75422
}'
```

### Register a new node

```bash
curl --request POST \
  --url https://blockchain-simulation-python.onrender.com/nodes/register \
  --header 'Content-Type: application/json' \
  --header 'User-Agent: insomnia/9.3.2' \
  --data '{
 "nodes": "127.0.0.1"
}'
```

### Mine a new block

```bash
curl --request GET \
  --url https://blockchain-simulation-python.onrender.com/mine \
  --header 'User-Agent: insomnia/9.3.2'
```
