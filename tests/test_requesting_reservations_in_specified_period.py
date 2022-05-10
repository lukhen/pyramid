from tests import EnchantedMock
from app import App, Formatter
from app.model import ReservationsDB
from pyramid.testing import DummyRequest
from datetime import date
from unittest.mock import create_autospec
import unittest


def test_valid_period_reservations_found():
    unittest.mock.MagicMock = EnchantedMock

    ilor = ["reservation 1", "reservation 2"]  # irrelevant list of reservations
    ifor = "reservation 1, reservation 2"  # irrelevant format of the reservations list
    start_date = date(2020, 3, 1)
    end_date = date(2020, 3, 5)
    db = create_autospec(spec=ReservationsDB)
    db.get_reservations_that_start_in_period.when_called_with(
        start_date, end_date
    ).produce((True, ilor, "")).otherwise([])
    formatter = create_autospec(spec=Formatter)
    formatter.reservations_simple_dict_view.when_called_with(ilor).produce(
        (True, ifor, "")
    ).otherwise(None)
    a = App(db, formatter)
    request = DummyRequest()
    request.matchdict["start_date"] = start_date
    request.matchdict["end_date"] = end_date

    response = a.on_request_for_reservations_that_start_in_period(request)

    assert response == ifor
