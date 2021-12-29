import re
from ..platform import TextProcessor

@TextProcessor.plugin_register('txtFormatter')
class TxtFormat(object):
    """
    对试题文本进行标准化处理
    """
    def begin(self,text_lines):
        text = ''
        for line in text_lines:
            # A) 或 A.  A、 => A)
            if re.search(r'^[A-H][\)\.、）]', line) is not None:
                text += re.sub(r'(^[A-H])([\)\.、）])', r'\1)', line)
            # n. xxx => [题目]n) xxx n、xxx => [题目]n) xxx n) xxx => [题目]n) xxx
            elif re.search(r'^[0-9]+[\)\.、）]', line) is not None:
                text += re.sub(r'(^[0-9]+)([\)\.、）])', r'[题目]\n\1)', line)
            else:
                text += line
        return text
    def transform(self,text):
        # A) 或 A.  A、 => A)
        text = re.sub(r'(^[A-H])([\)\.、）])', r'\1)', text, flags=re.MULTILINE)

        # n. xxx => [题目]n) xxx n、xxx => [题目]n) xxx n) xxx => [题目]n) xxx
        text = re.sub(r'(^[0-9]+)([\)\.、）])', r'[题目]\n\1)', text, flags=re.MULTILINE)
        text = re.sub(r'(^[{\[]explain[}\]])', r'[解析]', text, flags=re.MULTILINE)
        return text
    def process(self, text):
        return html.escape(text)