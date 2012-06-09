
from zope.interface import Interface as I


class IQuery(I):

    def search(query):
        pass


class IWho(IQuery):
    pass


class IWhoProvider(I):
    pass


class IWhere(IQuery):
    pass


class IWhat(IQuery):
    pass


class IWhatProvider(I):
    pass


class IWhereProvider(I):
    pass
