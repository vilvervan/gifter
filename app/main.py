import sys
import os
import logging
from .platform import TextProcessor

from pathlib import Path
print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())


def main(fullfilename):
    """
    开始进行文件转换
    :param fullfilename:文件全路径名
    :return:
    """

    if not os.path.exists(fullfilename):
        print("Oops,file doesn't exist!")
        return

    with open(fullfilename,'r',encoding='utf-8') as fp:
        file_content = fp.read()
        processor = TextProcessor()
        processed = processor.process(file_content)
        print(processed)
        return processed


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
