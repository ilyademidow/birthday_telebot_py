# Yes. Exactly. This is one more Telegram bot

I did similar in NodeJS if you want you can check https://github.com/ilyademidow/birthday_telebot/tree/master

* Bot congrats/reminds a person at his/her/its birthday in any Telegram channel
* You can manage a list of persons

# How can I use it?

## Prerequisits
1. You've registered your bot so you have Bot Auth Key and Bot Name
1. You know the Chat ID which you want to send Birthday congratulations

## How to run it?

Clone this repo to any directory. We define it `<git cloned path>`

### How to run it directly?
1. Install Python 3.10 and PIP
1. Install all required libraries. Run `pip install -r requirements.txt`
1. Put environment variables TELEGRAM_TOKEN, EFFECTIVE_CHAT_ID
1. Run `python3 bd-tg-bot.py`
1. Enjoy!

### How to deploy it to your Kubernetes cluster through GitHub actions
1. Create KUBE_CONFIG GitHub Action secret and put k8s config encoded in base64
1. Create TELEGRAM_TOKEN, EFFECTIVE_CHAT_ID GitHub Action secret and put your values there
1. Run github Actions