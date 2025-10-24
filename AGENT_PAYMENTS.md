# 🤖 Agent-Initiated Blockchain Payments

## Overview

Your Ticket Agent can now **send ETH payments** on the Base Sepolia blockchain! This means the agent can autonomously pay for tickets, tip users, or transfer funds on behalf of users.

---

## 🎯 Key Features

### 1. **Agent Wallet**
- Dedicated wallet for the agent
- Automatically generated on startup
- Can send and receive ETH on Base Sepolia

### 2. **Payment Sending**
- Agent can initiate on-chain transactions
- Automatic balance checking
- Gas estimation
- Transaction confirmation

### 3. **Balance Management**
- Check wallet balance anytime
- Track transaction history
- Monitor gas costs

---

## 💰 Agent Wallet Details

**Current Wallet Address**: `0xDA8AEbcca35E679Bb07F0c76D1Dd32cA518166CA`

**Private Key** (shown in server logs on startup):
```
🔑 Private Key: 0xb7deec21b6def4b82c2670a9904af025145b020ee66272569d21b0c0ebc21c7a
```

⚠️ **IMPORTANT**: This is a **testnet wallet** for Base Sepolia. Never use this on mainnet!

---

## 🧪 How to Fund the Agent Wallet

### Option 1: Coinbase Faucet

1. Visit: https://www.coinbase.com/faucets/base-ethereum-goerli-faucet
2. Enter the agent's address: `0xDA8AEbcca35E679Bb07F0c76D1Dd32cA518166CA`
3. Request testnet ETH
4. Wait ~30 seconds for confirmation

### Option 2: Manual Transfer

If you have Base Sepolia ETH in MetaMask:

1. Add Base Sepolia network to MetaMask
2. Send ETH to: `0xDA8AEbcca35E679Bb07F0c76D1Dd32cA518166CA`
3. Use any amount (0.1 ETH is good for testing)

---

## 🛠️ Available Tools

### 1. Check Agent Wallet Balance

**Via API:**
```bash
curl -X POST http://localhost:8002/execute-tool \
  -H "Content-Type: application/json" \
  -d '{
    "tool_name": "get_wallet_balance",
    "parameters": {}
  }'
```

**Response:**
```json
{
  "success": true,
  "address": "0xDA8AEbcca35E679Bb07F0c76D1Dd32cA518166CA",
  "balance": "0.5",
  "network": "Base Sepolia",
  "chainId": 84532,
  "message": "💰 Agent Wallet Balance\n\n📬 Address: 0xDA8...\n💎 Balance: 0.5 ETH\n..."
}
```

### 2. Send Payment from Agent

**Via API:**
```bash
curl -X POST http://localhost:8002/execute-tool \
  -H "Content-Type: application/json" \
  -d '{
    "tool_name": "send_payment",
    "parameters": {
      "to_address": "0x1234567890123456789012345678901234567890",
      "amount_eth": "0.01",
      "memo": "Payment for concert ticket"
    }
  }'
```

**Response:**
```json
{
  "success": true,
  "transactionHash": "0xabc123...",
  "amountETH": "0.01",
  "toAddress": "0x1234...",
  "explorerUrl": "https://sepolia.basescan.org/tx/0xabc123...",
  "message": "✅ Payment Sent Successfully!\n\n💸 Amount: 0.01 ETH\n..."
}
```

---

## 🎬 Use Cases

### Use Case 1: Agent Pays for User's Tickets

**Scenario**: User asks agent to buy tickets, agent pays on their behalf

```bash
# User: "Buy me 2 tickets to the Rock Legends Concert"

# Step 1: Agent checks available tickets
curl -X POST http://localhost:8002/execute-tool \
  -d '{"tool_name": "list_events", "parameters": {}}'

# Step 2: Agent calculates cost (2 tickets × $75 = $150 = 0.06 ETH)

# Step 3: Agent checks its balance
curl -X POST http://localhost:8002/execute-tool \
  -d '{"tool_name": "get_wallet_balance", "parameters": {}}'

# Step 4: Agent sends payment to venue's address
curl -X POST http://localhost:8002/execute-tool \
  -d '{
    "tool_name": "send_payment",
    "parameters": {
      "to_address": "0xVENUE_ADDRESS",
      "amount_eth": "0.06",
      "memo": "2 tickets to Rock Legends Concert"
    }
  }'

# Step 5: Tickets automatically issued!
```

### Use Case 2: Agent Tips a Service Provider

```bash
curl -X POST http://localhost:8002/execute-tool \
  -H "Content-Type: application/json" \
  -d '{
    "tool_name": "send_payment",
    "parameters": {
      "to_address": "0xSERVICE_PROVIDER_ADDRESS",
      "amount_eth": "0.001",
      "memo": "Tip for excellent service"
    }
  }'
```

### Use Case 3: Agent Refunds a User

```bash
curl -X POST http://localhost:8002/execute-tool \
  -H "Content-Type: application/json" \
  -d '{
    "tool_name": "send_payment",
    "parameters": {
      "to_address": "0xUSER_ADDRESS",
      "amount_eth": "0.06",
      "memo": "Refund for cancelled event"
    }
  }'
```

---

## 💬 Conversational Examples

### Example 1: Via Web Interface

**User**: "Check your wallet balance"

**Agent**: 
```
💰 Agent Wallet Balance

📬 Address: 0xDA8AEbcca35E679Bb07F0c76D1Dd32cA518166CA
💎 Balance: 0.5 ETH
🌐 Network: Base Sepolia
🔗 Chain ID: 84532

This wallet can send payments for ticket purchases!
```

### Example 2: Agent-Initiated Purchase

**User**: "Buy me a ticket to the Summer Music Festival using your wallet"

**Agent**:
1. Checks event details
2. Calculates cost: 0.06 ETH
3. Checks balance: 0.5 ETH ✅
4. Sends payment
5. Responds:

```
✅ Payment Sent Successfully!

💸 Amount: 0.06 ETH
📬 To: 0xVENUE_ADDRESS
🔗 Transaction: 0xabc123...
🌐 View on Explorer: https://sepolia.basescan.org/tx/0xabc123...

Your ticket has been purchased and confirmed on Base Sepolia blockchain!
```

---

## 🔐 Security Considerations

### For Testing (Current Setup)

✅ **Safe:**
- Testnet only (no real money)
- Private key shown in logs for easy recovery
- Wallet automatically generated
- Easy to reset by restarting server

### For Production (Future)

**MUST IMPLEMENT:**

1. **Secure Key Management**
   - Store private key in environment variable
   - Use AWS KMS, Google Cloud KMS, or HashiCorp Vault
   - Never commit keys to git
   - Rotate keys regularly

2. **Spending Limits**
   - Maximum transaction amount
   - Daily/hourly spending caps
   - Require approval for large transactions
   - Multi-signature for critical operations

3. **Access Control**
   - Authentication for send_payment tool
   - Rate limiting
   - IP whitelisting
   - Audit logging

4. **Monitoring**
   - Alert on low balance
   - Alert on unusual transactions
   - Track all outgoing payments
   - Regular balance reconciliation

---

## 📊 Transaction Flow

```
┌──────────────────┐
│   User Request   │
│ "Buy me tickets" │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Ticket Agent    │
│ • Checks balance │
│ • Estimates cost │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  MCP Server      │
│ • Validates tx   │
│ • Sends ETH      │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Base Sepolia     │
│ • Confirms tx    │
│ • Updates state  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Ticket Issued   │
│   QR Code Gen    │
└──────────────────┘
```

---

## 🧪 Testing Checklist

- [ ] Fund agent wallet with Base Sepolia ETH
- [ ] Check balance via `get_wallet_balance`
- [ ] Send small test payment (0.001 ETH)
- [ ] Verify transaction on block explorer
- [ ] Send payment for ticket purchase
- [ ] Confirm ticket issued automatically
- [ ] Test insufficient balance scenario
- [ ] Test invalid address rejection

---

## 🚨 Error Handling

### Insufficient Balance

```json
{
  "success": false,
  "error": "Insufficient balance. Have 0.01 ETH, need 0.06 ETH"
}
```

**Solution**: Fund the wallet with more ETH

### Invalid Address

```json
{
  "success": false,
  "error": "Invalid Ethereum address"
}
```

**Solution**: Provide a valid Ethereum address (checksummed)

### Network Congestion

```json
{
  "success": false,
  "error": "Transaction timeout"
}
```

**Solution**: Retry with higher gas price or wait for network to clear

---

## 🎯 Next Steps

1. **Fund the Agent Wallet**
   ```bash
   # Get testnet ETH from faucet
   # Send to: 0xDA8AEbcca35E679Bb07F0c76D1Dd32cA518166CA
   ```

2. **Test Balance Check**
   ```bash
   curl -X POST http://localhost:8002/execute-tool \
     -d '{"tool_name": "get_wallet_balance", "parameters": {}}'
   ```

3. **Send Test Payment**
   ```bash
   curl -X POST http://localhost:8002/execute-tool \
     -d '{
       "tool_name": "send_payment",
       "parameters": {
         "to_address": "YOUR_TEST_ADDRESS",
         "amount_eth": "0.001"
       }
     }'
   ```

4. **Try Ticket Purchase**
   - Ask agent to buy tickets
   - Agent uses its wallet to pay
   - Automatic confirmation!

---

## 📱 Web Interface Integration

The agent's payment capabilities are accessible via the web interface at http://localhost:8080

**Try asking:**
- "What's your wallet balance?"
- "Send 0.01 ETH to [address]"
- "Buy me a ticket and pay for it"
- "Check if you have enough funds to buy 3 tickets"

---

## 🎉 Summary

Your Ticket Agent can now:

✅ **Check its own balance**
✅ **Send ETH payments on-chain**
✅ **Estimate transaction costs**
✅ **Pay for tickets autonomously**
✅ **Handle errors gracefully**
✅ **Provide transaction receipts**

**Agent Wallet**: `0xDA8AEbcca35E679Bb07F0c76D1Dd32cA518166CA`

**Fund it here**: https://www.coinbase.com/faucets/base-ethereum-goerli-faucet

🚀 **Ready to test agent-initiated blockchain payments!**


