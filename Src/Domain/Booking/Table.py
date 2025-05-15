import json
import os
import uuid
from datetime import datetime, timedelta

class TableBooking:
    def __init__(self):
        self.booking_file = rf"F:\Restaurant_Management_System\Src\Database\Table.json"
        self.table_bookings = []
        self.load_bookings()

    def load_bookings(self):
        if os.path.exists(self.booking_file):
            with open(self.booking_file, 'r') as file:
                try:
                    self.table_bookings = json.load(file)
                except json.JSONDecodeError:
                    self.table_bookings = []

    def save_bookings(self):
        with open(self.booking_file, 'w') as file:
            json.dump(self.table_bookings, file, indent=4, default=str)

    def generate_time_slots_for_today(self):
        start_time = datetime.strptime("10:00", "%H:%M")
        end_time = datetime.strptime("22:00", "%H:%M")
        now = datetime.now()
        today = now.date()

        slots = []
        while start_time < end_time:
            end_slot = start_time + timedelta(hours=2)
            slot_str = f"{start_time.strftime('%H:%M')} - {end_slot.strftime('%H:%M')}"


            if now.time() < start_time.time():
                slots.append(slot_str)

            start_time = end_slot

        return slots

    def book_table(self):
        self.remove_expired_bookings()

        today = datetime.now().date()
        print(f"\n--- Table Booking for {today} ---")

        slots = self.generate_time_slots_for_today()


        booked_slots = [
            booking['time_slot'] for booking in self.table_bookings
            if booking['date'] == str(today)
        ]
        available_slots = [slot for slot in slots if slot not in booked_slots]

        if not available_slots:
            print("⚠️ No available time slots for the rest of today.")
            return

        print("\nAvailable Time Slots:")
        for idx, slot in enumerate(available_slots, 1):
            print(f"{idx}. {slot}")

        try:
            choice = int(input("Choose a time slot: "))
            if choice < 1 or choice > len(available_slots):
                raise ValueError
        except ValueError:
            print("❌ Invalid choice.")
            return

        selected_slot = available_slots[choice - 1]
        booking_id = str(uuid.uuid4())[:6]

        booking = {
            "booking_id": booking_id,
            "date": str(today),
            "time_slot": selected_slot,
            "created_at": datetime.now().isoformat()
        }

        self.table_bookings.append(booking)
        self.save_bookings()
        print(f"✅ Table booked today at {selected_slot}. Booking ID: {booking_id}")

    def remove_expired_bookings(self):
        current_time = datetime.now()
        updated_bookings = []

        for booking in self.table_bookings:
            created_at = datetime.fromisoformat(booking["created_at"])
            if current_time < created_at + timedelta(hours=2):
                updated_bookings.append(booking)

        if len(updated_bookings) != len(self.table_bookings):
            self.table_bookings = updated_bookings
            self.save_bookings()
            print("🧹 Expired bookings removed.")

# Run the booking
if __name__ == "__main__":
    tb = TableBooking()
    tb.book_table()
