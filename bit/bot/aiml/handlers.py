import json

from zope.component import adapter, getUtility

from twisted.python import log

from bit.bot.common.interfaces import ISubscriptions
from bit.bot.base.events import BotRespondsEvent, PersonSpeaksEvent


@adapter(BotRespondsEvent)
def bot_speaks(evt):
    log.msg('bit.bot.xmpp.handlers: bot_speaks')
    subs = getUtility(ISubscriptions)
    if 'bot-speaks' in subs.subscriptions:
        for subscriber in subs.subscriptions['bot-speaks']:
            subs.subscriptions['bot-speaks'][subscriber](
                json.dumps(dict(
                        emit={'bot-speaks': 'Bot to %s: %s' % (
                                evt.session_id, evt.message)
                              })))


@adapter(PersonSpeaksEvent)
def person_speaks(evt):
    log.msg('bit.bot.xmpp.handlers: person_speaks')
    subs = getUtility(ISubscriptions)
    if 'person-speaks' in subs.subscriptions:
        for subscriber in subs.subscriptions['person-speaks']:
            subs.subscriptions['person-speaks'][subscriber](
                json.dumps(dict(
                        emit={'person-speaks': 'Person to %s: %s' % (
                                evt.session_id, evt.message)
                              })))
# maybe update list of logged in people
#,bit=dict(bot=dict(admin=(dict(sessions=sessions)))))))
