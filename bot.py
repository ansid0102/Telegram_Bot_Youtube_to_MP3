from __future__ import unicode_literals
from telegram import User, Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import youtube_dl
import os
import requests
import logging
from pydub import AudioSegment
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_text(
        "Hello! Welcome to YT2MP3 Bot paste link to download")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def download(update: Update, context: CallbackContext) -> None:
    link = str(context.args[0])
    update.message.reply_text("downloading")
    ydl_opts = {
        'format': 'bestaudio/best ',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'noplaylist': True,
        'outtmpl': 'download'+'.%(ext)s',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.cache.remove()
        ydl.download([link])
        context.bot.send_audio(chat_id=update.message.chat_id, audio=open(
            '/home/sid/telebot/download.mp3', 'rb'), protect_content=False)


def main() -> None:
    updater = Updater(
        token='5155533820:AAH_aSy2_GrN0MaKX7HtFOczXWaEP6v9ANY', use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("download", download))
    dispatcher.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
