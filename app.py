from flask import Flask, render_template, request, redirect, url_for, flash
from services import BookingService

app = Flask(__name__)
app.secret_key = 'your_secret_key'
service = BookingService()

@app.route('/')
def index():
    bookings = service.get_all_bookings()
    return render_template('index.html', bookings=bookings)

@app.route('/booking/<int:booking_id>')
def view_booking(booking_id):
    booking = service.get_booking(booking_id)
    if booking:
        return render_template('booking.html', booking=booking, mode='view')
    flash('Бронювання не знайдено', 'error')
    return redirect(url_for('index'))

@app.route('/booking/new', methods=['GET', 'POST'])
def create_booking():
    if request.method == 'POST':
        guest_name = request.form['guest_name']
        check_in_date = request.form['check_in_date']
        check_out_date = request.form['check_out_date']
        room_id = request.form['room_id']
        success, message = service.create_booking(guest_name, check_in_date, check_out_date, room_id)
        flash(message, 'success' if success else 'error')
        if success:
            return redirect(url_for('index'))
    rooms = service.get_rooms()
    return render_template('booking.html', booking=None, rooms=rooms, mode='create')

@app.route('/booking/edit/<int:booking_id>', methods=['GET', 'POST'])
def edit_booking(booking_id):
    booking = service.get_booking(booking_id)
    if not booking:
        flash('Бронювання не знайдено', 'error')
        return redirect(url_for('index'))
    if request.method == 'POST':
        guest_name = request.form['guest_name']
        check_in_date = request.form['check_in_date']
        check_out_date = request.form['check_out_date']
        room_id = request.form['room_id']
        success, message = service.update_booking(booking_id, guest_name, check_in_date, check_out_date, room_id)
        flash(message, 'success' if success else 'error')
        if success:
            return redirect(url_for('index'))
    rooms = service.get_rooms()
    return render_template('booking.html', booking=booking, rooms=rooms, mode='edit')

@app.route('/booking/delete/<int:booking_id>')
def delete_booking(booking_id):
    success, message = service.delete_booking(booking_id)
    flash(message, 'success' if success else 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)