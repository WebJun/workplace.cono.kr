import logging


def create_logger(fname):
    mylogger = logging.getLogger(fname)
    mylogger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    stream_hander = logging.StreamHandler()
    stream_hander.setFormatter(formatter)
    mylogger.addHandler(stream_hander)

    file_handler = logging.FileHandler(
        f'appdata/logs/{fname}.log', encoding='utf-8')
    file_handler.setFormatter(formatter)
    mylogger.addHandler(file_handler)
    return mylogger
