import os
import logging
from .platform import TextProcessor


def test():
    processor = TextProcessor()
    print(processor.PLUGINS)
    processed = processor.process(text="<html><head></head><body><h1>GeeksForGeeks</h1></body></html>")
    print(processed)


def main(fullfilename):
    """
    开始进行文件转换
    :param fullfilename:文件全路径名
    :return:
    """
    count = 0
    with open(fullfilename,'r',encoding='utf-8') as fp:
        file_content = fp.read()
        processor = TextProcessor()
        # print(processor.PLUGINS)
        processed = processor.process(file_content)
        print(processed)



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
