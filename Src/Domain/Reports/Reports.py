import json
import os
from datetime import datetime, timedelta

class ReportGenerator:

    def __init__(self):
        self.order_file = rf"F:\Restaurant_Management_System\Src\Database\order.json"
        self.orders = self.load_orders()

    def load_orders(self):
        if not os.path.exists(self.order_file):
            print("Order file not found.")
            return []

        with open(self.order_file, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print("Error: Invalid JSON format in order file.")
                return []

    def generate(self):
        while True:
            print("\n--- Generate Order Report ---")
            print("1. Daily Report")
            print("2. Weekly Report")
            print("3. Monthly Report")
            print("4. Yearly Report")
            print("5. Exit")

            choice = input("Select an option: ").strip()

            if choice == "1":
                self.filter_and_display("daily")
            elif choice == "2":
                self.filter_and_display("weekly")
            elif choice == "3":
                self.filter_and_display("monthly")
            elif choice == "4":
                self.filter_and_display("yearly")
            elif choice == "5":
                print("Exiting Report Generator...")
                break
            else:
                print("Invalid choice. Please try again.")

    def filter_and_display(self, period):
        now = datetime.now()
        filtered_orders = []

        for order in self.orders:
            try:
                order_date = datetime.strptime(order.get("order_date", ""), "%Y-%m-%d %H:%M:%S")
            except:
                continue

            if (
                (period == "daily" and order_date.date() == now.date()) or
                (period == "weekly" and now - timedelta(days=7) <= order_date <= now) or
                (period == "monthly" and order_date.year == now.year and order_date.month == now.month) or
                (period == "yearly" and order_date.year == now.year)
            ):
                filtered_orders.append(order)

        self.display_report(filtered_orders, period)

    def display_report(self, orders, period):
        if not orders:
            print(f"No {period} orders found.")
            return

        total_sales = 0
        print(f"\n--- {period.capitalize()} Order Report ---")
        print(f"{'Order ID':<12} | {'Date':<20} | {'Total Amount':<12}")
        print("-" * 50)

        for order in orders:
            order_id = order.get("order_id", "N/A")
            date = order.get("order_date", "N/A")
            try:
                total = float(order.get("total_amount", 0))
            except:
                total = 0.0
            total_sales += total
            print(f"{order_id:<12} | {date:<20} | ₹{total:<10.2f}")

        print("-" * 50)
        print(f"Total Sales: ₹{total_sales:.2f}")


def generate_report():
    report = ReportGenerator()
    report.generate()
