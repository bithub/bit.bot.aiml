
import os
from zope.interface import implements
from zope.component import getUtility,getGlobalSiteManager
from bit.bot.common.interfaces import IPluginFactory, IIntelligent, IConfiguration

from bit.bot.aiml.ai import BitAI

from bit.bot.base.plugin import BitBotPluginBase


class BitBotAIPlugin(BitBotPluginBase):
    implements(IPluginFactory)

    name = 'bit.bot.aiml'

    def load_utils(self):
        name = getUtility(IConfiguration).get('bot','name')
        ai = BitAI(name.capitalize())
        ai.wake(True)
        gsm = getGlobalSiteManager()    
        gsm.registerUtility(ai,IIntelligent)

