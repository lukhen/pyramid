from abc import ABC, abstractmethod
from unittest.mock import MagicMock


class CountingReservationsContract(ABC):
    @abstractmethod
    def emptyDatabase(self):
        ...

    @abstractmethod
    def database_with_1_reservation(self):
        ...

    @abstractmethod
    def database_with_1000_reservations(self):
        ...

    def test_0(self):
        db = self.emptyDatabase()

        assert db.get_all_reservations_count() == 0

    def test_1(self):
        db = self.database_with_1_reservation()

        assert db.get_all_reservations_count() == 1

    def test_many(self):
        db = self.database_with_1000_reservations()

        assert db.get_all_reservations_count() == 1000


class EnchantedMock(MagicMock):
    def when_called_with(self, *args, **kwargs):
        self.call_args_2 = args
        self.call_kwargs_2 = kwargs
        return self

    def produce(self, product):
        self.product = product
        return self

    def otherwise(self, other):
        def side_effect(*args, **kwargs):
            if args == self.call_args_2 and kwargs == self.call_kwargs_2:
                return self.product
            else:
                return other

        self.side_effect = side_effect
