import ptbot
import os
from dotenv import load_dotenv
from pytimeparse import parse

load_dotenv()


TG_TOKEN = os.environ['TGBOT_TOKEN']  # подставьте свой ключ API
TG_CHAT_ID = os.environ['TGBOT_CHAT_ID']  # подставьте свой ID
BOT = ptbot.Bot(TG_TOKEN)


def render_progressbar(total,
                       iteration,
                       prefix='',
                       suffix='',
                       length=30,
                       fill='█',
                       zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def timer_done(chat_id):
    timer_is_done = 'Время вышло!'
    BOT.send_message(chat_id, timer_is_done)


def wait_timer(chat_id, text):
    message_id = BOT.send_message(chat_id, "Запускаю таймер")
    timeout_secs = parse(text)

    BOT.create_countdown(timeout_secs,
                         notify_progress,
                         chat_id=chat_id,
                         message_id=message_id,
                         timeout_secs_total=timeout_secs)

    BOT.create_timer(timeout_secs, timer_done, chat_id=chat_id,)


def notify_progress(secs_left, chat_id, message_id, timeout_secs_total):
    BOT.update_message(chat_id,
                       message_id,
                       "Осталось секунд: {}".format(secs_left)
                       + '\n'
                       + render_progressbar(timeout_secs_total, secs_left))


def main():
    BOT.reply_on_message(wait_timer)
    BOT.run_bot()


if __name__ == '__main__':
    main()
