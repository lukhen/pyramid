from app import App
from pyramid import testing
from tests import EnchantedMock


def test_regular_request():
    db = EnchantedMock()
    db.get_yearly_reservations_count.when_called_with(2020).produce(200).otherwise(0)
    fmt = EnchantedMock()
    fmt.format_reservations_count.when_called_with(200).produce(
        {"reservation_count": "200"}
    ).otherwise({})
    a = App(db, fmt)
    request = testing.DummyRequest()
    request.matchdict["year"] = 2020

    response = a.on_request_for_yearly_reservations_count(request)

    assert response == {"reservation_count": "200"}
