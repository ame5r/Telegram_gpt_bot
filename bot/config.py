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
admin_username = "AmeerGN" #"aaa999011"
n_default_tokens = config_yaml['n_default_tokens']

def no_tokens_message(tokens_spent, balance):
    
   return f"""<b>You have NO tokens left</b>
You have totally spent {tokens_spent} tokens while your balance is {balance}.
Each 1000 tokens cost ONLY 0.02$.
NOTE: 🔴🔴PLEASE USE YOUR TELEGRAM USERNAME WHEN YOU PAY🔴🔴
then send /paid to process your transation."""
# chat_modes
with open(config_dir / "chat_modes.yml", 'r') as f:
    chat_modes = yaml.safe_load(f)

# models
with open(config_dir / "models.yml", 'r') as f:
    models = yaml.safe_load(f)
