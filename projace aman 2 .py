import tkinter as tk
from tkinter import messagebox
import json
import os

FILE = "inventory.json"

# Load inventory from file
def load_inventory():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return []

# Save inventory to file
def save_inventory():
    with open(FILE, "w") as f:
        json.dump(inventory, f, indent=2)

# Render inventory in listbox
def render_inventory(items=None):
    listbox.delete(0, tk.END)
    data = items if items is not None else inventory
    if not data:
        listbox.insert(tk.END, "No items in inventory.")
        return
    for index, item in enumerate(data):
        listbox.insert(tk.END, f"{index+1}. {item['name']} ({item['quantity']} pcs) - ₹{item['price']} - {item['category']} [{item['status']}]")

# Add item
def add_item():
    name = entry_name.get().strip()
    quantity = entry_quantity.get().strip()
    price = entry_price.get().strip()
    category = entry_category.get().strip()

    if not (name and quantity and price and category):
        messagebox.showwarning("Input Error", "Please fill all fields.")
        return

    try:
        quantity = int(quantity)
        price = float(price)
    except ValueError:
        messagebox.showerror("Type Error", "Quantity must be integer and Price must be number.")
        return

    inventory.append({
        "name": name,
        "quantity": quantity,
        "price": price,
        "category": category,
        "status": "In Stock"
    })
    save_inventory()
    render_inventory()
    entry_name.delete(0, tk.END)
    entry_quantity.delete(0, tk.END)
    entry_price.delete(0, tk.END)
    entry_category.delete(0, tk.END)

# Delete selected item
def delete_item():
    selected = listbox.curselection()
    if not selected:
        return
    index = selected[0]
    if index >= len(inventory):
        return
    confirm = messagebox.askyesno("Confirm", "Delete selected item?")
    if confirm:
        del inventory[index]
        save_inventory()
        render_inventory()

# Toggle status of selected item
def toggle_status():
    selected = listbox.curselection()
    if not selected:
        return
    index = selected[0]
    if index >= len(inventory):
        return
    inventory[index]["status"] = "Out of Stock" if inventory[index]["status"] == "In Stock" else "In Stock"
    save_inventory()
    render_inventory()

# Search items
def search_items():
    query = entry_search.get().strip().lower()
    if not query:
        render_inventory()
        return
    filtered = [item for item in inventory if query in item["name"].lower() or query in item["category"].lower()]
    render_inventory(filtered)

# --- GUI Setup ---
root = tk.Tk()
root.title("FreshMart Inventory Manager")
root.geometry("700x500")

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Name").grid(row=0, column=0)
entry_name = tk.Entry(frame)
entry_name.grid(row=0, column=1)

tk.Label(frame, text="Quantity").grid(row=0, column=2)
entry_quantity = tk.Entry(frame)
entry_quantity.grid(row=0, column=3)

tk.Label(frame, text="Price").grid(row=1, column=0)
entry_price = tk.Entry(frame)
entry_price.grid(row=1, column=1)

tk.Label(frame, text="Category").grid(row=1, column=2)
entry_category = tk.Entry(frame)
entry_category.grid(row=1, column=3)

tk.Button(frame, text="Add Item", bg="green", fg="white", command=add_item).grid(row=2, column=1, pady=10)
tk.Button(frame, text="Delete Item", command=delete_item).grid(row=2, column=2)
tk.Button(frame, text="Toggle Status", command=toggle_status).grid(row=2, column=3)

entry_search = tk.Entry(root)
entry_search.pack(pady=5, fill=tk.X, padx=10)
entry_search.insert(0, "Search by name or category")
entry_search.bind("<KeyRelease>", lambda e: search_items())

listbox = tk.Listbox(root, width=100, height=15)
listbox.pack(padx=10, pady=10)

inventory = load_inventory()
render_inventory()

root.mainloop()