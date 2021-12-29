# -*- coding:utf-8 -*-
import re
category = ["选择题", "单选题", "多选题", "判断题"]
with open('t2.txt', 'r',encoding='utf-8') as fp:
    text = fp.read()
    text = re.sub(r'(^[0-9]+)([\)\.、）])', r'[题目]\n\1)', text, flags=re.MULTILINE)
    text = re.sub(r'(^[A-H])([\)\.、）])', r'\1)', text, flags=re.MULTILINE)
    text = re.sub(r'(^\[Explanation:\])', r'[解析]', text, flags=re.MULTILINE)
    text = re.sub(r'\n\n([\[题目\]\[选择题\]\[判断题\]\[多选题\]])', r'\n\n\n\1', text, flags=re.MULTILINE)

    lines = re.split(r'\n\n\n', text)

    for line in lines:
        # r += re.sub('\(([A-H]+)\)([\s\S]*)(\[解析\])', r'\2[答案]\1\n\3', line, re.MULTILINE)
        print(line)
