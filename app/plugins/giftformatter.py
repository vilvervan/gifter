import re
from ..platform import TextProcessor


@TextProcessor.plugin_register("giftFormatter")
class GiftFormat(object):
    @classmethod
    def choice_handle(cls, lines, index):
        """
        处理选择题
        :param lines:存放原始试题内容的列表
        :param index: 选择题开始的序号（包含选择题或单选题的题目文字所在的序号）
        :return: gift格式的所有选择题
        """

        def get_next_choice(start_index):
            """
            获取下一道选择题
            :param i: 检索选择题的开始行号，将会从start_index+1行开始检索下一道选择题
            :return: ｛index:下一道选择题的行号,value: 检索到的下一道选择题的全部文本，count:下一道选择题所占行数}
            """
            q = {'index': start_index, 'value': '', 'count': 0}
            count = 0
            i = start_index
            for line in lines[i:]:
                count += 1
            return q

        def get_topic(question_txt):
            """获取题目
            :param question_txt: 一道题目完整内容
            :return:
            """
            return re.search('^\[题目\](.*)\[选项\]',question_txt)

        def get_choice(question_txt):
            """获取选项
            :param question_txt: 一道题目完整内容
            :return: 以元组形式返回所有选项
            """
            return ""

        def get_answer(question_txt):
            """获取答案
            :param question_txt: 一道题目完整内容
            :return: 返回答案
            """
            return ""

        def get_explain(question_txt):
            """获取答案解析
            :param question_txt: 一道题目完整内容
            """
            return ""

        idx = index
        gift_txt = ""
        tmp = get_next_choice(idx)
        while tmp != {}:
            gift_txt += get_topic(tmp.value) + get_choice(tmp.value) + get_answer(tmp.value) + get_explain(tmp.value) + "\r\n"
            tmp = get_next_choice(tmp.index)
        return gift_txt, tmp.count

    def to_gift(self, text_lines):
        """转换为gift格式文本
        :param text_lines: 待转换的标准试题文本内容
        :return: gift格式试题文本内容
        """
        for idx, line in enumerate(text_lines):
            if "选择题" in line or "单选题" in line:
                choice = self.choice_handle(text_lines, idx)
                print(choice[0])

    def process(self, text):
        """
        将标准试题抓换位gifg格式
        :param text: 试题列表，每个列表元素一行
        :return: gift格式试题
        """
        return self.to_gift(text)
