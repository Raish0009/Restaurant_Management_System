import uuid
import json
import os
from Src.Domain.Order.OrderProcessing import OrderProcessing

class Menu:

    def __init__(self):
        self.filename = rf"F:\Restaurant_Management_System\Src\Database\Menu.json"
        self.base_categories = [
            "Breakfast", "Lunch", "Dinner", "Snacks", 
            "Drinks", "Desserts", "Soft Drinks"
        ]
        self.FoodMenu = {category: [] for category in self.base_categories}
        self.load_menu()

    def load_menu(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                try:
                    loaded_data = json.load(file)
                    for category_name, items in loaded_data.items():
                        self.FoodMenu[category_name] = items
                except json.JSONDecodeError:
                    print("Warning: Menu.json is empty or corrupted. Using default category structure.")
        else:
            print(f"Info: {self.filename} not found. Starting with a new menu structure.")


    def save_menu(self):
        with open(self.filename, 'w') as file:
            json.dump(self.FoodMenu, file, indent=4)

    def remove_item(self):
        name = input("Enter the item name to remove: ").strip().lower()
        found = False

        for category in list(self.FoodMenu.keys()): 
            items_in_category = self.FoodMenu[category]
         
            for i in range(len(items_in_category) - 1, -1, -1):
                item = items_in_category[i]
                if item["item_name"].lower() == name:
                    removed_item_name = item['item_name'] 
                    self.FoodMenu[category].pop(i) 
                    self.save_menu()
                    print(f"Item '{removed_item_name}' removed from {category}.")
                    found = True

        if not found:
            print(f"No item found with name '{name}'.")


    def update_item(self):
        name = input("Enter the item name to update: ").strip().lower()
        found = False

        for category in self.FoodMenu:
            for item in self.FoodMenu[category]:
                if item["item_name"].lower() == name:
                    print(f"\nUpdating item in {category}: '{item['item_name']}'")
                    
                    # Update name
                    new_name = input(f"Current name: {item['item_name']}. Enter new name (leave blank to keep current): ").strip()
                    if new_name:
                        item['item_name'] = new_name

                    # Update size
                    print(f"Current size: {item['size']}")
                    new_size = input("Enter new size (e.g., Half, Full, Piece, Glass, Can - leave blank to keep current): ").strip()
                    if new_size:
                        item['size'] = new_size

                    # Update price
                    current_price_display = item.get('price', 'N/A')
                    print(f"Current price: ₹{current_price_display}")
                    new_price_str = input("Enter new price (leave blank to keep current): ").strip()
                    if new_price_str:
                        try:
                            float(new_price_str) 
                            item['price'] = new_price_str
                        except ValueError:
                            print("Invalid price format. Price not updated.")

                    self.save_menu()
                    print(f"Item '{item['item_name']}' updated successfully.")
                    found = True
                    break 
            if found:
                break  

        if not found:
            print(f"No item found with name '{name}'.")

    def display_table(self):
        display_categories = self.base_categories + [cat for cat in self.FoodMenu if cat not in self.base_categories]
        
        any_item_displayed = False
        for category in display_categories:
            items = self.FoodMenu.get(category, [])
            
            if category not in self.FoodMenu:
                continue

            print(f"\n{category}:")
            if not items:
                print("  No items yet.")
            else:
                any_item_displayed = True
                print(f"{'ID':<8} | {'Name':<25} | {'Size':<15} | {'Price':<8}")
                print("-" * (8 + 3 + 25 + 3 + 15 + 3 + 8 + 2)) 
                for item in items:
                    item_id = item.get('item_id', 'N/A')
                    item_name = item.get('item_name', 'N/A')
                    item_size = item.get('size', 'N/A')
                    item_price = item.get('price', 'N/A')
                    print(f"{item_id:<8} | {item_name:<25} | {item_size:<15} | ₹{item_price:<7}") 
        if not any_item_displayed and not self.FoodMenu: 
             print("Menu is completely empty.")


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
                
                item_name = input("Enter item name: ").strip()
                if not item_name:
                    print("Item name cannot be empty. Aborting add.")
                    continue
                menuDict['item_name'] = item_name

                # Size selection
                print("\nChoose Item Size/Type:")
                print("1 - Half Plate")
                print("2 - Full Plate")
                print("3 - Unit (e.g., Piece, Glass, Bottle, Can, Serving)")
                size_choice_input = input("Choose Item size/type option (1-3): ").strip()

                if size_choice_input == '1':
                    menuDict['size'] = "Half"
                elif size_choice_input == '2':
                    menuDict['size'] = "Full"
                elif size_choice_input == '3':
                    unit_type = input("Enter unit description (e.g., Piece, Glass, Bottle, Can, Serving): ").strip()
                    if unit_type:
                        menuDict['size'] = unit_type
                    else:
                        print("Unit description cannot be empty. Item not added.")
                        continue
                else:
                    print("Invalid size/type choice! Item not added.")
                    continue
                
                item_price_str = input("Enter item price: ").strip()
                if not item_price_str:
                    print("Item price cannot be empty. Aborting add.")
                    continue
                try:
                    float(item_price_str)
                    menuDict['price'] = item_price_str
                except ValueError:
                    print("Invalid price format. Please enter a numeric value. Item not added.")
                    continue

                # Category selection
                print("\nChoose Category:")
                for i, cat_name in enumerate(self.base_categories):
                    print(f"{i+1} - {cat_name}")
                
                category_choice_input = input(f"Choose Category number (1-{len(self.base_categories)}): ").strip()
                try:
                    category_idx = int(category_choice_input) - 1
                    if 0 <= category_idx < len(self.base_categories):
                        chosen_category_name = self.base_categories[category_idx]
                        menuDict['category'] = chosen_category_name 
                        
                        self.FoodMenu[chosen_category_name].append(menuDict)
                        self.save_menu()
                        print(f"Item '{menuDict['item_name']}' added to {chosen_category_name} and saved successfully!")
                    else:
                        print("Invalid category choice! Item not added.")
                        continue
                except ValueError:
                    print("Invalid input. Please enter a number for category. Item not added.")
                    continue

            elif choice == "3":
                self.remove_item()

            elif choice == "4":
                self.update_item()

            elif choice == "5":
                print("Exiting Menu Management... Thank you! 🙏")
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
