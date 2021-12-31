# -*- coding:utf-8 -*-
import traceback
import re
from ..platform import TextProcessor


@TextProcessor.plugin_register("giftFormatter")
class GiftFormat(object):
    """
    本插件用于将标准格式的习题文本转换为gift格式文本。
    标准格式文本如下：

    CATEGORY:习题库/第22章 了解广域网接入技术
    ###
    单选题
    ###
    [题目]
    1)传输距离长，传输容量大，一般采用(  )线缆进行传输。
    [选项]
    A)双绞线
    B)同轴电缆
    C)光纤
    D)电话线
    [答案]C
    ###
    """
    category = ["选择题", "单选题", "多选题", "判断题"]
    lines = []

    def get_answer(self,question_txt):
        an = re.search(r'^\[答案\](.*)', question_txt, flags=re.MULTILINE)
        return an[1]

    def get_explain(self, question_txt):
        """获取答案解析
        :param question_txt: 一道题目完整内容
        :return (gift格式选择题的解析部分
        """
        ex = re.search(r'\[解析\]([\s\S]*)', question_txt)
        ex = '' if not ex else re.sub(r'^\[解析\]', '####', ex[0]) + '\n'
        return ex

    def get_topic(self,cat,question_txt):
        """
        获取题干
        :param cat:题目类型
        :param question_txt:题目完整内容
        :return: 题干gift格式文本
        """
        pattern = ''

        if cat in ["选择题", '单选题', '多选题']:
            pattern = r'^\[题目\]\n\d+\)([\s\S]*)\[选项\]'
        elif cat == '判断题':
            pattern = r'^\[题目\]\n\d+\)([\s\S]*)\[答案\]'

        tp = re.search(pattern, question_txt, flags=re.MULTILINE)

        tp = "::" + cat + "::" + tp[1].strip()

        return tp

    def get_choices(self, question_txt):
        """
        获取选择题的所有选项
        :param ques: 题目完整的文本内容
        :return: gift格式的选择项（带答案）
        """
        ch = re.search(r'\[选项\]([\s\S]*)\[答案\]', question_txt, flags=re.MULTILINE)[1]

        # 处理答案 X) => =
        an = self.get_answer(question_txt).strip()
        prefix = '=' if len(an) == 1 else '~%' + str(100 / len(an)) + "%"
        for e in an:
            ch = re.sub('^' + e + '\\)', prefix, ch, flags=re.MULTILINE)
        ch = re.sub('(^[A-Z]\))', '~', ch, flags=re.MULTILINE)
        return ch

    def parse_ques(self, cat, ques):
        """
        解析指定题目为gift格式
        :param cat:题目类型
        :param ques:题目完整的文本内容
        :return: 一道题的gift格式内容
        """
        gft = ''
        gft += self.get_topic(cat, ques).rstrip() + "{"
        if cat == '选择题' or cat == '多选题' or cat == '单选题':
            gft += self.get_choices(ques)
        elif cat == '判断题':
            gft += 'True' if self.get_answer(ques) == 'A' else 'False'
        else:
            print("unknown question type:" + ques)
            return

        gft += self.get_explain(ques)
        gft += "}\n"
        return gft

    def parse_category(self,cat):
        return re.sub(r'^CATEGORY:(.*) ', r'$CATEGORY: $course$/\1', cat)

    def giften(self,questions):
        self.lines = questions
        gift_result = ""
        cat = ''
        for line in questions:
            line = line.strip()
            if re.search(r'^CATEGORY:', line): # 内容为题库信息
                gift_result += self.parse_category(line) + '\n' + '\n'
            elif line in self.category: # 内容为题型信息
                cat = line
            elif re.search(r'^\[题目\]', line): # 内容为题目
                gift_result += self.parse_ques(cat, line) + '\n'

        return gift_result

    def process(self, text):
        """
        将标准试题抓换位gifg格式
        :param text: 试题列表，每个列表元素一行
        :return: gift格式试题
        """
        # return self.to_gift(text.split("\n"))
        return self.giften(text.split("###"))
        # return text
