# -*- coding: utf-8 -*-


class Singleton(type):
    """
    Metaclass to implement Singleton Pattern.

    """
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls.instance = None

    def __call__(cls,*args,**kw):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kw)
        return cls.instance


from restructurer import Restructurer

def KanjiIterator(string):
    for s in string:
        if Restructurer.is_kanji(s):
            yield s

