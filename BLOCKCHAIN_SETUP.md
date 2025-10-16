# 🔗 Blockchain Ticket Sales - Base Sepolia Integration

## Overview

Your MCP Ticket Server now accepts **real on-chain payments** on the **Base Sepolia testnet**! Users can purchase event tickets by sending ETH directly to the payment wallet address. The system automatically verifies transactions and issues tickets.

---

## 🌐 Network Details

-   **Network**: Base Sepolia (Testnet)
-   **Chain ID**: 84532
-   **RPC URL**: https://sepolia.base.org
-   **Block Explorer**: https://sepolia.basescan.org
-   **Faucet**: https://www.coinbase.com/faucets/base-ethereum-goerli-faucet

---

## 🏗️ Architecture

```
┌─────────────────────┐
│   User's Wallet     │
│  (MetaMask, etc.)   │
└──────────┬──────────┘
           │ Send ETH
           ▼
┌─────────────────────┐
│  Payment Address    │ (Your wallet)
│  Base Sepolia       │
└──────────┬──────────┘
           │ Blockchain monitors transaction
           ▼
┌─────────────────────┐
│  MCP Ticket Server  │
│  • Verifies payment │
│  • Issues ticket    │
│  • Generates QR code│
└─────────────────────┘
```

---

## 🚀 Quick Start

### 1. Get Your Payment Wallet Address

When you start the MCP server, it will display:

```bash
cd /Users/kevinjones/google/mcp-ticket-server
npm run dev
```

Output:

```
🎫 MCP Ticket Sales Server
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📍 Port: 3000
⛓️  Blockchain: Base Sepolia (Chain ID: 84532)
💳 Payment Method: On-chain ETH transactions
📬 Payment Address: 0xDA8AEbcca35E679Bb07F0c76D1Dd32cA518166CA
✅ Server Ready!
```

**Important**: Save this payment address! You'll need Base Sepolia ETH in this wallet.

### 2. Get Base Sepolia Testnet ETH

Visit the Coinbase Faucet:
👉 https://www.coinbase.com/faucets/base-ethereum-goerli-faucet

-   Connect your wallet
-   Request testnet ETH
-   Send some to your payment address (from step 1)

### 3. Add Base Sepolia to MetaMask

**Network Details:**

-   Network Name: `Base Sepolia`
-   RPC URL: `https://sepolia.base.org`
-   Chain ID: `84532`
-   Currency Symbol: `ETH`
-   Block Explorer: `https://sepolia.basescan.org`

---

## 💰 How Payment Works

### Step 1: User Initiates Purchase

```bash
# Via Ticket Agent
curl -X POST http://localhost:8002/execute-tool \
  -H "Content-Type: application/json" \
  -d '{
    "tool_name": "purchase_tickets",
    "parameters": {
      "event_id": "event-3",
      "quantity": 2,
      "customer_email": "user@example.com",
      "customer_name": "John Doe"
    }
  }'
```

### Step 2: System Returns Payment Instructions

```json
{
    "success": false,
    "requiresPayment": true,
    "paymentIntent": {
        "id": "35797296-7d20-499e-a485-6fd7733e73c9",
        "amount": 150,
        "blockchain": {
            "network": "Base Sepolia",
            "chainId": 84532,
            "paymentAddress": "0xDA8AEbcca35E679Bb07F0c76D1Dd32cA518166CA",
            "amountETH": "0.060000",
            "amountUSD": 150
        },
        "expiresAt": "2025-10-16T18:42:31.554Z"
    }
}
```

### Step 3: User Sends ETH

Using MetaMask, Coinbase Wallet, or any Web3 wallet:

1. Switch to **Base Sepolia** network
2. Send **0.060000 ETH** to `0xDA8AEbcca35E679Bb07F0c76D1Dd32cA518166CA`
3. Wait for transaction confirmation (~2-5 seconds)

### Step 4: Verify Payment

```bash
curl -X POST http://localhost:8002/execute-tool \
  -H "Content-Type: application/json" \
  -d '{
    "tool_name": "check_payment_status",
    "parameters": {
      "payment_intent_id": "35797296-7d20-499e-a485-6fd7733e73c9"
    }
  }'
```

Once payment is confirmed, the ticket status changes to `"paid"` and a QR code is generated!

---

## 🛠️ Advanced: Manual Transaction Verification

If a user sends the transaction manually (not through the system), you can verify it:

```bash
curl -X POST http://localhost:3000/mcp/tool/verify_transaction \
  -H "Content-Type: application/json" \
  -d '{
    "paymentIntentId": "35797296-7d20-499e-a485-6fd7733e73c9",
    "transactionHash": "0x..."
  }'
```

---

## 🔐 Security Best Practices

### For Testing (Current Setup)

✅ Using temporary wallet generated on startup
✅ Testnet only (no real money)
✅ Easy to reset and restart

### For Production (Future)

**DO:**

-   ✅ Store private key in secure environment variable
-   ✅ Use hardware wallet or HSM
-   ✅ Implement multi-sig for large transactions
-   ✅ Monitor wallet balance and alerts
-   ✅ Use Chainlink price feeds for accurate ETH/USD conversion

**DON'T:**

-   ❌ Hardcode private keys
-   ❌ Commit `.env` files to git
-   ❌ Share private keys
-   ❌ Use testnet wallets on mainnet

---

## 📊 Price Conversion

Currently using a **fixed ETH price** of $2,500 USD.

For production, integrate with:

-   **Chainlink Price Feeds** (recommended)
-   CoinGecko API
-   Binance API
-   Custom oracle

---

## 🧪 Testing the Full Flow

### Test 1: Purchase Tickets

```bash
# 1. Purchase tickets (get payment address)
curl -X POST http://localhost:8002/execute-tool \
  -H "Content-Type: application/json" \
  -d '{
    "tool_name": "purchase_tickets",
    "parameters": {
      "event_id": "event-1",
      "quantity": 1,
      "customer_email": "test@example.com",
      "customer_name": "Test User"
    }
  }'

# 2. Note the payment address and amount from response

# 3. Send ETH using MetaMask to the payment address

# 4. Check payment status
curl -X POST http://localhost:8002/execute-tool \
  -H "Content-Type: application/json" \
  -d '{
    "tool_name": "check_payment_status",
    "parameters": {
      "payment_intent_id": "YOUR_PAYMENT_INTENT_ID"
    }
  }'

# 5. Get your ticket!
curl -X POST http://localhost:8002/execute-tool \
  -H "Content-Type: application/json" \
  -d '{
    "tool_name": "get_my_tickets",
    "parameters": {}
  }'
```

### Test 2: List Available Events

```bash
curl -X POST http://localhost:8002/execute-tool \
  -H "Content-Type: application/json" \
  -d '{
    "tool_name": "list_events",
    "parameters": {}
  }'
```

---

## 🎯 Available Events

| Event                      | Venue                 | Date          | Price (USD) | Price (ETH) |
| -------------------------- | --------------------- | ------------- | ----------- | ----------- |
| Summer Music Festival 2025 | Hollywood Bowl        | July 15, 2025 | $150        | 0.06 ETH    |
| Tech Conference 2025       | Madison Square Garden | Sept 20, 2025 | $299        | 0.1196 ETH  |
| Rock Legends Concert       | The Fillmore          | June 10, 2025 | $75         | 0.03 ETH    |
| Broadway Musical Night     | Madison Square Garden | Aug 5, 2025   | $120        | 0.048 ETH   |

---

## 🔍 Troubleshooting

### Problem: "Cannot connect to MCP server"

**Solution**: Make sure the MCP server is running on port 3000

```bash
cd /Users/kevinjones/google/mcp-ticket-server
npm run dev
```

### Problem: "Payment not detected"

**Solutions**:

1. Verify you sent to the **correct address**
2. Check you're on **Base Sepolia network** (Chain ID: 84532)
3. Confirm transaction on block explorer: https://sepolia.basescan.org
4. Wait for block confirmation (~2-5 seconds)

### Problem: "Insufficient funds"

**Solution**: Get more Base Sepolia ETH from faucet
👉 https://www.coinbase.com/faucets/base-ethereum-goerli-faucet

### Problem: "Transaction reverted"

**Solution**: Ensure you're sending the **exact amount** of ETH specified (±1% tolerance)

---

## 📚 API Reference

### Purchase Tickets

**POST** `/mcp/tool/purchase_tickets`

Request:

```json
{
    "eventId": "event-1",
    "quantity": 2,
    "customerEmail": "user@example.com",
    "customerName": "John Doe"
}
```

Response:

```json
{
    "requiresPayment": true,
    "paymentIntent": {
        "blockchain": {
            "paymentAddress": "0x...",
            "amountETH": "0.060000",
            "network": "Base Sepolia",
            "chainId": 84532
        }
    }
}
```

### Check Payment Status

**POST** `/mcp/tool/check_payment_status`

Request:

```json
{
    "paymentIntentId": "uuid-here"
}
```

### Verify Transaction

**POST** `/mcp/tool/verify_transaction`

Request:

```json
{
    "paymentIntentId": "uuid-here",
    "transactionHash": "0x..."
}
```

---

## 🎉 What's Next?

Your blockchain ticket system is ready! Users can:

1. ✅ Browse events via the web interface (http://localhost:8080)
2. ✅ Purchase tickets with real on-chain ETH transactions
3. ✅ Get instant confirmation when payment is detected
4. ✅ Receive QR code tickets automatically

### Future Enhancements:

-   🔮 NFT tickets (ERC-721 tokens)
-   🎟️ Ticket transfers and resale marketplace
-   💎 Dynamic pricing based on demand
-   🏆 Loyalty rewards and discounts
-   📱 Mobile wallet integration
-   🔔 Webhook notifications for payments

---

**Need help?** Check the main README.md or TROUBLESHOOTING.md

**Ready to go live?**

1. Switch to Base mainnet
2. Update RPC endpoint
3. Configure production wallet
4. Integrate Chainlink price feeds
5. Add comprehensive error handling
6. Set up monitoring and alerts

🚀 **Happy ticket selling!**
