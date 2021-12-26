class TextProcessor(object):
    PLUGINS = {}

    def process(self,text,plugins=()):
        if plugins == ():
            for plugin_name in self.PLUGINS.keys():
                text = self.PLUGINS[plugin_name]().process(text)
        else:
            for plugin_name in plugins:
                text = self.PLUGINS[plugin_name]().process(text)
        return text

    @classmethod
    def plugin_register(cls,plugin_name):
        def wrapper(plugin):
            cls.PLUGINS.update({plugin_name:plugin})
            return plugin
        return wrapper
