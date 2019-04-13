from config import *
from base_model import *
from flask import Flask, request
import numpy as np
from pymessenger.bot import Bot



app = Flask(__name__)
bot = Bot(ACCESS_TOKEN)

@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET': 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    else:
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                print(message)
                if message.get('message'):
                    recipient_id = message['sender']['id']
                if 'message' in message:
                	print(message['message'])
                    response_sent_text = get_message(message['message'].get('text'))
                    send_message(recipient_id, response_sent_text)

    return "Message Processed"


def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

def get_message(message):
	greetings = [True if word.lower() in GREETING_INPUTS else False for word in message.split()]
    
	if True in greetings:
		return np.random.choice(GREETING_RESPONSES)
	else:
		responce =  get_response(message)
		corpus.remove(message)
		return responce

def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run()
