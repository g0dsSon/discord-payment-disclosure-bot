# Disforcer

A Discord bot that monitors Discord channels and enforces required terms or phrases in messages. Non-compliant messages are automatically removed with DM notifications to users.

## Project Structure
```
disforcer
├── src
│   ├── bot
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── core.py
│   │   ├── logger.py
│   │   ├── server.py
│   │   └── types.py
│   └── config
│       ├── templates
│       │   └── messages.yaml
│       ├── __init__.py
│       ├── config.example.toml
│       └── config.toml
├── tests
│   ├── __init__.py
│   ├── conftest.py
│   └── test_bot.py
├── Dockerfile
├── LICENSE
├── Makefile
├── README.md
├── bot.log
├── fly.toml
└── pyproject.toml
```

## Prerequisites

- Python 3.8+
- Discord Bot Token
- Make (optional, for development commands)

## Setup

1. Clone and setup environment:
```bash
git clone https://github.com/g0dsS0n/disforcer.git
cd disforcer
python -m venv venv
source venv/bin/activate
```

2. Install and configure:
```bash
make install  # Installs package in development mode
make config   # Creates config.toml from example
```

3. Edit `src/bot/config/config.toml` with your Discord token and settings

## Development Commands
```bash
> make help
Available commands:
  install       Install dependencies
  lint          Run linters (black, isort, flake8)
  test          Run tests with pytest
  format        Format code with black and isort
  build         Build the package
  clean         Clean up build artifacts
  run           Run the bot
  config        Create initial config from example
```
## Configuration

### Bot Settings (src/bot/config/config.toml)
```bash
[bot]
token = "YOUR_DISCORD_TOKEN"
prefix = "!"
log_file = "bot.log"

[monitoring]
channels_to_monitor = [
    "selling-artisans",
    "selling-keyboards"
    ]
```
###
 Environment Variables
- `BOT_CONFIG_PATH`: Optional custom config file location

## Deployment Instructions

### Fly.io

1. Install flyctl:
```bash
    curl -L https://fly.io/install.sh | sh
```

2. Login or create account:
```bash
    flyctl auth login
```

3. Create app:
```bash
    flyctl apps create disforcer
```

4. Set Discord token:
```bash
    flyctl secrets set DISCORD_TOKEN=your_token
```

5. Deploy:
```bash
    flyctl deploy
```

6. Verify by monitoring logs:
```bash
    flyctl logs
```

The deployment uses:
- Single machine to prevent duplicate message handling
- Automatic restarts on failure
- Continuous operation (no auto-stop)
- Environment variable for config path

## Discord Setup

1. Go to Discord Developer Portal (https://discord.com/developers/applications)
2. Create new application or select existing one
3. Go to "Bot" section
4. Under "Privileged Gateway Intents", enable "Message Content Intent"
5. Under "Bot Permissions", select:
   - Read Messages/View Channels
   - Send Messages
   - Manage Messages
6. Use the generated permissions integer in your bot invite URL:
   https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=PERMISSION_INTEGER&scope=bot

## Contributing

1. Fork repository
2. Create feature branch
3. Make changes
4. Run make format and make test
5. Submit Pull Request

## License

MIT License - See LICENSE file

## Author

g0dSsOn