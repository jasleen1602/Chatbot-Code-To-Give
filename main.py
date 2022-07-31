from Bot import ChatBot as bot
import subprocess
import threading
from flask import Flask, render_template, request, json, jsonify
import os
# from translate import Translator
from twilio.twiml.messaging_response import MessagingResponse
# from googletrans import Translator
from langdetect import detect
from google_trans_new import google_translator  
translator = google_translator()  
# translator = Translator(service_urls=['translate.googleapis.com'])

bot = bot.ChatBot.getBot()
usertext = []
botresponse = []

#InputLanguageChoice = StringVar()
#TranslateLanguageChoice = StringVar()
#LanguageChoices = {'Hindi','English','Kannad','Gujrati'}
#InputLanguageChoice.set('English')
#TranslateLanguageChoice.set('Hindi')

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('chat.html')
@app.route("/sms",methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    msg = request.form.get('Body')
    phone_no=request.form.get('From')
    lang = translator.detect(msg)[0]
    print(lang)
    translated_text = translator.translate(msg)
    print(translated_text)
    message = translated_text

    print(message)
    usertext.append(message)
    
    if(len(botresponse)>=1):
        print(1)
        print(botresponse[len(botresponse)-1])
        if(message.find('yes') or message.find('YES') or message.find('Yes')):
            print(2)
            message+=', '
            message+=botresponse[len(botresponse)-1]
            print(message)
        
        elif(message.find('no') or message.find('NO') or message.find('No')):
            message+=', '
            message+=botresponse[len(botresponse)-1]
            print(message)

    while True:
        if message == "":
            return "Sorry, I didn't get that"

        elif len(botresponse)!=0:
        
            if ((message.find('Rs')!=-1 or message.find('rs')!=-1) and (botresponse[len(botresponse)-1] == "Yes, I'm here to help you. How much do you want to earn?")):
                bot_response = "Considering your expectations, help me know more about yourself. Are you currently working"
            # bot_response = str(bot.response(message))
                botresponse.append(bot_response)
                translated_response = translator.translate(bot_response,lang_tgt=lang)
                resp = MessagingResponse()
                resp.message(translated_response)
                print(resp)
                return str(resp)

            elif ((message.find('Rs')!=-1 or message.find('rs')!=-1 )and( botresponse[len(botresponse)-1] == "You will need to rent a place. How much money would you need to start this?" or botresponse[len(botresponse)-1] == "How much money would you need to start this?")):
                res = ''.join(filter(lambda i: i.isdigit(), message))
                free = int(res)
                if(free<10000):
                    message = "less money"
                else:
                    message = "good money"
    
                bot_response = str(bot.response(message,phone_no))
                botresponse.append(bot_response)
                translated_response = translator.translate(bot_response,lang_tgt=lang)
                resp = MessagingResponse()
                resp.message(translated_response)
                print(resp)
                return str(resp)

            elif (message.find('hr')!=-1 or message.find('hours')!=-1 or message.find('hrs')!=-1):
                res = ''.join(filter(lambda i: i.isdigit(), message))
                free = int(res)

                if(free<=3):
                    bot_response = "You do not get enough free time to start a business. Do you have people who can work with you."
                else:
                    bot_response = "You are getting enough time to start something new. Do you have any idea?"
                botresponse.append(bot_response)
                translated_response = translator.translate(bot_response,lang_tgt=lang)
                resp = MessagingResponse()
                resp.message(translated_response)
                print(resp)
                return str(resp)

            bot_response = str(bot.response(message,phone_no))
            botresponse.append(bot_response)
            translated_response = translator.translate(bot_response,lang_tgt=lang)
            resp = MessagingResponse()
            resp.message(translated_response)
            print(resp)
            return str(resp)

        else:
            bot_response = str(bot.response(message,phone_no))
            botresponse.append(bot_response)
            translated_response = translator.translate(bot_response,lang_tgt=lang)
            resp = MessagingResponse()
            resp.message(translated_response)
            print(resp)
            return str(resp)

usertxt = []
botresp = []


   
@app.route("/ask", methods=['POST'])
def ask():
   
    txt = (request.form['messageText'])
    if(txt==""):
        message = ""
    else:
        lang = translator.detect(txt)[0]
        print(lang)
        translated_text = translator.translate(txt)
        message = translated_text

    print(message)
    usertxt.append(message)

    if(len(botresp)>=1):
        print(1)
        print(botresp[len(botresp)-1])
        if(message.find('yes') or message.find('YES') or message.find('Yes')):
            print(2)
            message+=', '
            message+=botresp[len(botresp)-1]
            print(message)
        
        elif(message.find('no') or message.find('NO') or message.find('No')):
            message+=', '
            message+=botresp[len(botresp)-1]
            print(message)
    
    while True:
        if message == "":
            return jsonify({'status':'OK','answer':"Sorry, I didn't get that", 'lang':'en'})
            # continue

        elif len(botresp)!=0:
    
            if ((message.find('Rs')!=-1 or message.find('rs')!=-1) and (botresp[len(botresp)-1] == "Yes, I'm here to help you. How much do you want to earn?")):
                bot_response = "Considering your expectations, help me know more about yourself. Are you currently working"
            # bot_response = str(bot.response(message))
                botresp.append(bot_response)
                translated_response = translator.translate(bot_response,lang_tgt=lang)
                response = translated_response
                print(response)
                return jsonify({'status':'OK','answer':response, 'lang':lang})

            elif ((message.find('Rs')!=-1 or message.find('rs')!=-1 )and( botresp[len(botresp)-1] == "You will need to rent a place. How much money would you need to start this?" or botresp[len(botresp)-1] == "How much money would you need to start this?")):
                res = ''.join(filter(lambda i: i.isdigit(), message))
                free = int(res)
                if(free<10000):
                    message = "less money"
                else:
                    message = "good money"
    
                bot_response = str(bot.response(message))
                botresp.append(bot_response)
                translated_response = translator.translate(bot_response,lang_tgt=lang)
                response = translated_response
                print(response)
                return jsonify({'status':'OK','answer':response, 'lang':lang})

            elif (message.find('hr')!=-1 or message.find('hours')!=-1 or message.find('hrs')!=-1):
                res = ''.join(filter(lambda i: i.isdigit(), message))
                free = int(res)

                if(free<=3):
                    bot_response = "You do not get enough free time to start a business. Do you have people who can work with you."
                else:
                    bot_response = "You are getting enough time to start something new. Do you have any idea?"
                botresp.append(bot_response)
                translated_response = translator.translate(bot_response,lang_tgt=lang)
                response = translated_response
                print(response)
                return jsonify({'status':'OK','answer':response, 'lang':lang})

            bot_response = str(bot.response(message))
            botresp.append(bot_response)
            translated_response = translator.translate(bot_response,lang_tgt=lang)
            response = translated_response
            print(response)
            return jsonify({'status':'OK','answer':response, 'lang':lang})

        else:
            bot_response = str(bot.response(message))
            botresp.append(bot_response)
            translated_response = translator.translate(bot_response,lang_tgt=lang)
            response = translated_response
            print(response)
            return jsonify({'status':'OK','answer':response, 'lang':lang})













#@app.route("/ask", methods=['POST'])
#def ask():
#    message = request.form['messageText']
#   ans = bot.get_response(message)
#   print(ans)
#   while True:
#       if message == "quit":
#           exit()
#       else:
#           class Object:
#               def __init__(self, status=None, answer=None):
#                    self.status = status
#                    self.answer = answer
#
#                def toJSON(self):
#                    return json.dumps(self, default=lambda o: o.__dict__, 
#            sort_keys=True, indent=4)
#            data = Object('OK', ans)
#            return data.toJSON()


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)