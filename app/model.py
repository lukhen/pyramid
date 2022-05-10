from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Date, ForeignKey, VARCHAR
from sqlalchemy import create_engine, extract
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.pool import StaticPool
from interface import Interface, implements, InterfaceMeta
from abc import abstractmethod
import datetime

Base = declarative_base()


class ReservationsDB(metaclass=InterfaceMeta):
    def get_all_reservations_count(self):
        ...

    def get_yearly_reservations_count(self, year):
        ...

    def get_reservations_that_start_in_period(self, start_date, end_date):
        ...


@implements(ReservationsDB)
class SqlDatabase:
    def __init__(self, db_uri, connect_args={}, engine=None):
        # SMELL
        if db_uri == "sqlite:///:memory:":
            self.engine = create_engine(
                db_uri, connect_args={"check_same_thread": False}, poolclass=StaticPool
            )
        else:
            self.engine = create_engine(db_uri)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def get_all_reservations_count(self):
        session = self.Session()
        return len(session.query(Reservation).all())

    def get_yearly_reservations_count(self, year):
        session = self.Session()
        return len(
            session.query(Reservation)
            .filter(extract("year", Reservation.DataOd) == year)
            .all()
        )

    def get_reservations_that_start_in_period(self, start_date, end_date):
        try:
            if start_date > end_date:
                return (False, [], "Start date can't be older than end date.")
            session = self.Session()
            reservations = (
                session.query(Reservation)
                .filter(Reservation.DataOd >= start_date)
                .filter(Reservation.DataOd <= end_date)
            ).all()
            return (True, reservations, "")
        except Exception as e:
            return (False, [], str(e))

    def fill_with_dummy_data(self):
        session = self.Session()
        names = ["John Smith", "Albert Einstein", "Alan Turing", "Rick Deckard"]
        clients = [Client(Nazwisko=name) for name in names]
        rooms = [
            Room(name="P01"),
            Room(name="P02"),
            Room(name="P03"),
            Room(name="P04"),
        ]
        reservations = [
            Reservation(
                DataOd=datetime.date(2020, 3, 10), DataDo=datetime.date(2020, 3, 15)
            ),
            Reservation(
                DataOd=datetime.date(2020, 4, 10), DataDo=datetime.date(2020, 4, 15)
            ),
            Reservation(
                DataOd=datetime.date(2020, 5, 10), DataDo=datetime.date(2020, 5, 15)
            ),
            Reservation(
                DataOd=datetime.date(2020, 6, 10), DataDo=datetime.date(2020, 6, 15)
            ),
        ]
        for reservation in reservations:
            reservation.client = clients.pop()
            reservation.room = rooms.pop()

        session.add_all(reservations)
        session.commit()


class Reservation(Base):
    __tablename__ = "Rezerwacje"

    RezerwacjaID = Column(Integer, primary_key=True)
    PokojID = Column(Integer, ForeignKey("rooms.id"))
    KlientID = Column(Integer, ForeignKey("Klienci.KlientID"))
    DataOd = Column(Date)
    DataDo = Column(Date)
    room = relationship("Room")
    client = relationship("Client")

    def __eq__(self, other):
        return self.RezerwacjaID == other.RezerwacjaID

    def __repr__(self):
        return f"<Reservation: {self.RezerwacjaID}>"


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(length=150), nullable=False)


class Client(Base):
    __tablename__ = "Klienci"

    KlientID = Column(Integer, primary_key=True)
    Nazwisko = Column(VARCHAR(length=255), nullable=True)
