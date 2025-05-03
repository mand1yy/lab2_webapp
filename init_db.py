from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class Room(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)
    room_number = Column(String, nullable=False)
    room_type = Column(String, nullable=False)
    bookings = relationship("Booking", back_populates="room")

class Booking(Base):
    __tablename__ = 'bookings'
    id = Column(Integer, primary_key=True)
    guest_name = Column(String, nullable=False)
    check_in_date = Column(String, nullable=False)
    check_out_date = Column(String, nullable=False)
    room_id = Column(Integer, ForeignKey('rooms.id'), nullable=False)
    room = relationship("Room", back_populates="bookings")

def init_db():
    engine = create_engine('sqlite:///hotel.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    # Додавання номерів
    if session.query(Room).count() == 0:
        rooms = [
            Room(room_number="101", room_type="Single"),
            Room(room_number="202", room_type="Double"),
            Room(room_number="303", room_type="Suite")
        ]
        session.add_all(rooms)
        session.commit()
    session.close()

if __name__ == '__main__':
    init_db()