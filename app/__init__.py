from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.request import Request
from pyramid.static import static_view
import os
from app.model import SqlDatabase
from abc import abstractmethod, ABC
from interface import InterfaceMeta, implements


class Formatter(metaclass=InterfaceMeta):
    def format_reservations_count(self, reservation_count):
        ...

    def reservations_simple_dict_view(self, reservations):
        ...


@implements(Formatter)
class EnglishLanguageFormatter:
    def format_reservations_count(self, reservation_count):
        return {"reservation_count": "{}".format(reservation_count)}

    def reservations_simple_dict_view(self, reservations):
        return (
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


class App:
    def __init__(self, db, formatter):
        self.db = db
        self.formatter = formatter

    def on_request_for_all_reservations_count(self, request):
        request.response.headers.update({"Access-Control-Allow-Origin": "*"})
        return self.formatter.format_reservations_count(
            self.db.get_all_reservations_count()
        )

    def on_request_for_yearly_reservations_count(self, request):
        request.response.headers.update({"Access-Control-Allow-Origin": "*"})
        return self.formatter.format_reservations_count(
            self.db.get_yearly_reservations_count(request.matchdict["year"])
        )

    def on_request_for_reservations_that_start_in_period(self, request):
        request.response.headers.update({"Access-Control-Allow-Origin": "*"})
        data_monad = self.db.get_reservations_that_start_in_period(
            request.matchdict["start_date"], request.matchdict["end_date"]
        )
        format_monad = self.formatter.reservations_simple_dict_view(data_monad[1])
        return format_monad[1]


def main(global_config, **settings):
    config = Configurator(settings=settings)

    db = SqlDatabase(os.environ.get("DB_URI"))
    if os.environ.get("DB_URI") == "sqlite:///:memory:":
        db.fill_with_dummy_data()

    a = App(db, EnglishLanguageFormatter())

    config.add_route("allrescount", "/allrescount")
    config.add_route("rescountinyear", "/countreservations/{year}")
    config.add_route("resinperiod", "/resinperiod/{start_date}/{end_date}")
    config.add_view(
        a.on_request_for_reservations_that_start_in_period,
        route_name="resinperiod",
        renderer="json",
    )

    config.add_view(
        a.on_request_for_all_reservations_count,
        route_name="allrescount",
        renderer="json",
    )
    config.add_view(
        a.on_request_for_yearly_reservations_count,
        route_name="rescountinyear",
        renderer="json",
    )
    config.add_route("images", "/images/*subpath")
    images_view = static_view("./images", use_subpath=True)
    config.add_view(images_view, route_name="images")
    return config.make_wsgi_app()
