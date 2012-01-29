
import os, inspect
from zope.interface import implements
from zope.component import getUtility,provideUtility,provideAdapter

from bit.core.interfaces import IPlugin, IConfiguration, IPluginExtender
from bit.bot.common.interfaces import  IIntelligent

from bit.bot.aiml.ai import BitAI

from bit.bot.base.plugin import BotPlugin
from bit.bot.aiml.handlers import bot_speaks

from bit.bot.aiml.extends import AIMLPlugin

class BitBotAIPlugin(BotPlugin):
    implements(IPlugin)

    name = 'bit.bot.aiml'

    _handlers = [bot_speaks]

    def load_adapters(self):
        provideAdapter(AIMLPlugin,[IPlugin,],IPluginExtender)        

    def load_utils(self):
        name = getUtility(IConfiguration).get('bot','name')
        ai = BitAI(name.capitalize())
        ai.wake(True)
        provideUtility(ai,IIntelligent)


