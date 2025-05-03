from repository import BookingRepository, BookingModel
from datetime import datetime

class BookingService:
    def __init__(self):
        self.repo = BookingRepository()

    def create_booking(self, guest_name: str, check_in_date: str, check_out_date: str, room_id: str) -> tuple[bool, str]:
        if not guest_name or not check_in_date or not check_out_date or not room_id:
            return False, "Усі поля обов'язкові"
        try:
            check_in = datetime.strptime(check_in_date, '%Y-%m-%d')
            check_out = datetime.strptime(check_out_date, '%Y-%m-%d')
            if check_in >= check_out:
                return False, "Дата виїзду повинна бути пізніше дати заїзду"
            if check_in < datetime.now():
                return False, "Дата заїзду не може бути в минулому"
            room_id = int(room_id)
            booking_id = self.repo.add(guest_name, check_in_date, check_out_date, room_id)
            if booking_id:
                return True, "Бронювання успішно створено"
            return False, "Помилка при створенні бронювання"
        except ValueError:
            return False, "Некоректний формат дати або даних"

    def get_booking(self, booking_id: int) -> BookingModel:
        return self.repo.get_by_id(booking_id)

    def get_all_bookings(self) -> list[BookingModel]:
        return self.repo.get_all()

    def update_booking(self, booking_id: int, guest_name: str, check_in_date: str, check_out_date: str, room_id: str) -> tuple[bool, str]:
        if not guest_name or not check_in_date or not check_out_date or not room_id:
            return False, "Усі поля обов'язкові"
        try:
            check_in = datetime.strptime(check_in_date, '%Y-%m-%d')
            check_out = datetime.strptime(check_out_date, '%Y-%m-%d')
            if check_in >= check_out:
                return False, "Дата виїзду повинна бути пізніше дати заїзду"
            if check_in < datetime.now():
                return False, "Дата заїзду не може бути в минулому"
            room_id = int(room_id)
            success = self.repo.update(booking_id, guest_name, check_in_date, check_out_date, room_id)
            if success:
                return True, "Бронювання успішно оновлено"
            return False, "Помилка при оновленні бронювання"
        except ValueError:
            return False, "Некоректний формат дати або даних"

    def delete_booking(self, booking_id: int) -> tuple[bool, str]:
        success = self.repo.delete(booking_id)
        if success:
            return True, "Бронювання успішно видалено"
        return False, "Помилка при видаленні бронювання"

    def get_rooms(self) -> list[dict]:
        return self.repo.get_all_rooms()