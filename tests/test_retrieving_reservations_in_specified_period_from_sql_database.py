from app.model import SqlDatabase, Reservation, Room, Client
from datetime import date
import pytest


@pytest.fixture
def db():
    return SqlDatabase(db_uri="sqlite:///:memory:")


def test_0(db):
    reservations_monad = db.get_reservations_that_start_in_period(
        date(2020, 3, 1), date(2020, 3, 10)
    )

    assert reservations_monad == (True, [], "")


def test_1(db):
    session = db.Session()
    reservation = Reservation(DataOd=date(2020, 3, 5), DataDo=date(2020, 3, 15))
    room = Room(name="1")
    reservation.room = room
    client = Client(Nazwisko="John Smith")
    reservation.client = client
    session.add(reservation)
    session.commit()

    reservations_monad = db.get_reservations_that_start_in_period(
        date(2020, 3, 1), date(2020, 3, 10)
    )

    assert reservations_monad == (True, [reservation], "",)


def test_1_in_period_1_after(db):
    session = db.Session()
    reservation_in = Reservation(DataOd=date(2020, 3, 5), DataDo=date(2020, 3, 15))
    reservation_out = Reservation(DataOd=date(2020, 3, 15), DataDo=date(2020, 3, 20))
    room = Room(name="1")
    reservation_in.room = room
    reservation_out.room = room
    client = Client(Nazwisko="John Smith")
    reservation_in.client = client
    reservation_out.client = client
    session.add(reservation_in)
    session.add(reservation_out)
    session.commit()

    reservations_monad = db.get_reservations_that_start_in_period(
        date(2020, 3, 1), date(2020, 3, 10)
    )

    assert reservations_monad == (True, [reservation_in], "",)


def test_1_in_period_1_before(db):
    session = db.Session()
    reservation_in = Reservation(DataOd=date(2020, 3, 5), DataDo=date(2020, 3, 15))
    reservation_before = Reservation(DataOd=date(2020, 2, 27), DataDo=date(2020, 3, 2))
    room = Room(name="1")
    reservation_in.room = room
    reservation_before.room = room
    client = Client(Nazwisko="John Smith")
    reservation_in.client = client
    reservation_before.client = client
    session.add(reservation_in)
    session.add(reservation_before)
    session.commit()

    reservations_monad = db.get_reservations_that_start_in_period(
        date(2020, 3, 1), date(2020, 3, 10)
    )

    assert reservations_monad == (True, [reservation_in], "",)


def test_2_reservations_on_edges(db):
    session = db.Session()
    reservation_before = Reservation(DataOd=date(2020, 2, 27), DataDo=date(2020, 3, 2))
    reservation_at_start_edge = Reservation(
        DataOd=date(2020, 3, 1), DataDo=date(2020, 3, 2)
    )
    reservation_in = Reservation(DataOd=date(2020, 3, 5), DataDo=date(2020, 3, 15))
    reservation_at_end_edge = Reservation(
        DataOd=date(2020, 3, 10), DataDo=date(2020, 3, 12)
    )
    reservation_after = Reservation(DataOd=date(2020, 3, 15), DataDo=date(2020, 3, 20))
    reservations = [
        reservation_before,
        reservation_at_start_edge,
        reservation_in,
        reservation_at_end_edge,
        reservation_after,
    ]

    for reservation in reservations:
        room = Room(name="1")
        reservation.room = room
        client = Client(Nazwisko="John Smith")
        reservation.client = client
        session.add(reservation)
    session.commit()

    reservations_monad = db.get_reservations_that_start_in_period(
        date(2020, 3, 1), date(2020, 3, 10)
    )

    assert reservations_monad[0] is True
    assert reservation_before not in reservations_monad[1]
    assert reservation_at_start_edge in reservations_monad[1]
    assert reservation_in in reservations_monad[1]
    assert reservation_at_end_edge in reservations_monad[1]
    assert reservation_after not in reservations_monad[1]


def test_start_date_older_than_end_date(db):
    reservations_monad = db.get_reservations_that_start_in_period(
        date(2020, 3, 5), date(2020, 3, 1)
    )

    assert reservations_monad == (False, [], "Start date can't be older than end date.")


def test_exception(db):
    reservations_monad = db.get_reservations_that_start_in_period(
        date(2020, 3, 5), "bad date"
    )

    assert reservations_monad[0] is False
