import json
import os
import uuid
import datetime
from Src.Domain.Bill.Billing import Bills
from Src.Domain.Booking.Table import TableBooking
class OrderProcessing:
    def __init__(self, menu_path):
        self.menu_path = menu_path
        self.menu = self.load_menu()
        self.order = []
        self.order_file = rf"F:\Restaurant_Management_System\Src\Database\Order.json"


    def load_menu(self):
        if os.path.exists(self.menu_path):
            with open(self.menu_path, 'r') as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    print("Warning: Menu file is corrupted or empty.")
                    return {"Breakfast": [], "Lunch": [], "Dinner": []}
        else:
            print("Menu file not found.")
            return {"Breakfast": [], "Lunch": [], "Dinner": []}

    def display_menu(self):
        print("\n--- Food Menu ---")
        for category, items in self.menu.items():
            print(f"\n{category}:")
            if not items:
                print("  No items available.")
            else:
                print(f"{'ID':<8} | {'Name':<20} | {'Size':<6} | {'Price':<6}")
                print("-" * 50)
                for item in items:
                    print(f"{item['item_id']:<8} | {item['item_name']:<20} | {item['size']:<6} | ₹{item['price']:<6}")


    def add_item(self):
        self.display_menu()
        name = input("\nEnter item name to add: ").strip().lower()
        found = False
        for category in self.menu.values():
            for item in category:
                if item["item_name"].lower() == name:
                    self.order.append(item)
                    print(f"Added: {item['item_name']} ({item['size']})")
                    found = True
                    break
            if found:
                break
        if not found:
            print("Item not found in the menu.")

    def remove_item(self):
        if not self.order:
            print("No items in your order to remove.")
            return

        print("\n--- Current Order ---")
        for i, item in enumerate(self.order, start=1):
            print(f"{i}. {item['item_name']} ({item['size']}) - ₹{item['price']}")

        try:
            index = int(input("Enter item number to remove: "))
            if 1 <= index <= len(self.order):
                removed = self.order.pop(index - 1)
                print(f"Removed: {removed['item_name']}")
            else:
                print("Invalid index.")
        except ValueError:
            print("Please enter a valid number.")


    def finalize_order(self):
        if not self.order:
            print("No items in order.")
            return

        print("\nSelect Order Type:")
        print("1. Pack Order")
        print("2. Table Booking")
        order_type = input("Enter choice (1 or 2): ").strip()

        if order_type == "2":
            
            booking = TableBooking()
            booking.book_table()
        elif order_type != "1":
            print("❌ Invalid choice. Cancelling billing.")
            return

        print("\n--- Final Order ---")
        subtotal = sum(int(item['price']) for item in self.order)

        tax_rate = 0.05
        discount_rate = 0.10 if subtotal >= 500 else 0

        tax = round(subtotal * tax_rate, 2)
        discount = round(subtotal * discount_rate, 2)
        total = round(subtotal + tax - discount, 2)

        print(f"\nSubtotal: ₹{subtotal}")
        print(f"Tax (5%): ₹{tax}")
        if discount_rate > 0:
            print(f"Discount (10%): -₹{discount}")
        print(f"Total Amount: ₹{total}")
        print("Please proceed to payment...")

        order_id = str(uuid.uuid4())[:8]
        order_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        final_order = {
            "order_id": order_id,
            "order_date": order_date,
            "items": self.order,
            "subtotal": subtotal,
            "tax": tax,
            "discount": discount,
            "total_amount": total,
            "order_type": "Pack Order" if order_type == "1" else "Table Booking"
        }

        billing = Bills(rf"F:\Restaurant_Management_System\Src\Database\Bill.json")
        payment_success = billing.generate_invoice(final_order)

        if payment_success:
            self.append_to_file(self.order_file, final_order)
            print("✅ Order saved to Order.json")
            self.order.clear()
        else:
            print("❌ Payment failed or cancelled. Order not saved.")




    def append_to_file(self, filepath, data):
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r') as file:
                    existing = json.load(file)
            else:
                existing = []
        except json.JSONDecodeError:
            existing = []

        existing.append(data)

        with open(filepath, 'w') as file:
            json.dump(existing, file, indent=4)



    def process(self):
        while True:
            print("\nOrder Your Food:")
            print("1. Add Item")
            print("2. Remove Item")
            print("3. Finalize Order")
            print("4. Book a Table")
            print("5. Exit")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.add_item()
            elif choice == "2":
                self.remove_item()
            elif choice == "3":
                self.finalize_order()
            elif choice == "4":
                booking = TableBooking()
                booking.book_table()
            elif choice == "5":
                print("Exiting Order Menu...")
                break
            else:
                print("Invalid choice. Try again.")
