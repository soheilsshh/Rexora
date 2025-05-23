# Rexora – WebSocket-Based Trade Copier System

## 📖 Overview

**Rexora** is a real-time trade copying system designed to synchronize trading actions from a single master account to multiple slave accounts. Built using Django and Django Channels, it leverages WebSockets to ensure low-latency communication between the master and slave clients.

---

## 🧩 System Architecture

- **Master Account**: Initiates trade actions (e.g., open, modify, close trades).
- **WebSocket Server**: Handles real-time communication using Django Channels and Redis.
- **Slave Accounts**: Receive and execute trade actions broadcasted by the master.

**Workflow**:
1. The master connects to the WebSocket server and sends trade actions.
2. The server broadcasts these actions to all connected slave accounts.
3. Slave accounts execute the received trade actions accordingly.

---

## 🛠️ Technologies Used

- **Backend**: Django, Django Channels
- **Real-Time Communication**: WebSockets
- **Message Broker**: Redis
- **Testing Tools**: Postman, WebSocket King

---

## 🔗 WebSocket Endpoint

- **URL Pattern**: `ws://<server-address>/ws/trades/<master_id>/`
- **Example**: `ws://localhost:8000/ws/trades/soheilmaster/`

Each slave connects to the WebSocket server using the master's ID to receive relevant trade actions.

---

## 📄 Message Protocol

All messages are JSON-formatted. Below are the supported actions:

### 1. Open Trade

```json
{
  "action": "open_trade",
  "master_account": "soheilmaster",
  "PTI": "Rexora_ABC1234",
  "symbol": "XAUUSD",
  "lot_size": 1.0,
  "type": "buy",
  "price": 1800.5,
  "stop_loss": 1795.0,
  "take_profit": 1810.0,
  "open_time": 1625235900,
  "magic_number": 12345,
  "account_balance": 10000,
  "slippage": 3
}
```

### 2. Modify Trade

```json
{
  "action": "modify_trade",
  "master_account": "soheilmaster",
  "PTI": "Rexora_ABC1234",
  "new_stop_loss": 1790.0,
  "new_take_profit": 1820.0
}
```

### 3. Close Trade

```json
{
  "action": "close_trade",
  "master_account": "soheilmaster",
  "PTI": "Rexora_ABC1234"
}
```

### 4. Open Pending Order

```json
{
  "action": "open_pending_order",
  "master_account": "soheilmaster",
  "PTI": "Rexora_ABC1234",
  "symbol": "XAUUSD",
  "lot_size": 1.0,
  "type": "buy_limit",
  "price": 1790.0,
  "stop_loss": 1785.0,
  "take_profit": 1800.0,
  "open_time": 1625235900,
  "magic_number": 12345,
  "account_balance": 10000,
  "slippage": 3
}
```

---

## 🧰 Installation Guide

Follow the steps below to set up and run the Rexora WebSocket trade copier on your local machine.

### 1. 📆 Clone the Repository

```bash
git clone https://github.com/soheilsshh/Rexora.git
cd Rexora
```

### 2. 🧪 Set Up a Virtual Environment

```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. 📃 Install Dependencies from requirements.txt

```bash
pip install -r requirements.txt
```

> If `requirements.txt` is missing or incomplete, continue with the next step.

### 4. ⚙️ Manually Install Required Libraries

```bash
pip install django
pip install channels
pip install channels_redis
pip install daphne
```

Optional tools for testing:

```bash
pip install websocket-client
```

> Make sure Redis is also installed and running on your machine.

To install Redis:
- macOS: `brew install redis`
- Linux: `sudo apt install redis`
- Windows: Use [Redis for Windows](https://github.com/tporadowski/redis/releases)

To start Redis:

```bash
redis-server
```

### 5. ⚙️ Run Migrations

```bash
python manage.py migrate
```

### 6. 🚀 Run the Development Server

```bash
python manage.py runserver
```

WebSocket server will be available at:

```
ws://localhost:8000/ws/trades/soheilmaster/
```

---

## 🚨 Deployment Notes

When deploying the project to production, make sure you configure Redis in your `settings.py`:

```python
# settings.py

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}
```

Ensure Redis is installed and properly running on the deployment server.

---

## 🚀 Future Enhancements

- Add support for multiple master accounts
- Save all trade actions to a database
- Implement secure communication with SSL/TLS and token-based authentication

---

