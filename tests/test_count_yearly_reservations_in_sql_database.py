from app.model import SqlDatabase, Reservation
from datetime import date


def test_0_reservations_in_2020():
    db = SqlDatabase("sqlite:///:memory:", connect_args={"check_same_thread": False})

    assert db.get_yearly_reservations_count(2020) == 0


def test_1_reservation_in_2020_0_in_other_years():
    db = SqlDatabase("sqlite:///:memory:", connect_args={"check_same_thread": False})
    session = db.Session()
    session.add(
        Reservation(PokojID=1, DataOd=date(2020, 7, 1), DataDo=date(2020, 7, 10))
    )
    session.commit()

    reservation_count_in_2020 = db.get_yearly_reservations_count(2020)

    assert reservation_count_in_2020 == 1


def test_many_reservations_in_2020_0_in_other_years():
    db = SqlDatabase("sqlite:///:memory:", connect_args={"check_same_thread": False})
    session = db.Session()
    for i in range(1000):
        session.add(
            Reservation(PokojID=i, DataOd=date(2020, 7, 1), DataDo=date(2020, 7, 10))
        )
    session.commit()

    reservation_count_in_2020 = db.get_yearly_reservations_count(2020)

    assert reservation_count_in_2020 == 1000


def test_1_reservation_in_2020_1_in_other_year():
    db = SqlDatabase("sqlite:///:memory:", connect_args={"check_same_thread": False})
    session = db.Session()
    session.add(
        Reservation(PokojID=1, DataOd=date(2020, 7, 1), DataDo=date(2020, 7, 10))
    )
    session.add(
        Reservation(PokojID=1, DataOd=date(2019, 7, 1), DataDo=date(2019, 7, 10))
    )
    session.commit()

    reservation_count_in_2020 = db.get_yearly_reservations_count(2020)

    assert reservation_count_in_2020 == 1


def test_many_reservations_in_2020_many_in_other_year():
    db = SqlDatabase("sqlite:///:memory:", connect_args={"check_same_thread": False})
    session = db.Session()
    for i in range(1000):
        session.add(
            Reservation(PokojID=i, DataOd=date(2020, 7, 1), DataDo=date(2020, 7, 10))
        )

    for i in range(900):
        session.add(
            Reservation(PokojID=i, DataOd=date(2019, 7, 1), DataDo=date(2019, 7, 10))
        )

    for i in range(900):
        session.add(
            Reservation(PokojID=i, DataOd=date(2021, 7, 1), DataDo=date(2019, 7, 10))
        )

    session.commit()

    reservation_count_in_2020 = db.get_yearly_reservations_count(2020)

    assert reservation_count_in_2020 == 1000
