import datetime
import uuid
import json
import os

class Bills:
    def __init__(self, bill_path):
        self.bill_path = bill_path

    def choose_payment_method(self):
        print("\nChoose Payment Method:")
        print("1. Cash")
        print("2. UPI")
        print("3. Credit Card")
        print("4. Debit Card")
        methods = {
            "1": "Cash",
            "2": "UPI",
            "3": "Credit Card",
            "4": "Debit Card"
        }
        choice = input("Enter your choice: ").strip()
        return methods.get(choice, "Cash")

    def generate_invoice(self, order_details):
        print("\n--- Invoice ---")
        print(f"Bill ID: {str(uuid.uuid4())[:8]}")
        print(f"Order ID: {order_details['order_id']}")
        print(f"Date: {order_details['order_date']}")
        print("-" * 60)
        print(f"{'Item Name':<20} {'Size':<10} {'Price (₹)':<10}")
        print("-" * 60)
        for item in order_details['items']:
            print(f"{item['item_name']:<20} {item['size']:<10} ₹{item['price']:<10}")
        print("-" * 60)
        print(f"{'Subtotal':<30} ₹{order_details['subtotal']}")
        print(f"{'Tax (5%)':<30} ₹{order_details['tax']}")
        if order_details['discount'] > 0:
            print(f"{'Discount (10%)':<30} -₹{order_details['discount']}")
        print(f"{'Total Amount':<30} ₹{order_details['total_amount']}")
        print("-" * 60)

        payment_method = self.choose_payment_method()
        print(f"Payment Method: {payment_method}")

        confirm = input("Confirm payment? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("Payment cancelled.")
            return False

        print("Payment successful ✅")
        print("Thank you for dining with us!\n")

        invoice = {
            "invoice_id": str(uuid.uuid4())[:8],
            "order_id": order_details['order_id'],
            "date": order_details['order_date'],
            "items": order_details['items'],
            "subtotal": order_details['subtotal'],
            "tax": order_details['tax'],
            "discount": order_details['discount'],
            "total_amount": order_details['total_amount'],
            "payment_method": payment_method
        }

        self.save_invoice(invoice)
        return True


    def save_invoice(self, invoice):
        try:
            if os.path.exists(self.bill_path):
                with open(self.bill_path, 'r') as file:
                    existing = json.load(file)
            else:
                existing = []
        except json.JSONDecodeError:
            existing = []

        existing.append(invoice)
        with open(self.bill_path, 'w') as file:
            json.dump(existing, file, indent=4)
