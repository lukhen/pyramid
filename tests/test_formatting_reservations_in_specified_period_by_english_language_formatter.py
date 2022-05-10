from app import EnglishLanguageFormatter
from datetime import date
from app.model import Reservation, Client, Room
import pytest


@pytest.fixture
def formatter():
    return EnglishLanguageFormatter()


def test_0(formatter):
    assert formatter.reservations_simple_dict_view([]) == (True, {}, "")


def test_1(formatter):
    reservation = Reservation(DataOd=date(2020, 3, 5), DataDo=date(2020, 3, 15))
    room = Room(name="1")
    reservation.room = room
    client = Client(Nazwisko="John Smith")
    reservation.client = client

    assert formatter.reservations_simple_dict_view([reservation]) == (
        True,
        {
            "0": {
                "date_from": {"year": 2020, "month": 3, "day": 5},
                "date_to": {"year": 2020, "month": 3, "day": 15},
                "client": "John Smith",
                "room": "1",
            }
        },
        "",
    )


def test_3(formatter):
    room = Room(name="1")
    client = Client(Nazwisko="John Smith")
    reservations = [
        Reservation(DataOd=date(2020, 3, 5), DataDo=date(2020, 3, 15)),
        Reservation(DataOd=date(2020, 4, 5), DataDo=date(2020, 4, 15)),
        Reservation(DataOd=date(2020, 5, 5), DataDo=date(2020, 5, 15)),
    ]
    for reservation in reservations:
        reservation.room = room
        reservation.client = client

    assert formatter.reservations_simple_dict_view(reservations) == (
        True,
        {
            f"{i}": {
                "date_from": {
                    "year": reservation.DataOd.year,
                    "month": reservation.DataOd.month,
                    "day": reservation.DataOd.day,
                },
                "date_to": {
                    "year": reservation.DataDo.year,
                    "month": reservation.DataDo.month,
                    "day": reservation.DataDo.day,
                },
                "client": reservation.client.Nazwisko,
                "room": reservation.room.name,
            }
            for i, reservation in enumerate(reservations)
        },
        "",
    )
