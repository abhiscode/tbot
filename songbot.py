from config import token

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from telegram import MessageEntity

base_url="https://saavn.sumit.codes/"

import urllib.request, json
def fetchJson(url):
    resp=urllib.request.urlopen(url)
    return json.loads(resp.read().decode())

def start(update, context):
    text="Hello {yourname}".format(yourname=update.effective_user.full_name)
    update.message.reply_text(text)

def download(update, context):
    x=update.message.parse_entity(types= MessageEntity.URL)
    for i in x:
        
        try:
            rejson= fetchJson(base_url + x[i])
        except:
            continue
        if "error" in rejson:
           continue
        title= rejson["result"][0]["song_title"]
        dlink= rejson["result"][0]["download_link"]
        update.message.reply_document(dlink, "{}".format(title))
    update.message.reply_text("I didn't find anything.")












updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start',start))
dispatcher.add_handler(MessageHandler(Filters.entity(MessageEntity.URL), download))
updater.start_polling()
updater.idle()