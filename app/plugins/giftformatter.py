# -*- coding:utf-8 -*-
import traceback
import re
from ..platform import TextProcessor


@TextProcessor.plugin_register("giftFormatter")
class GiftFormat(object):
    category = ["选择题", "单选题", "多选题", "判断题"]
    lines = []

    def get_next_question(self, start_index):
        """
        获取下一道选择题
        :param start_index: 开始行号(不包括“选择题”题目)
        :return: ｛index:下一道选择题的行号,value: 检索到的下一道选择题的全部文本，count:下一道选择题所占行数}
        """
        q = {'index': start_index, 'value': '', 'line_count': 0}
        i = start_index
        first = False
        for line in self.lines[i:]:
            q['line_count'] += 1
            if len(line.strip()) == 0:
                continue

            if line in self.category:
                break

            if '[题目]' in line:
                if first is False:
                    first = True
                else:
                    q['line_count'] -= 1
                    break

            if any(ext in line for ext in self.category):
                q['line_count'] -= 1
                break

            q['value'] += line + '\n'
        return q

    def get_answer(self,question_txt):
        an = re.search('^\[答案\]([\s\S]*)\[解析\]', question_txt, flags=re.MULTILINE)
        return an[1]
        return ''

    def get_explain(self, question_txt):
        """获取答案解析
        :param question_txt: 一道题目完整内容
        :return (gift格式选择题的解析部分
        """
        ex = re.search('\[解析\]([\s\S]*)', question_txt)
        ex = re.sub('(^\[解析\])', '####', ex[0])
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
            pattern = r'^\[题目\]([\s\S]*)\[选项\]'
        elif cat == '判断题':
            pattern = r'^\[题目\]([\s\S]*)\[答案\]'

        tp = re.search(pattern, question_txt)
        tp = "::" + cat + "::" + tp[1]

        return tp

    def get_choices(self, question_txt):
        """
        获取选择题的所有选项
        :param ques: 题目完整的文本内容
        :return: gift格式的选择项（带答案）
        """
        ch = re.search('\[选项\]([\s\S]*)\[答案\]', question_txt)[1]

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
        if cat == '判断题':
            gft += self.get_answer(ques)
        gft += self.get_explain(ques)
        gft += "}\n"
        return gft

    def handle_type(self,index,cat):
        """
        批量转换某种题型
        :param index:该题型题目开始的行号
        :param cat: 题型名称
        :return: 该题型所有题目的gift格式文本
        """
        idx = index
        gift_ques = ""
        tmp = self.get_next_question(idx)
        while tmp['line_count'] > 0:
            gift_ques += self.parse_ques(cat, tmp['value']) + '\n'
            idx = tmp['index'] + tmp['line_count']
            tmp = self.get_next_question(idx)
        return gift_ques, idx

    def to_gift(self, text_lines):
        """标准文件转换为gift格式文本
        :param text_lines: 待转换的标准试题文本列表，一个元素表示一行试题文本
        :return: gift格式试题文本内容,下一大题的开始行号
        """
        self.lines = text_lines
        gift_result = ""
        i = 0
        while i < len(text_lines):
            line = text_lines[i]
            ct = [ele for ele in self.category if ele in line]
            if len(ct) > 0:
                rt = self.handle_type(i + 1, ct[0])
                gift_result += rt[0] + '\n'
                i = rt[1]
                continue
            else:
                i += 1

        return gift_result

    def process(self, text):
        """
        将标准试题抓换位gifg格式
        :param text: 试题列表，每个列表元素一行
        :return: gift格式试题
        """
        return self.to_gift(text.split("\n"))
