from app.model import SqlDatabase, Reservation
from tests import CountingReservationsContract
import pytest


class TestCountingReservationsInSqlDatabase(CountingReservationsContract):
    @pytest.fixture(autouse=True)
    def _db(self):
        self._db = SqlDatabase(
            "sqlite:///:memory:", connect_args={"check_same_thread": False}
        )

    def emptyDatabase(self):
        return self._db

    def database_with_1_reservation(self):
        session = self._db.Session()
        session.add(Reservation(PokojID=1))
        session.commit()
        return self._db

    def database_with_1000_reservations(self):
        session = self._db.Session()
        for i in range(1000):
            session.add(Reservation(PokojID=i))
        session.commit()
        return self._db
