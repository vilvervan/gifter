import re
from ..platform import TextProcessor

@TextProcessor.plugin_register('txtFormatter')
class TxtFormat(object):
    """
    # 对试题文本进行标准化处理.
    # 本插件适合处理如下格式试题：

    Category:题目名称(如果分级的话，级别之间用/隔开）
    选择题
    1、题干(A)
    A、选项
    B、选项
    C.
    ...
    [Explanation:]题目解析内容.如果没有注释，则去掉该部分

    多选题
    1、题干(ABC)
    A、选项
    B、选项
    C.
    D.
    E.

    判断题
    1、题干(答案)
    [Explanation:]题目解析内容

    Category:题目名称(如果分级的话，级别之间用/隔开）
    选择题
    ...

    多选题
    ...

    判断题
    ...

    注意：
    * 1、 1. 1） 三种形式都可以
    * Category: 中的冒号是半角冒号
    * 题型名称包括：选择题（或单选题，这两个名称都表示单选题）、多选题、判断题
    """
    def transform(self,text):
        # 题干前面增加[题目]
        text = re.sub(r'(^[0-9]+)([\)\.、）])', r'[题目]\n\1)', text, flags=re.MULTILINE)

        # A、A. A） => A)
        text = re.sub(r'(^[A-H])([\)\.、）])', r'\1)', text, flags=re.MULTILINE)

        # 第一个选项前面增加 [选项】
        text = re.sub(r'(^[A][\)])', r'[选项]\n\1', text, flags=re.MULTILINE)

        # [Explanation:] => [解析]
        text = re.sub(r'(^\{Explanation:\})', r'[解析]', text, flags=re.MULTILINE)

        # [题目] 选择题 单选题 判断题 多选题 前面的空行标准化为两个空行（3个\n)
        text = re.sub(r'\n{1,}^(\[题目\]|选择题|单选题|判断题|多选题|CATEGORY:)', r'\n\n\n\1', text, flags=re.MULTILINE)

        # 划分题目到列表中
        lines = re.split(r'\n\n\n', text)

        qe = ''
        for line in lines:
            line = line.strip()
            if re.search(r'\[解析\]', line, flags=re.MULTILINE):
                qe += re.sub(r'\(([A-H]+)\)([\s\S]*)(\[解析\])', r'\2[答案]\1\n\3', line, re.MULTILINE)
            else:
                qe += re.sub(r'\(([A-H]+)\)([\s\S]*)', r'\2\n[答案]\1', line, re.MULTILINE)
            qe += '\n###\n'

        # print(qe)
        return qe

    def process(self, text):
        return self.transform(text)