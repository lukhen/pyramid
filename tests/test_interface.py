from abc import ABCMeta, abstractmethod, ABC
from interface import Interface, implements, InterfaceMeta
import pytest
import builtins


class TestImplementingClassImplementsMethods:
    def test_1_method(self):
        class Shape(metaclass=InterfaceMeta):
            def width(self):
                ...

        with pytest.raises(TypeError) as excinfo:

            @implements(Shape)
            class Circle:
                ...

            Circle()

    def test_2_methods_single_interface(self):
        class IKlass(metaclass=InterfaceMeta):
            def meth1(self):
                ...

            def meth2(self):
                ...

        class Klass:
            def meth1(self):
                ...

        with pytest.raises(TypeError) as excinfo:

            @implements(IKlass)
            class Klass:
                def meth1(self):
                    ...

            Klass()
        assert "Can't instantiate" in str(excinfo.value)

    def test_2_methods_multiple_interfaces(self):
        class IKlass1(metaclass=InterfaceMeta):
            def meth1(self, x, y):
                ...

        class IKlass2(metaclass=InterfaceMeta):
            def meth2(self, a, b):
                ...

        with pytest.raises(TypeError) as excinfo:

            @implements(IKlass1, IKlass2)
            class Klass:
                def meth1(self, x, y):
                    ...

            Klass()
        assert "Can't instantiate" in str(excinfo.value)


class TestMethodSignatures:
    def test_2_methods_single_interface(self):
        class IKlass(metaclass=InterfaceMeta):
            def meth1(self, x, y):
                ...

            def meth2(self, a, b):
                ...

        with pytest.raises(TypeError) as excinfo:

            @implements(IKlass)
            class Klass:
                def meth1(self, x, y):
                    ...

                def meth1(self, x):
                    ...

            Klass()
        assert "Different signatures" in str(excinfo.value)

    def test_2_methods_multiple_interfaces(self):
        class IKlass1(metaclass=InterfaceMeta):
            def meth1(self, x, y):
                ...

        class IKlass2(metaclass=InterfaceMeta):
            def meth2(self, a, b):
                ...

        with pytest.raises(TypeError) as excinfo:

            @implements(IKlass1, IKlass2)
            class Klass:
                def meth1(self, x, y):
                    ...

                def meth2(self, a):
                    ...

            Klass()
        assert "Different signatures" in str(excinfo.value)


class TestImplementingClassHasCorrectBases:
    def test_no_inheritance_single_interface(self):
        class IKlass(metaclass=InterfaceMeta):
            ...

        @implements(IKlass)
        class Klass:
            ...

        class TestKlass(IKlass):
            ...

        assert Klass.__bases__ == TestKlass.__bases__

    def test_single_inheritance_single_interface(self):
        class IKlass(metaclass=InterfaceMeta):
            ...

        class Base:
            ...

        @implements(IKlass)
        class Klass(Base):
            ...

        class TestKlass(IKlass, Base):
            ...

        assert Klass.__bases__ == TestKlass.__bases__

    def test_multiple_inheritance_multiple_interface(self):
        class IKlass1(metaclass=InterfaceMeta):
            ...

        class IKlass2(metaclass=InterfaceMeta):
            ...

        class Base1:
            ...

        class Base2:
            ...

        @implements(IKlass1, IKlass2)
        class Klass(Base1, Base2):
            ...

        class TestKlass(IKlass1, IKlass2, Base1, Base2):
            ...

        assert Klass.__bases__ == TestKlass.__bases__
