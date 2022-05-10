from tests import EnchantedMock
from app import App
from pyramid import testing


def test_regular_request():
    db = EnchantedMock()
    db.get_all_reservations_count.return_value = 100
    fmt = EnchantedMock()
    fmt.format_reservations_count.when_called_with(100).produce(
        {"reservation_count": "100"}
    ).otherwise({})

    a = App(db, fmt)
    request = testing.DummyRequest()

    response = a.on_request_for_all_reservations_count(request)

    assert response == {"reservation_count": "100"}
