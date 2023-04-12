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
HELP_MESSAGE = f"""С помощью этого бота вы сможете получить все ответы на вопросы от Искусственного Интеллекта.
Я могу:

💻 Дать развернутый ответ, который не может дать вам Google.

📝 Я могу написать для вас Essay(сочинение) на любую тему.

📚 Написать Assignment, Реферат, Докладную работу на 3000 слов и больше (без плагиата).

🧮 Решать сложные математические задания.

💸 Написать бизнес план
И помочь с работой.

Я понимаю более 10 языков, так же вы можете отправить мне аудио вместо текста.

PRICE LIST
🪬3000 ТОКЕНОВ(~700слов, 3~4 запроса) 15.000 сум
🪬6000 ТОКЕНОВ(~1400слов, 6~7 запросов) 30.000 сум
🪬10000 ТОКЕНОВ(~2400слов, 10~11 запросов) 50.000 сум
 И тд.

Чем больше токенов закупаете, тем больше бот выдает ответов. 
Минимальная оплата 15.000 сум за 
3000 токенов.
Так же имеется услуга «безлимит» на определенное время.
За подробностями @galactusadmin

После оплаты, напишите в чат /paid для подтверждения.
"""
ADMIN_HELP_MESSAGE = f"""Commands:
⚪ /balance – Show balance
⚪ /help – Show help
⚪ /paid - Send notifecation for admin to process transaction
⚪ /recharge USERID N_TOKENS - Add tokens for user with USERID
"""

def no_tokens_message(): 
   return f"""<b>У вас закончились ТОКЕНЫ…😢</b>
Не расстраивайтесь, вы можете обрести токены за минимальную сумму денег!
Каждые 3000 токенов = 15.000 сум!!!

PRICE LIST
🪬3000 ТОКЕНОВ(~700слов, 3~4 запроса) 15.000 сум
🪬6000 ТОКЕНОВ(~1400слов, 6~7 запросов) 30.000 сум
🪬10000 ТОКЕНОВ(~2400слов, 10~11 запросов) 50.000 сум
 И тд.

Чем больше токенов закупаете, тем больше бот выдает ответов. 
Минимальная оплата 15.000 сум за 
3000 токенов.
Так же имеется услуга «безлимит» на определенное время.
За подробностями @galactusadmin

<b>❗️После оплаты, напишите в чат /paid для подтверждения.</b>"""


def you_got_tokens(amount, current_balance):
    message = f"Поздравляем!!\nВы только что приобрели токены!🥳\n"
    message += f"Вы получили <b>{amount}</b> токенов\n"
    message += f"Ваш баланс: <b>{current_balance}</b>"
    return message


def balance_message(total_n_used_tokens,n_current_tokens):
    text = f"Вы использовали <b>{total_n_used_tokens}</b> токенов\n\n"
    text +=f"Ваш баланс на данный момент <b>{str(n_current_tokens)}</b> токенов\n"
    return text
def invalid_parameters():
    return f"Invalid parameters"

def toke_amount_invalid(amountStr):
    return f"The number of token is invalid {amountStr}"

def user_not_exists(user_id):
    return f"user {user_id} does not exist or invalid"

def user_paid(username):
    return f"The user {username} has paid!"


def get_start_message(isAdmin,update):
    reply_text = ''
    if not isAdmin:
        reply_text += f'''
Hi! I'm GALACTUS BOT 🤖

С помощью этого бота вы сможете получить все ответы на вопросы от Искусственного Интеллекта.
Я могу:

💻 Дать развернутый ответ, который не может дать вам Google.

📝 Я могу написать для вас Essay(сочинение) на любую тему.

📚 Написать Assignment, Реферат, Докладную работу на 3000 слов и больше (без плагиата).

🧮 Решать сложные математические задания.

💸 Написать бизнес план
И помочь с работой.

Я понимаю более 10 языков, так же вы можете отправить мне аудио вместо текста.

Commands:
🪬/balance – Показать Баланс
🪬/start – Перезапуск бота
🪬/help – Помощь

🎤 Вы так же можете отправить Голосовое вместо текста.

НОВЫЙ ПОЛЬЗОВАТЕЛЬ ?
❗️Мы предоставляем тебе бесплатно {n_default_tokens} ТОКЕНОВ!!!
Просто задай вопрос:👩‍💻
'''
    else:
        reply_text += ADMIN_HELP_MESSAGE
   # reply_text += f"\nNEW USER?\n🔴Currently you have FREE {n_default_tokens} tokens"

    #reply_text += "\nAnd now... ask me anything!"
    #reply_text += f"\nYour ID is {update.message.from_user.id}"
    return reply_text
def please_wait():
    return "⏳ Пожалуйста <b>подождите</b> пока  бот ответит на предыдущее сообщение.\n"




# chat_modes
with open(config_dir / "chat_modes.yml", 'r') as f:
    chat_modes = yaml.safe_load(f)

# models
with open(config_dir / "models.yml", 'r') as f:
    models = yaml.safe_load(f)
