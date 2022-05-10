from app import EnglishLanguageFormatter


def test_0():
    f = EnglishLanguageFormatter()
    assert f.format_reservations_count(0) == {"reservation_count": "0"}


def test_100():
    f = EnglishLanguageFormatter()
    assert f.format_reservations_count(100) == {"reservation_count": "100"}
