import ptbot
from pytimeparse import parse
from decouple import config


TG_TIMER_TOKEN = config('TGBOT_TOKEN', default='')


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


def timer_done(chat_id, bot):
    timer_is_done = 'Время вышло!'
    bot.send_message(chat_id, timer_is_done)


def wait_timer(chat_id, text, bot):
    message_id = bot.send_message(chat_id, "Запускаю таймер")
    timeout_secs = parse(text)

    bot.create_countdown(timeout_secs,
                         notify_progress,
                         chat_id=chat_id,
                         message_id=message_id,
                         timeout_secs_total=timeout_secs,
                         bot=bot)

    bot.create_timer(timeout_secs + 0.1, timer_done, chat_id=chat_id, bot=bot)


def notify_progress(secs_left, chat_id, message_id, timeout_secs_total, bot):
    bot.update_message(chat_id,
                       message_id,
                       "Осталось секунд: {}".format(secs_left)
                       + '\n'
                       + render_progressbar(timeout_secs_total, secs_left))


def main():
    bot = ptbot.Bot(TG_TIMER_TOKEN)

    def adapter_wait_timer(chat_id, text):
        return wait_timer(chat_id, text, bot)

    bot.reply_on_message(adapter_wait_timer)
    bot.run_bot()


if __name__ == '__main__':
    main()
