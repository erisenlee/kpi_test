from collections import namedtuple
# from functools import wraps


class Indicator:
    def __init__(self, name, expected_type):
        self.name = name
        self.expected_type = expected_type
    def __get__(self, instance,cls):
        if instance is None:
            return self
        return instance.__dict__[self.name]
    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError('unexpected type')
        instance.__dict__[self.name]=value

#class decorator 
def typecheck(**kwargs):
    def decorate(cls):
        for key, expected_type in kwargs.items():
            setattr(cls, key, Indicator(key, expected_type))
        return cls
    return decorate


# @typecheck(name=str,count=int)
# class Basic:
#     def __init__(self, name, count):
#         self.name = name
#         self.count=count

def get_nametuple(name, *args,**kwargs):
    if not isinstance(name, str):
        raise TypeError('argument {} is not str'.format(name))
    if not args and not kwargs:
        raise ValueError('no fields')
    if kwargs:
        Name = namedtuple(name.capitalize(), kwargs.keys())
        return Name._make(kwargs.values())
    return namedtuple(name.capitalize(),list(args))


    



if __name__ == '__main__':
    ss = get_nametuple('Ss', a=1,b=2)

    print(ss)
    
    