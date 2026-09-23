class Foo(object):
    instance = None

    def __init__(self, name):
        self.name = name

    def __new__(cls, *args, **kwargs):
        if cls.instance:
            return cls.instance
        cls.instance = object.__new__(cls)
        return cls.instance


obj1 = Foo('lisa')
obj2 = Foo('jack')

print(obj1, obj2)
# <__main__.Foo object at 0x0000029CCF1B7350> <__main__.Foo object at 0x0000029CCF1B7350>