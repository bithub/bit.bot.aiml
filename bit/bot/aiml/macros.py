from zope.interface import implements
from zope.component import getUtility

from twisted.internet import defer

from bit.bot.common.interfaces import IMembers, ISessions

from bit.aiml.async.macros import BotAIMacro
from bit.aiml.async.interfaces import IAIMLMacro

from bit.bot.aiml.interfaces import IWho, IWhat, IWhere


class WhoIs(BotAIMacro):
    implements(IAIMLMacro)

    def parse(self, kernel, elem):
        query = kernel._processElement(['star',{}], self.request)
        return getUtility(IWho).search(self.request, query)


class WhatIs(BotAIMacro):
    implements(IAIMLMacro)

    def parse(self, kernel, elem):
        query = kernel._processElement(['star',{}], self.request)
        return getUtility(IWhat).search(self.request, query)


class WhereIs(BotAIMacro):
    implements(IAIMLMacro)

    def parse(self, kernel, elem):
        query = kernel._processElement(['star',{}], self.request)
        return getUtility(IWhere).search(self.request, query)
