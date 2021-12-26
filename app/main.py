import os
import logging
from .platform import TextProcessor


def test():
    processor = TextProcessor()
    print(processor.PLUGINS)
    processed = processor.process(text="<html><head></head><body><h1>GeeksForGeeks</h1></body></html>")
    print(processed)


def main():
    r = "data"


if __name__ == '__main__':
    file = open("log", encoding="utf-8", mode="a")
    logging.basicConfig(level=logging.DEBUG,
                        stream=file,
                        format="%(asctime)s "
                               "%(filename)s [line:%(lineno)d] "
                               "%(levelname)s\n"
                               "%(message)s",
                        datefmt="%a, %d %b %Y %H:%M:%S"
                        )
    main()
