from abc import ABCMeta, abstractmethod, ABC
import inspect
import types


class InterfaceMeta(ABCMeta):
    def __new__(cls, name, bases, dct):

        for (member_name, member) in dct.items():
            if isinstance(member, types.FunctionType):
                dct[member_name] = abstractmethod(member)

        X = type(name, (ABC,), dct)
        return X


class Interface(metaclass=ABCMeta):
    ...


def implements(*interfaces):
    def decor(cls):
        bases = [*interfaces, *cls.__bases__]
        if object in bases:
            bases.remove(object)
        X = type(cls.__name__, (*bases,), dict(cls.__dict__))

        def functions_have_same_signature(f1, f2):
            return inspect.signature(f1) == inspect.signature(f2)

        for interface in interfaces:
            common_methods = set(interface.__abstractmethods__).intersection(
                cls.__dict__.keys()
            )

            for method_name in common_methods:
                cls_method = cls.__dict__[method_name]
                interface_method = interface.__dict__[method_name]
                if not functions_have_same_signature(cls_method, interface_method):
                    raise TypeError(
                        "Different signatures: {}.{}{} != {}.{}{}".format(
                            interface,
                            method_name,
                            inspect.signature(interface_method),
                            cls,
                            method_name,
                            inspect.signature(cls_method),
                        )
                    )

        return X

    return decor
