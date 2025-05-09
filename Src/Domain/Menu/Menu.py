import uuid
import json
import os
from Src.Domain.Order.OrderProcessing import OrderProcessing

class Menu:

    def __init__(self):
        self.filename = rf"F:\Restaurant_Management_System\Src\Database\Menu.json"
        self.FoodMenu = {
            "Breakfast": [],
            "Lunch": [],
            "Dinner": []
        }
        self.load_menu()

    def load_menu(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                try:
                    self.FoodMenu = json.load(file)
                except json.JSONDecodeError:
                    print("Warning: Menu is empty or corrupted. Starting fresh.")

    def save_menu(self):
        with open(self.filename, 'w') as file:
            json.dump(self.FoodMenu, file, indent=4)

    def remove_item(self):
        name = input("Enter the item name to remove: ").strip().lower()
        found = False

        for category in ["Breakfast", "Lunch", "Dinner"]:
            for item in self.FoodMenu[category]:
                if item["item_name"].lower() == name:
                    self.FoodMenu[category].remove(item)
                    self.save_menu()
                    print(f"Item '{item['item_name']}' removed from {category}.")
                    found = True
                    break
            if found:
                break

        if not found:
            print(f"No item found with name '{name}'.")

    def update_item(self):
        name = input("Enter the item name to update: ").strip().lower()
        found = False

        for category in ["Breakfast", "Lunch", "Dinner"]:
            for item in self.FoodMenu[category]:
                if item["item_name"].lower() == name:
                    print(f"Updating item in {category}:")
                    print(f"Current name: {item['item_name']}")
                    new_name = input("Enter new name (leave blank to keep current): ")
                    if new_name:
                        item['item_name'] = new_name

                    print(f"Current size: {item['size']}")
                    new_size = input("Enter new size (Half/Full, leave blank to keep current): ")
                    if new_size in ["Half", "Full"]:
                        item['size'] = new_size

                    print(f"Current price: {item['price']}")
                    new_price = input("Enter new price (leave blank to keep current): ")
                    if new_price:
                        item['price'] = new_price

                    self.save_menu()
                    print(f"Item '{item['item_name']}' updated.")
                    found = True
                    break
            if found:
                break

        if not found:
            print(f"No item found with name '{name}'.")

    def display_table(self):
        for category, items in self.FoodMenu.items():
            print(f"\n{category}:")
            if not items:
                print("  No items yet.")
            else:
                print(f"{'ID':<8} | {'Name':<20} | {'Size':<6} | {'Price':<6}")
                print("-" * 50)
                for item in items:
                    print(f"{item['item_id']:<8} | {item['item_name']:<20} | {item['size']:<6} | ₹{item['price']:<6}")

    def menucard(self):
        while True:
            print("\n--- Menu Management ---")
            print("1. View Full Menu")
            print("2. Add Item")
            print("3. Remove Item")
            print("4. Update Item")
            print("5. Exit")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                print("\n--- Full Menu ---")
                self.display_table()

            elif choice == "2":
                menuDict = {}
                item_id = str(uuid.uuid4())[:6]
                menuDict['item_id'] = item_id
                menuDict['item_name'] = input("Enter item name: ")

                print("1 - Half plate")
                print("2 - Full plate")
                size = int(input("Choose Item size: "))

                if size == 1:
                    menuDict['size'] = "Half"
                elif size == 2:
                    menuDict['size'] = "Full"
                else:
                    print("Invalid size choice!")
                    continue

                menuDict['price'] = input("Enter item price: ")

                print("1 - Breakfast")
                print("2 - Lunch")
                print("3 - Dinner")
                category = int(input("Choose Category: "))

                if category == 1:
                    menuDict['category'] = "Breakfast"
                    self.FoodMenu["Breakfast"].append(menuDict)
                elif category == 2:
                    menuDict['category'] = "Lunch"
                    self.FoodMenu["Lunch"].append(menuDict)
                elif category == 3:
                    menuDict['category'] = "Dinner"
                    self.FoodMenu["Dinner"].append(menuDict)
                else:
                    print("Invalid category choice!")
                    continue

                self.save_menu()
                print("Item added and saved successfully!")

            elif choice == "3":
                self.remove_item()

            elif choice == "4":
                self.update_item()

            elif choice == "5":
                print("Exiting... Thank you! 🙏")
                break

            else:
                print("Invalid choice! Please try again.")

    def staff_menu(self):
        while True:
            print("\n--- Staff Menu ---")
            print("1. View Full Menu")
            print("2. Process Order")
            print("3. Exit")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                print("\n--- Full Menu ---")
                self.display_table()

            elif choice == "2":
                order = OrderProcessing(self.filename)
                order.process()

            elif choice == "3":
                print("Exiting Staff Menu... 👋")
                break

            else:
                print("Invalid choice! Please try again.")
