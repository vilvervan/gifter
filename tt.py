# -*- coding:utf-8 -*-
import re
category = ["选择题", "单选题", "多选题", "判断题"]
with open('t2.txt', 'r',encoding='utf-8') as fp:
    text = fp.read()
    text = re.sub(r'(^[0-9]+)([\)\.、）])', r'[题目]\n\1)', text, flags=re.MULTILINE)
    text = re.sub(r'(^[A-H])([\)\.、）])', r'\1)', text, flags=re.MULTILINE)
    text = re.sub(r'(^\[Explanation:\])', r'[解析]', text, flags=re.MULTILINE)
    text = re.sub(r'\n{2,}([\[题目\]\[选择题\]\[判断题\]\[多选题\]])', r'\n\n\n\1', text, flags=re.MULTILINE)

    lines = re.split(r'\n\n\n', text)

    r = ''
    for line in lines:
        if re.search(r'\[解析\]', line,flags=re.MULTILINE):
            r += re.sub(r'\(([A-H]+)\)([\s\S]*)(\[解析\])', r'\2[答案]\1\n\3', line, re.MULTILINE)
        else:
            r += re.sub(r'\(([A-H]+)\)([\s\S]*)', r'\2\n[答案]\1', line, re.MULTILINE)
        r += '\n\n'
    print(r)
