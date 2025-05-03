from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dataclasses import dataclass
from init_db import Room, Booking, Base
from datetime import datetime

@dataclass
class BookingModel:
    id: int
    guest_name: str
    check_in_date: str
    check_out_date: str
    room_id: int
    room_number: str = None
    room_type: str = None

class BookingRepository:
    def __init__(self):
        self.engine = create_engine('sqlite:///hotel.db')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add(self, guest_name: str, check_in_date: str, check_out_date: str, room_id: int) -> int:
        session = self.Session()
        try:
            booking = Booking(
                guest_name=guest_name,
                check_in_date=check_in_date,
                check_out_date=check_out_date,
                room_id=room_id
            )
            session.add(booking)
            session.commit()
            return booking.id
        except:
            session.rollback()
            return None
        finally:
            session.close()

    def get_by_id(self, booking_id: int) -> BookingModel:
        session = self.Session()
        try:
            booking = session.query(Booking).join(Room).filter(Booking.id == booking_id).first()
            if booking:
                return BookingModel(
                    id=booking.id,
                    guest_name=booking.guest_name,
                    check_in_date=booking.check_in_date,
                    check_out_date=booking.check_out_date,
                    room_id=booking.room_id,
                    room_number=booking.room.room_number,
                    room_type=booking.room.room_type
                )
            return None
        finally:
            session.close()

    def get_all(self) -> list[BookingModel]:
        session = self.Session()
        try:
            bookings = session.query(Booking).join(Room).all()
            return [BookingModel(
                id=b.id,
                guest_name=b.guest_name,
                check_in_date=b.check_in_date,
                check_out_date=b.check_out_date,
                room_id=b.room_id,
                room_number=b.room.room_number,
                room_type=b.room.room_type
            ) for b in bookings]
        finally:
            session.close()

    def update(self, booking_id: int, guest_name: str, check_in_date: str, check_out_date: str, room_id: int) -> bool:
        session = self.Session()
        try:
            booking = session.query(Booking).filter(Booking.id == booking_id).first()
            if booking:
                booking.guest_name = guest_name
                booking.check_in_date = check_in_date
                booking.check_out_date = check_out_date
                booking.room_id = room_id
                session.commit()
                return True
            return False
        except:
            session.rollback()
            return False
        finally:
            session.close()

    def delete(self, booking_id: int) -> bool:
        session = self.Session()
        try:
            booking = session.query(Booking).filter(Booking.id == booking_id).first()
            if booking:
                session.delete(booking)
                session.commit()
                return True
            return False
        except:
            session.rollback()
            return False
        finally:
            session.close()

    def get_all_rooms(self) -> list[dict]:
        session = self.Session()
        try:
            rooms = session.query(Room).all()
            return [{"id": r.id, "room_number": r.room_number, "room_type": r.room_type} for r in rooms]
        finally:
            session.close()