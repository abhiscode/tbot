from config import token

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from telegram import MessageEntity

base_url="http://206.189.128.223:5000/result/?query="

import urllib.request, json
def fjson(url):
    resp=urllib.request.urlopen(url)
    return json.loads(resp.read().decode())

def start(update, context):
    text="Hello {yourname}".format(yourname=update.effective_user.full_name)
    update.message.reply_text(text)

def download(update, context):
    x=update.message.parse_entities(types= MessageEntity.URL)
    msg=update.message.reply_text("Fetching.....")
    for i in x:
        try:
            rjson= fjson(base_url + x[i])
            title= rjson["song"]
            link= rjson["media_url"]
            msg.delete()
            update.message.reply_document(link, filename=title + ".mp3", caption= "{}".format(title))
            continue 
        except:
            continue
        if "error" in rjson:
            continue
    msg.edit_text("I didn't find anything.")











updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start',start))
dispatcher.add_handler(MessageHandler(Filters.entity(MessageEntity.URL), download))
updater.start_polling()
updater.idle()