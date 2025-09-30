# Saatlik Volatilite Bot — GitHub Actions

This repository runs the volatility bot every hour using GitHub Actions.

## Steps
1. Create a new repository on GitHub and upload these files.
2. Go to Settings → Secrets and variables → Actions → New repository secret, add:
   - TELEGRAM_BOT_TOKEN
   - TELEGRAM_CHAT_ID
3. (Optional) MODE, TOP_N, MIN_VOLUME_USD, MIN_QUOTE_VOL_USDT
4. Go to the Actions tab, enable workflows, and test Run workflow.
