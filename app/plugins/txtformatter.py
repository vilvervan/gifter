import re
from ..platform import TextProcessor

@TextProcessor.plugin_register('txtFormatter')
class TxtFormat(object):
    """
    对试题文本进行标准化处理
    试题文本格式要求：

    选择题
    1、题干(答案)
    A、选项
    B、选项
    [Explanation:]题目解析内容

    判断题
    1、题干(答案)
    [Explanation:]题目解析内容

    、  也可以是.或者全角）
    :   半角冒号
    题型名称包括：选择题（或单选题，同一个意思）、多选题、判断题
    """
    def transform(self,text):
        text = re.sub(r'(^[0-9]+)([\)\.、）])', r'[题目]\n\1)', text, flags=re.MULTILINE)
        text = re.sub(r'(^[A-H])([\)\.、）])', r'\1)', text, flags=re.MULTILINE)
        text = re.sub(r'(^[A][\)])', r'[选项]\1', text, flags=re.MULTILINE)
        text = re.sub(r'(^\[Explanation:\])', r'[解析]', text, flags=re.MULTILINE)
        text = re.sub(r'\n{2,}([\[题目\]\[选择题\]\[单选题\]\[判断题\]\[多选题\]])', r'\n\n\n\1', text, flags=re.MULTILINE)

        lines = re.split(r'\n\n\n', text)

        r = ''
        for line in lines:
            if re.search(r'\[解析\]', line, flags=re.MULTILINE):
                r += re.sub(r'\(([A-H]+)\)([\s\S]*)(\[解析\])', r'\2[答案]\1\n\3', line, re.MULTILINE)
            else:
                r += re.sub(r'\(([A-H]+)\)([\s\S]*)', r'\2\n[答案]\1', line, re.MULTILINE)
            r += '\n\n'

        print(r)
        return r
    def process(self, text):
        return self.transform(text)