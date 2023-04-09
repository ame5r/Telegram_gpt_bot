import yaml
import dotenv
from pathlib import Path

config_dir = Path(__file__).parent.parent.resolve() / "config"

# load yaml config
with open(config_dir / "config.yml", 'r') as f:
    config_yaml = yaml.safe_load(f)

# load .env config
config_env = dotenv.dotenv_values(config_dir / "config.env")

# config parameters
telegram_token = config_yaml["telegram_token"]
openai_api_key = config_yaml["openai_api_key"]
use_chatgpt_api = config_yaml.get("use_chatgpt_api", True)
allowed_telegram_usernames = config_yaml["allowed_telegram_usernames"]
new_dialog_timeout = config_yaml["new_dialog_timeout"]
enable_message_streaming = config_yaml.get("enable_message_streaming", True)
payme_link = config_yaml['payme_link']
mongodb_uri = f"mongodb://mongo:{config_env['MONGODB_PORT']}"
admin_username = "galactusadmin"
n_default_tokens = config_yaml['n_default_tokens']
HELP_MESSAGE = f"""Commands:
⚪ /balance – Show balance
⚪ /help – Show help
⚪ /paid - Send notifecation for admin to process transaction
"""
ADMIN_HELP_MESSAGE = f"""Commands:
⚪ /balance – Show balance
⚪ /help – Show help
⚪ /paid - Send notifecation for admin to process transaction
⚪ /recharge USERID N_TOKENS - Add tokens for user with USERID
"""
def no_tokens_message():
    
   return f"""<b>You have NO tokens left</b>
You are run out of tokens.
You need at least 100 tokens to be able to ask a question.
But don't worry you can buy token with a small amount of money!
Each 1000 tokens cost ONLY 0.02$.
NOTE: 🔴🔴PLEASE USE YOUR TELEGRAM USER ID WHEN YOU PAY🔴🔴
then send /paid to process your transation."""


def you_got_tokens(amount, current_balance):
    message = f"Congratulations!\nYou have new tokens now!🥳\n"
    message += f"You got {amount} tokens."
    message += f"Current balance: {current_balance}"
    return message


def invalid_parameters():
    return f"Invalid parameters"

def toke_amount_invalid(amountStr):
    return f"The number of token is invalid {amountStr}"

def user_not_exists(user_id):
    return f"user {user_id} does not exist or invalid"

def user_paid(username):
    return f"The user {username} has paid!"


def get_start_message(isAdmin,update):
    reply_text = "Hi! I'm <b>ChatGPT</b> bot implemented with GPT-3.5 OpenAI API 🤖\n\n"
    if not isAdmin:
        reply_text += HELP_MESSAGE
    else:
        reply_text += ADMIN_HELP_MESSAGE
    reply_text += f"\nNEW USER?\n🔴Currently you have FREE {n_default_tokens} tokens"

    reply_text += "\nAnd now... ask me anything!"
    reply_text += f"\nYour ID is {update.message.from_user.id}"

def please_wait():
    return "⏳ Please <b>wait</b> for a reply to the previous message\n"




# chat_modes
with open(config_dir / "chat_modes.yml", 'r') as f:
    chat_modes = yaml.safe_load(f)

# models
with open(config_dir / "models.yml", 'r') as f:
    models = yaml.safe_load(f)
