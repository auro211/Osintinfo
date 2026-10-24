import os
import telebot
import subprocess

# Hosting platform par token environment variable se aayega. 
# Agar local test kar rahe hain toh neeche default mein token daal dein.
BOT_TOKEN = os.environ.get('BOT_TOKEN', 'YAHAN_APNA_BOT_TOKEN_DALEIN')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    help_text = (
        "🤖 *OSINT Bot Active*\n\n"
        "Commands:\n"
        "`/scan_username <username>` - Username scan karne ke liye\n"
        "`/scan_email <email>` - Email scan karne ke liye\n\n"
        "Example: `/scan_username a__dxt`"
    )
    bot.reply_to(message, help_text, parse_mode='Markdown')

@bot.message_handler(commands=['scan_username'])
def scan_username(message):
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "⚠️ Username daalein. Example: `/scan_username a__dxt`", parse_mode='Markdown')
            return
        
        target = parts[1]
        bot.reply_to(message, f"🔍 Scanning username `{target}`... Thoda wait karein.", parse_mode='Markdown')
        
        # user-scanner command run kar rahe hain
        result = subprocess.run(['user-scanner', '-u', target], capture_output=True, text=True, timeout=180)
        
        output = result.stdout
        if not output:
            output = result.stderr
            
        # Telegram message limit 4096 characters hai, isliye truncate kar rahe hain
        if len(output) > 4000:
            output = output[:4000] + "\n\n... [Output truncated due to Telegram limits]"
            
        bot.reply_to(message, f"✅ *Result for {target}:*\n```\n{output}\n```", parse_mode='Markdown')
        
    except subprocess.TimeoutExpired:
        bot.reply_to(message, "❌ Timeout! Scan mein zyada time lag raha hai.")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")

@bot.message_handler(commands=['scan_email'])
def scan_email(message):
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "⚠️ Email daalein. Example: `/scan_email test@gmail.com`", parse_mode='Markdown')
            return
        
        target = parts[1]
        bot.reply_to(message, f"🔍 Scanning email `{target}`... Thoda wait karein.", parse_mode='Markdown')
        
        # user-scanner command run kar rahe hain email ke liye (-e flag)
        result = subprocess.run(['user-scanner', '-e', target], capture_output=True, text=True, timeout=180)
        
        output = result.stdout
        if not output:
            output = result.stderr
            
        if len(output) > 4000:
            output = output[:4000] + "\n\n... [Output truncated due to Telegram limits]"
            
        bot.reply_to(message, f"✅ *Result for {target}:*\n```\n{output}\n```", parse_mode='Markdown')
        
    except subprocess.TimeoutExpired:
        bot.reply_to(message, "❌ Timeout! Scan mein zyada time lag raha hai.")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")

print("Bot is running...")
bot.infinity_polling()
