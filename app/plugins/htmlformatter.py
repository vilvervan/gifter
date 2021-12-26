from ..platform import TextProcessor
import html


@TextProcessor.plugin_register('htmlFormatter')
class HtmlFormat(object):
    """html文档标签转义
    < => &lt;
    > => &gt:
    ...
    """
    def process(self, text):
        return html.escape(text)
