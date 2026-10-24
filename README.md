# OSINT Telegram Bot Hosting Instructions

## Hosting Steps for Render / Heroku:
1. **GitHub Repo Banayein**: In sabhi files ko ek repository mein push/upload karein.
2. **Render.com Par Jayein**: Account banayein aur GitHub connect karein.
3. **Background Worker Banayein**: Dashboard par "New" -> "Background Worker" choose karein.
4. **Settings Configuration**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python bot.py`
5. **Environment Variable**:
   - Variable Name: `BOT_TOKEN`
   - Value: BotFather se mila hua Telegram API token enter karein.
6. **Deploy**: Deploy button dabayein!
