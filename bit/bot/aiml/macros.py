from zope.interface import implements
from zope.component import getUtility

from twisted.internet import defer

from bit.bot.common.interfaces import IMembers, ISessions

from bit.aiml.async.macros import BotAIMacro
from bit.aiml.async.interfaces import IAIMLMacro

from bit.bot.aiml.interfaces import IWho, IWhat, IWhere


class WhoIs(BotAIMacro):
    implements(IAIMLMacro)

    def parse(self, elem):
        return getUtility(IWho).search(self.request, self.star)


class WhatIs(BotAIMacro):
    implements(IAIMLMacro)

    def parse(self, elem):
        return getUtility(IWhat).search(self.request, self.star)


class WhereIs(BotAIMacro):
    implements(IAIMLMacro)

    def parse(self, elem):
        return getUtility(IWhere).search(self.request, self.star)
