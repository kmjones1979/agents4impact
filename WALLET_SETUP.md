# 🔐 Agent Wallet Setup Guide - USDC on Base Sepolia

## 📍 Where to Put Your Private Key

Your agent's private key goes in **ONE PLACE**:

```bash
/Users/kevinjones/google/mcp-ticket-server/.env
```

---

## 🚀 Quick Setup (2 Minutes)

### Step 1: Create the `.env` file

```bash
cd /Users/kevinjones/google/mcp-ticket-server
cp .env.example .env
```

### Step 2: Get Your Private Key from MetaMask

1. Open MetaMask
2. Click on your account icon (top right)
3. Select **Account Details**
4. Click **Show Private Key**
5. Enter your MetaMask password
6. Copy the private key

⚠️ **IMPORTANT**: Keep this private key secret! Never share it or commit it to Git.

### Step 3: Add Private Key to `.env`

Open `/Users/kevinjones/google/mcp-ticket-server/.env` and add:

```env
# Agent Wallet Configuration
PAYMENT_WALLET_PRIVATE_KEY=your_private_key_here
```

**With or without `0x` prefix - both work!**

Examples:

```env
# Option 1 (with 0x)
PAYMENT_WALLET_PRIVATE_KEY=0xcf26437df85673195404796ecc02c1eaf90e92b7fd76880890fbec28c7f7b91d

# Option 2 (without 0x)
PAYMENT_WALLET_PRIVATE_KEY=cf26437df85673195404796ecc02c1eaf90e92b7fd76880890fbec28c7f7b91d
```

### Step 4: Restart the MCP Server

```bash
cd /Users/kevinjones/google/mcp-ticket-server
pkill -f "tsx watch src/server.ts"
npm run dev
```

You should see:

```
💎 Blockchain Service Initialized
📬 Agent Wallet Address: 0xYourAddress
💵 USDC Contract: 0x036CbD53842c5426634e7929541eC2318f3dCF7e
```

---

## 💎 What is the Public Address?

The **public address** is automatically derived from your private key.

**You DON'T need to configure it separately!**

When you start the server, it will show you:

```
📬 Agent Wallet Address: 0xe0259BD6F7780ce94e4853608b50A319D70bF67d
```

This is your agent's public address - you can share this freely!

---

## 💰 Fund Your Wallet

### Get USDC on Base Sepolia

**Option 1: Circle Faucet (Recommended)**

1. Visit: https://faucet.circle.com/
2. Select **"Base Sepolia"**
3. Enter your wallet address: `0xYourAddress`
4. Click **"Get USDC"**
5. You'll receive 10 USDC testnet tokens

**Option 2: Coinbase Faucet**

1. Visit: https://www.coinbase.com/faucets/base-ethereum-goerli-faucet
2. Connect your MetaMask wallet
3. Request testnet ETH (needed for gas)
4. Swap some ETH for USDC on a testnet DEX

### Get ETH for Gas

Even though payments are in USDC, you need ETH for transaction fees!

1. Visit: https://www.coinbase.com/faucets/base-ethereum-goerli-faucet
2. Enter your wallet address
3. Request testnet ETH
4. You'll receive ~0.5 ETH (enough for thousands of transactions)

---

## ✅ Verify Setup

### Check Your Wallet Balance

```bash
curl http://localhost:3000/mcp/tool/get_balance
```

Response:

```json
{
    "success": true,
    "address": "0xYourAddress",
    "balanceUSDC": "10.00",
    "balanceETH": "0.5",
    "network": "Base Sepolia",
    "chainId": 84532,
    "usdcContract": "0x036CbD53842c5426634e7929541eC2318f3dCF7e"
}
```

### Via Ticket Agent

```bash
curl -X POST http://localhost:8002/execute-tool \
  -H "Content-Type: application/json" \
  -d '{"tool_name": "get_wallet_balance", "parameters": {}}'
```

---

## 📁 Complete File Structure

```
/Users/kevinjones/google/
├── mcp-ticket-server/
│   ├── .env                 ← PUT PRIVATE KEY HERE
│   ├── .env.example         ← Template file
│   ├── src/
│   │   ├── blockchain.ts    ← Uses .env
│   │   └── server.ts
│   └── package.json
└── agents/
    └── ticket_agent.py      ← Uses MCP server
```

---

## 🔐 The `.env` File (Complete Example)

```env
# Server Configuration
PORT=3000

# 🔑 AGENT WALLET CONFIGURATION
# This is where you put YOUR agent's private key
# Get it from MetaMask: Account Details > Export Private Key
PAYMENT_WALLET_PRIVATE_KEY=your_private_key_here

# Blockchain Configuration (Base Sepolia)
BASE_SEPOLIA_RPC=https://sepolia.base.org
USDC_CONTRACT_ADDRESS=0x036CbD53842c5426634e7929541eC2318f3dCF7e
```

---

## 🎯 How the Agent Uses This Wallet

### 1. **Receiving Payments**

When a user buys tickets:

-   System generates payment request
-   User sends USDC to agent's wallet address
-   System detects USDC transfer
-   Ticket automatically issued

### 2. **Sending Payments**

When the agent pays for something:

-   Agent checks USDC balance
-   Agent sends USDC transaction
-   Uses ETH for gas fees
-   Transaction confirmed on-chain

---

## 🔍 Finding Your Public Address

### Method 1: From Server Logs

Start the server and look for:

```
📬 Agent Wallet Address: 0xYourPublicAddress
```

### Method 2: Using API

```bash
curl http://localhost:3000/mcp/tool/get_balance | python3 -m json.tool
```

### Method 3: From MetaMask

If you used your MetaMask private key:

1. Open MetaMask
2. Click on your account name
3. The address is shown below the name
4. Click to copy

---

## 🛡️ Security Best Practices

### ✅ DO:

1. **Keep `.env` secret**

    ```bash
    # Already in .gitignore
    echo ".env" >> .gitignore
    ```

2. **Use a dedicated wallet for the agent**

    - Don't use your personal MetaMask wallet
    - Create a new wallet just for the agent

3. **Start with testnet**

    - Test everything on Base Sepolia first
    - Never use testnet keys on mainnet

4. **Back up your private key**

    - Store it in a password manager
    - Don't save it in multiple files

5. **Monitor your wallet**
    - Check balance regularly
    - Set up alerts for low balance

### ❌ DON'T:

1. **Never commit `.env` to Git**

    - It's already in `.gitignore`
    - Double-check before pushing

2. **Don't share your private key**

    - Not in Discord
    - Not in screenshots
    - Not in documentation

3. **Don't use the same key across multiple projects**

    - Each agent should have its own wallet

4. **Don't use temporary/generated keys in production**
    - The auto-generated key changes on restart
    - Always configure `PAYMENT_WALLET_PRIVATE_KEY`

---

## 🧪 Testing Your Setup

### Test 1: Check Balance

```bash
curl -X POST http://localhost:8002/execute-tool \
  -H "Content-Type: application/json" \
  -d '{"tool_name": "get_wallet_balance", "parameters": {}}'
```

Expected:

```json
{
    "success": true,
    "balanceUSDC": "10.00",
    "balanceETH": "0.5"
}
```

### Test 2: Send Test Payment

```bash
curl -X POST http://localhost:8002/execute-tool \
  -H "Content-Type: application/json" \
  -d '{
    "tool_name": "send_payment",
    "parameters": {
      "to_address": "0x1234567890123456789012345678901234567890",
      "amount_usd": "1.00"
    }
  }'
```

### Test 3: Purchase Tickets

```bash
curl -X POST http://localhost:8002/execute-tool \
  -H "Content-Type: application/json" \
  -d '{
    "tool_name": "purchase_tickets",
    "parameters": {
      "event_id": "event-3",
      "quantity": 1,
      "customer_email": "test@example.com",
      "customer_name": "Test User"
    }
  }'
```

---

## 🚨 Troubleshooting

### Problem: "No wallet configured"

**Solution**: Make sure `.env` file exists with `PAYMENT_WALLET_PRIVATE_KEY`

```bash
cd /Users/kevinjones/google/mcp-ticket-server
cat .env  # Should show your private key
```

### Problem: "Using temporary wallet"

**Solution**: You haven't set `PAYMENT_WALLET_PRIVATE_KEY` in `.env`

The server will generate a random wallet that changes on restart.

### Problem: "Insufficient USDC balance"

**Solution**: Fund your wallet from the faucet

-   https://faucet.circle.com/ (for USDC)
-   https://www.coinbase.com/faucets/base-ethereum-goerli-faucet (for ETH gas)

### Problem: "Invalid private key"

**Solutions**:

1. Make sure there are no spaces or quotes around the key
2. Try with and without the `0x` prefix
3. Make sure you copied the full key (64 characters)

### Problem: "Transaction failed"

**Solution**: Make sure you have ETH for gas fees

```bash
# Check ETH balance
curl http://localhost:3000/mcp/tool/get_balance
```

If `balanceETH` is 0, get some from the faucet.

---

## 📋 Checklist

-   [ ] Created `/Users/kevinjones/google/mcp-ticket-server/.env`
-   [ ] Added `PAYMENT_WALLET_PRIVATE_KEY` to `.env`
-   [ ] Restarted MCP server
-   [ ] Verified agent wallet address appears in logs
-   [ ] Funded wallet with USDC from https://faucet.circle.com/
-   [ ] Funded wallet with ETH from Coinbase faucet
-   [ ] Tested balance check
-   [ ] Tested sending a small payment
-   [ ] Ready to buy tickets! 🎫

---

## 🎉 You're All Set!

Your agent now has:

-   ✅ A persistent wallet (doesn't change on restart)
-   ✅ USDC balance for payments
-   ✅ ETH balance for gas fees
-   ✅ Ability to send and receive USDC
-   ✅ Automatic ticket purchases

**Agent Wallet Address**: Check your server logs!

**Next Steps**:

1. Try buying a ticket through the web interface
2. Ask the agent to check its balance
3. Test agent-initiated payments

🚀 **Happy ticket selling with USDC!**
