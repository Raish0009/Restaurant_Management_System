import json
import os
import uuid
from datetime import datetime, timedelta

class TableBooking:
    def __init__(self):
        self.database_dir = rf"F:\Restaurant_Management_System\Src\Database"
        os.makedirs(self.database_dir, exist_ok=True)

        self.booking_file = os.path.join(self.database_dir, "Table.json")
        self.tables_config_file = os.path.join(self.database_dir, "tables_config.json")

        self.tables_data = self._load_json_file(self.tables_config_file, "table configuration")
        self.table_bookings = self._load_json_file(self.booking_file, "booking data")

    def _load_json_file(self, file_path: str, file_description: str, default_value=None):
        if default_value is None:
            default_value = []
        if not os.path.exists(file_path):
            print(f"ℹ️ {file_description.capitalize()} file '{file_path}' not found. Initializing with default.")
            return default_value
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            print(f"⚠️ Error decoding JSON from {file_path} ({file_description}). Using default.")
            return default_value
        except Exception as e:
            print(f"⚠️ An unexpected error occurred while loading {file_path}: {e}. Using default.")
            return default_value

    def save_bookings(self):
        try:
            with open(self.booking_file, 'w') as file:
                json.dump(self.table_bookings, file, indent=4, default=str)
        except IOError as e:
            print(f"❌ Error saving bookings to {self.booking_file}: {e}")


    def _prompt_user_for_choice(self, prompt_message: str, options: list, item_display_func=None):
        if not options:
            return None

        print(f"\n{prompt_message}:")
        if item_display_func is None:
            item_display_func = lambda item: str(item)

        for idx, option_item in enumerate(options, 1):
            print(f"{idx}. {item_display_func(option_item)}")

        while True:
            try:
                choice_str = input(f"Choose an option (1-{len(options)}) or press Enter to cancel: ")
                if not choice_str:
                    print("ℹ️ Selection cancelled.")
                    return None
                choice_idx = int(choice_str) - 1
                if 0 <= choice_idx < len(options):
                    return options[choice_idx]
                else:
                    print(f"❌ Invalid choice. Please enter a number between 1 and {len(options)}.")
            except ValueError:
                print("❌ Invalid input. Please enter a number.")

    def _get_integer_input(self, prompt: str, min_value=None, max_value=None) -> int | None:
        while True:
            try:
                val_str = input(f"{prompt}: ")
                if not val_str and min_value is None :
                    return None
                val_int = int(val_str)

                valid = True
                if min_value is not None and val_int < min_value:
                    valid = False
                if max_value is not None and val_int > max_value:
                    valid = False
                
                if valid:
                    return val_int
                else:
                    range_msg = ""
                    if min_value is not None and max_value is not None:
                        range_msg = f" between {min_value} and {max_value}"
                    elif min_value is not None:
                        range_msg = f" no less than {min_value}"
                    elif max_value is not None:
                        range_msg = f" no more than {max_value}"
                    print(f"❌ Number out of range. Please enter a number{range_msg}.")

            except ValueError:
                print("❌ Invalid input. Please enter a whole number.")


    def generate_time_slots_for_today(self, interval_hours=2):
        start_of_day_service = datetime.strptime("10:00", "%H:%M").time()
        end_of_day_service = datetime.strptime("22:00", "%H:%M").time()
        now = datetime.now()
        today_date = now.date()

        current_slot_start_time = datetime.combine(today_date, start_of_day_service)
        service_end_datetime = datetime.combine(today_date, end_of_day_service)
        slots = []

        while current_slot_start_time < service_end_datetime:
            slot_end_time = current_slot_start_time + timedelta(hours=interval_hours)
            if slot_end_time > service_end_datetime:
                slot_end_time = service_end_datetime

            if now < slot_end_time:
                slot_str = f"{current_slot_start_time.strftime('%H:%M')} - {slot_end_time.strftime('%H:%M')}"
                slots.append(slot_str)

            current_slot_start_time = slot_end_time
            if current_slot_start_time >= service_end_datetime :
                break
        return slots

    def get_table_status_for_slot(self, date_str: str, time_slot_str: str):
        if not self.tables_data:
            print("⚠️ No table configurations loaded. Cannot determine table status.")
            return []

        tables_status_list = []
        for table_config in self.tables_data:
            is_booked = any(
                booking['date'] == date_str and
                booking['time_slot'] == time_slot_str and
                booking.get('table_no') == table_config['table_no']
                for booking in self.table_bookings
            )
            tables_status_list.append({
                "table_no": table_config['table_no'],
                "total_seats": table_config['total_seats'],
                "status": "Booked" if is_booked else "Available",
                "available_seats_in_slot": 0 if is_booked else table_config['total_seats']
            })
        return tables_status_list

    def display_current_table_status(self):
        self.remove_expired_bookings()
        today_str = str(datetime.now().date())
        print(f"\n--- Table Status for {today_str} ---")

        available_slots_today = self.generate_time_slots_for_today()
        if not available_slots_today:
            print("⚠️ No time slots available for viewing status for the rest of today.")
            return

        selected_slot = self._prompt_user_for_choice(
            "Available Time Slots for Viewing Status",
            available_slots_today
        )
        if not selected_slot:
            return

        print(f"\n--- Status for Tables at {selected_slot} on {today_str} ---")
        table_statuses = self.get_table_status_for_slot(today_str, selected_slot)

        if not table_statuses:
            print("No tables defined or could not fetch status.")
            return

        print(f"{'Table No.':<10} | {'Total Seats':<12} | {'Status':<10} | {'Seats Avail. (Slot)':<20}")
        print("-" * 65)
        for table_info in table_statuses:
            print(
                f"{table_info['table_no']:<10} | "
                f"{table_info['total_seats']:<12} | "
                f"{table_info['status']:<10} | "
                f"{table_info['available_seats_in_slot']:<20}"
            )
        print("-" * 65)

    def book_table(self):
        self.remove_expired_bookings()
        today_str = str(datetime.now().date())
        print(f"\n--- Table Booking for {today_str} ---")

        all_possible_slots_today = self.generate_time_slots_for_today()
        if not all_possible_slots_today:
            print("⚠️ No time slots available for booking for the rest of today.")
            return

        selected_slot = self._prompt_user_for_choice(
            "Available Time Slots for Booking",
            all_possible_slots_today
        )
        if not selected_slot:
            return

        tables_in_selected_slot_status = self.get_table_status_for_slot(today_str, selected_slot)
        available_tables_for_booking = [
            t for t in tables_in_selected_slot_status if t['status'] == 'Available'
        ]

        if not available_tables_for_booking:
            print(f"😢 Sorry, no tables are available for the slot: {selected_slot}.")
            return

        def display_table_option(table_info):
            return f"Table No. {table_info['table_no']:<5} (Seats: {table_info['total_seats']})"

        chosen_table_info = self._prompt_user_for_choice(
            f"Available Tables for Slot: {selected_slot}",
            available_tables_for_booking,
            item_display_func=display_table_option
        )
        if not chosen_table_info:
            return

        selected_table_no = chosen_table_info['table_no']
        selected_table_total_seats = chosen_table_info['total_seats']

        num_seats_to_book = self._get_integer_input(
            f"How many seats for Table {selected_table_no} (1-{selected_table_total_seats})?",
            min_value=1,
            max_value=selected_table_total_seats
        )
        if num_seats_to_book is None:
            print("❌ Booking cancelled or invalid number of seats entered.")
            return

        booking_id = str(uuid.uuid4())[:6]
        booking = {
            "booking_id": booking_id, "date": today_str, "time_slot": selected_slot,
            "table_no": selected_table_no, "seats_booked": num_seats_to_book,
            "created_at": datetime.now().isoformat()
        }

        self.table_bookings.append(booking)
        self.save_bookings()
        print(f"\n✅ Table {selected_table_no} booked for {num_seats_to_book} seat(s) on {today_str} at {selected_slot}. Booking ID: {booking_id}")

    def remove_expired_bookings(self):
        now = datetime.now()
        updated_bookings = []
        changed = False

        for booking in self.table_bookings:
            try:
                booking_date_str = booking["date"]
                slot_end_str = booking["time_slot"].split(' - ')[1]
                slot_end_datetime = datetime.strptime(f"{booking_date_str} {slot_end_str}", "%Y-%m-%d %H:%M")

                if now < slot_end_datetime:
                    updated_bookings.append(booking)
                else:
                    changed = True
            except (KeyError, IndexError, ValueError) as e:
                print(f"⚠️ Skipping potentially malformed booking during expiration check: {booking}. Error: {e}")
                updated_bookings.append(booking)

        if changed:
            self.table_bookings = updated_bookings
            self.save_bookings()
            print("🧹 Expired bookings removed based on slot end times.")

if __name__ == "__main__":
    booking_system = TableBooking()

    if not booking_system.tables_data:
        print("\n‼️ CRITICAL: Table configuration ('tables_config.json') is missing or empty.")
        print("‼️ Please create this file in the database directory with table definitions.")
        print("‼️ Example entry: [{\"table_no\": 1, \"total_seats\": 4}]")

    while True:
        print("\nRestaurant Table Booking System")
        print("1. Book a Table")
        print("2. View Current Table Status")
        print("3. View All Bookings (Debug)")
        print("4. Manually Remove Expired Bookings")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            if not booking_system.tables_data:
                print("❌ Cannot book: No tables configured. Check 'tables_config.json'.")
            else:
                booking_system.book_table()
        elif choice == '2':
            if not booking_system.tables_data:
                print("❌ Cannot show status: No tables configured. Check 'tables_config.json'.")
            else:
                booking_system.display_current_table_status()
        elif choice == '3':
            print("\n--- All Current Bookings ---")
            if booking_system.table_bookings:
                for b_idx, b in enumerate(booking_system.table_bookings, 1):
                    print(f"--- Booking {b_idx} ---")
                    print(json.dumps(b, indent=2))
            else:
                print("No bookings found.")
        elif choice == '4':
            booking_system.remove_expired_bookings()
        elif choice == '5':
            print("Exiting system. Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")