'''
Author: Nichole Sherman
Date: 12/5/2023
Purpose: Generate meal options based on user selections
'''
import tkinter as tk
from tkinter import ttk
import random

# Class to create Meal Generator
class MealGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Meal Generator")

        # Options to populate listboxes
        self.protein_options = ['beans', 'eggs', 'chicken breast',
                                'steak', 'shrimp', 'red lentils',
                                'pressed yogurt', 'scallops',
                                'salmon', 'pork tenderloin']
        self.veggie_options = ['broccoli', 'red cabbage', 'green beans',
                               'bok choy', 'spinach', 'kale',
                               'eggplant', 'carrots', 'brussels sprouts',
                               'bell peppers']
        self.carb_options = ['spaghetti squash', 'red potatoes',
                             'sweet potatoes', 'brown rice',
                             'quinoa', 'chickpeas', 'bulgur',
                             'plantain', 'butternut squash', 'spelt']
        self.fat_options = ['extra virgin olive oil', 'walnut oil',
                            'sesame oil', 'avocado oil', 'canola oil',
                            'extra virgin coconut oil', 'butter',
                            'raw avocado', 'chopped almonds',
                            'chopped peanuts']
        self.flavor_options = ['Italian', 'French', 'Mexican', 'Japanese',
                               'Thai', 'Moroccan', 'Indian', 'Caribbean',
                               'Southwest', 'Spanish']

        # Lists to store user selections
        self.selected_proteins = []
        self.selected_veggies = []
        self.selected_carbs = []
        self.selected_fats = []
        self.selected_flavors = []

        # Create dictionary storing spices and cooking instructions
        self.cooking_instructions = self.create_dictionary('cooking.txt')

        # Create instructions and labels for listboxes
        tk.Label(
            root, 
            text="Select as many items as you like from each category and click 'Save'.").grid(
                row=0, column=0, columnspan=5, padx=5)
        tk.Label(
            root, 
            text="Clicking a highlighted item will unselect it. The reset button will clear all categories").grid(
                row=1, column=0, columnspan=5, padx=5)
        tk.Label(
            root, 
            text="Once you are done saving, click 'Generate Meal'.").grid(
                row=2, column=0, columnspan=5, padx=5)
        tk.Label(root, text="Proteins").grid(row=3, column=0, padx=5, pady=5)
        tk.Label(root, text="Vegetables").grid(row=3, column=1, padx=5, pady=5)
        tk.Label(root, text="Smart Carbs").grid(row=3, column=2, padx=5, pady=5)
        tk.Label(root, text="Healthy Fats").grid(row=3, column=3, padx=5, pady=5)
        tk.Label(root, text="Flavor Profiles").grid(row=3, column=4, padx=5, pady=5)

        # Create listboxes and list of listboxes
        self.listboxes = []
        self.create_listbox(self.protein_options, 4, 0)
        self.create_listbox(self.veggie_options, 4, 1)
        self.create_listbox(self.carb_options, 4, 2)
        self.create_listbox(self.fat_options, 4, 3)
        self.create_listbox(self.flavor_options, 4, 4)
        
        # Create buttons
        self.create_button("Save", self.save_all, 9)
        self.create_button("Reset", self.reset_all, 10)
        self.create_button("Generate Meal", self.generate_meal, 11)

        # Create textbox to display generated meals
        self.result_text = tk.Text(root, width=80, height=30, wrap=tk.WORD)
        self.result_text.grid(row=12, column=0, columnspan=5, padx=5, pady=10)

    # Function to create and populate listboxes
    def create_listbox(self, options, row, column):
        listbox = tk.Listbox(
            self.root,
            selectmode=tk.MULTIPLE,
            width=20, height=10, exportselection=False)
        for option in options:
            listbox.insert(tk.END, option)
        listbox.grid(row=row, column=column, pady=5)
        # Store listboxes for use with save and reset buttons
        self.listboxes.append(listbox)  
    
    # Function to create buttons    
    def create_button(self, text, command, row):
        button = ttk.Button(
            self.root,
            text=text,
            command=command).grid(
                row=row, column=0, columnspan=5, pady=5)

    # Function to ensure selections are saved when save all button is pressed
    def save_all(self):
        # Pair the listbox with the corresponding selection list and iterate through to add selections to list
        for listbox, selected_list in zip(
            self.listboxes, [self.selected_proteins, self.selected_veggies, 
                             self.selected_carbs, self.selected_fats, self.selected_flavors]):
            selected_indices = listbox.curselection()
            selected_items = [listbox.get(index) for index in selected_indices]
            # Clear list in case user did not reset before re-selecting
            selected_list.clear()
            selected_list.extend(selected_items)

    # Function to reset all listbox selections and clear the selection lists
    def reset_all(self):
        # Pair the listbox with the corresponding selection list and iterate through to clear lists
        for listbox, selected_list in zip(
            self.listboxes, [self.selected_proteins, self.selected_veggies, 
                             self.selected_carbs, self.selected_fats, self.selected_flavors]):
            listbox.selection_clear(0, tk.END)
            selected_list.clear()

    # Function to create the dictionary
    def create_dictionary(self, file_path):
        result_dict = {}
        key = ''
        value_lines = []
        # Open and read file
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()  
            #Loop through lines, remove whitespace, and create key/value pairs         
            for line in lines:
                line = line.strip()
                if not line:
                    if key:
                        result_dict[key] = ' '.join(value_lines)
                        key = ''
                        value_lines = []
                elif not key:
                    key = line
                else:
                    value_lines.append(line)
            if key:
                result_dict[key] = ' '.join(value_lines)
            
            return result_dict

    # Function to generate meals
    def generate_meal(self):
        # Clear text area
        self.result_text.delete(1.0, tk.END)

        # Check for empty lists and alert user if any are found
        if not self.selected_proteins or not self.selected_veggies \
                or not self.selected_carbs or not self.selected_fats \
                or not self.selected_flavors:
            self.result_text.insert(
                tk.END,
                "Please select at least one option from each category and click save.")
            return

        # Generate a random meal from selected options
        protein_selection = random.choice(self.selected_proteins)
        veggie_selection = random.choice(self.selected_veggies)
        carb_selection = random.choice(self.selected_carbs)
        fat_selection = random.choice(self.selected_fats)
        flavor_selection = random.choice(self.selected_flavors)

        # Display the generated meal
        self.result_text.insert(tk.END, f"Meal Option:\n\n")
        self.result_text.insert(
            tk.END,
            f"Protein: {protein_selection}\n\n")
        self.result_text.insert(
            tk.END,
            f"Cooking Instructions: {self.cooking_instructions.get(protein_selection, 'No instructions available')}\n\n")
        self.result_text.insert(
            tk.END,
            f"Vegetable: {veggie_selection}\n\n")
        self.result_text.insert(
            tk.END,
            f"Cooking Instructions: {self.cooking_instructions.get(veggie_selection, 'No instructions available')}\n\n")
        self.result_text.insert(
            tk.END,
            f"Smart Carb: {carb_selection}\n\n")
        self.result_text.insert(
            tk.END,
            f"Cooking Instructions: {self.cooking_instructions.get(carb_selection, 'No instructions available')}\n\n")
        self.result_text.insert(
            tk.END,
            f"Healthy Fat: {fat_selection}\n\n")
        self.result_text.insert(
            tk.END,
            f"Flavor Profile: {flavor_selection}\n\n")
        self.result_text.insert(
            tk.END,
            f"Spices: {self.cooking_instructions.get(flavor_selection, 'No instructions available')}")
        
# Create instance of tkinter/GUI and MealGeneratorApp class and start program
if __name__ == "__main__":
    root = tk.Tk()
    app = MealGeneratorApp(root)
    root.mainloop()