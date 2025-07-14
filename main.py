import tkinter as tk
from tkinter import ttk, messagebox

class Room:
    def __init__(self, number_type, price, is_booked=False):
        self.number_type = int(number_type)
        self.price = float(price)
        self.is_booked = bool(is_booked)
    def book(self): #TO BOOK
        if not self.is_booked:
            self.is_booked = True
            return True
        return False
    def unbook(self): #TO UNBOOK
        self.is_booked = False
    def get_price(self):#GET THE ROOM PRICE
        return self.price
    def is_available(self):#CHECK AVAILABILITY
        return not self.is_booked

class Guest:
    def __init__(self, name, phone):
        self.name = str(name)
        self.phone = int(phone)
    def get_details(self): #GET CUSTOMER DETAILS
        return f"Guest Name: {self.name}, Phone: {self.phone}"

class Booking: 
    def __init__(self, number_type, name, days):
        self.number_type = int(number_type)
        self.name = str(name)
        self.days = int(days)

    def calculate_bill(self, room_price):
        return self.days * room_price #Not using inheritance
    # here from room as base class coz booking inheriting room is weird


        
class System: 
    def __init__(self):
        self.rooms = []
        self.bookings = []

    def add_room(self, number_type, price): #Add Room
        room = Room(number_type, price) #Creating a object as room
        self.rooms.append(room) #Append room in the list
        return f"Room {number_type} added successfully."

    def book_room(self, number_type, guest_name, days):
        for room in self.rooms:
            if room.number_type == number_type and room.is_available():
                if room.book():
                    booking = Booking(number_type, guest_name, days) #an instance of Booking class
                    self.bookings.append(booking)
                    bill = booking.calculate_bill(room.get_price())
                    return f"Room {number_type} booked for {guest_name}."
        return f"No available room of type {number_type} to book."

    def unbook_room(self, number_type):
        for room in self.rooms:
            if room.number_type == number_type and not room.is_available():
                room.unbook()
                return f"Room {number_type} has been unbooked."
        return f"Room {number_type} is not currently booked."

    def show_all_room(self):
        for room in self.rooms:
            status = "Booked" if room.is_booked else "Available"
            print(f"Room {room.number_type} | Price: {room.price} | Status: {status}")        

    def show_bookings(self):
        if not self.bookings:
            print("No bookings found.")
        for booking in self.bookings:
            print(f"{booking.name} booked Room {booking.number_type} for {booking.days} days")

class HotelGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System")
        self.root.geometry("800x600")
        
        self.system = System()
        
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        title_label = ttk.Label(main_frame, text="Hotel Management System", 
                               font=('Arial', 20, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.rowconfigure(1, weight=1)
        
        self.create_room_tab()
        self.create_booking_tab()
        self.create_view_tab()
    
    def create_room_tab(self):
        room_frame = ttk.Frame(self.notebook)
        self.notebook.add(room_frame, text="Room Management")
        
        add_room_frame = ttk.LabelFrame(room_frame, text="Add New Room", padding="10")
        add_room_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(add_room_frame, text="Room Number:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.room_number_entry = ttk.Entry(add_room_frame, width=20)
        self.room_number_entry.grid(row=0, column=1, padx=(10, 0), pady=5)
        
        ttk.Label(add_room_frame, text="Price per Night:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.room_price_entry = ttk.Entry(add_room_frame, width=20)
        self.room_price_entry.grid(row=1, column=1, padx=(10, 0), pady=5)
        
        add_room_btn = ttk.Button(add_room_frame, text="Add Room", command=self.add_room)
        add_room_btn.grid(row=2, column=0, columnspan=2, pady=10)
        
        room_list_frame = ttk.LabelFrame(room_frame, text="Room List", padding="10")
        room_list_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        room_frame.rowconfigure(1, weight=1)
        
        columns = ('Room Number', 'Price', 'Status')
        self.room_tree = ttk.Treeview(room_list_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.room_tree.heading(col, text=col)
            self.room_tree.column(col, width=150)
        
        self.room_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        room_scrollbar = ttk.Scrollbar(room_list_frame, orient=tk.VERTICAL, command=self.room_tree.yview)
        room_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.room_tree.configure(yscrollcommand=room_scrollbar.set)
        
        room_list_frame.columnconfigure(0, weight=1)
        room_list_frame.rowconfigure(0, weight=1)
        
        unbook_btn = ttk.Button(room_list_frame, text="Unbook Selected Room", command=self.unbook_room)
        unbook_btn.grid(row=1, column=0, pady=10)
        
        refresh_btn = ttk.Button(room_list_frame, text="Refresh", command=self.refresh_room_list)
        refresh_btn.grid(row=1, column=1, pady=10)
    
    def create_booking_tab(self):
        booking_frame = ttk.Frame(self.notebook)
        self.notebook.add(booking_frame, text="Make Booking")
        
        booking_form_frame = ttk.LabelFrame(booking_frame, text="New Booking", padding="10")
        booking_form_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(booking_form_frame, text="Room Number:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.booking_room_entry = ttk.Entry(booking_form_frame, width=20)
        self.booking_room_entry.grid(row=0, column=1, padx=(10, 0), pady=5)
        
        ttk.Label(booking_form_frame, text="Guest Name:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.guest_name_entry = ttk.Entry(booking_form_frame, width=20)
        self.guest_name_entry.grid(row=1, column=1, padx=(10, 0), pady=5)
        
        ttk.Label(booking_form_frame, text="Number of Days:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.days_entry = ttk.Entry(booking_form_frame, width=20)
        self.days_entry.grid(row=2, column=1, padx=(10, 0), pady=5)
        
        book_btn = ttk.Button(booking_form_frame, text="Book Room", command=self.book_room)
        book_btn.grid(row=3, column=0, columnspan=2, pady=10)
        
        available_frame = ttk.LabelFrame(booking_frame, text="Available Rooms", padding="10")
        available_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        booking_frame.rowconfigure(1, weight=1)
        
        columns = ('Room Number', 'Price per Night')
        self.available_tree = ttk.Treeview(available_frame, columns=columns, show='headings', height=8)
        
        for col in columns:
            self.available_tree.heading(col, text=col)
            self.available_tree.column(col, width=200)
        
        self.available_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        available_scrollbar = ttk.Scrollbar(available_frame, orient=tk.VERTICAL, command=self.available_tree.yview)
        available_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.available_tree.configure(yscrollcommand=available_scrollbar.set)
        
        available_frame.columnconfigure(0, weight=1)
        available_frame.rowconfigure(0, weight=1)
        
        refresh_available_btn = ttk.Button(available_frame, text="Refresh Available Rooms", command=self.refresh_available_rooms)
        refresh_available_btn.grid(row=1, column=0, pady=10)
        
        self.available_tree.bind('<Double-1>', self.on_available_room_select)
    
    def create_view_tab(self):
        view_frame = ttk.Frame(self.notebook)
        self.notebook.add(view_frame, text="View Bookings")
        
        bookings_frame = ttk.LabelFrame(view_frame, text="Current Bookings", padding="10")
        bookings_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        view_frame.rowconfigure(0, weight=1)
        view_frame.columnconfigure(0, weight=1)
        
        columns = ('Room Number', 'Guest Name', 'Days', 'Total Bill')
        self.bookings_tree = ttk.Treeview(bookings_frame, columns=columns, show='headings', height=12)
        
        for col in columns:
            self.bookings_tree.heading(col, text=col)
            self.bookings_tree.column(col, width=150)
        
        self.bookings_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        bookings_scrollbar = ttk.Scrollbar(bookings_frame, orient=tk.VERTICAL, command=self.bookings_tree.yview)
        bookings_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.bookings_tree.configure(yscrollcommand=bookings_scrollbar.set)
        
        bookings_frame.columnconfigure(0, weight=1)
        bookings_frame.rowconfigure(0, weight=1)
        
        refresh_bookings_btn = ttk.Button(bookings_frame, text="Refresh Bookings", command=self.refresh_bookings)
        refresh_bookings_btn.grid(row=1, column=0, pady=10)
    
    def add_room(self):
        try:
            room_number = int(self.room_number_entry.get())
            price = float(self.room_price_entry.get())
            
            message = self.system.add_room(room_number, price)
            messagebox.showinfo("Success", message)
            
            self.room_number_entry.delete(0, tk.END)
            self.room_price_entry.delete(0, tk.END)
            self.refresh_room_list()
            self.refresh_available_rooms()
                
        except ValueError:
            messagebox.showerror("Error", "Please enter valid room number and price.")
    
    def book_room(self):
        try:
            room_number = int(self.booking_room_entry.get())
            guest_name = self.guest_name_entry.get().strip()
            days = int(self.days_entry.get())
            
            if not guest_name:
                messagebox.showerror("Error", "Please enter guest name.")
                return
            
            if days <= 0:
                messagebox.showerror("Error", "Number of days must be positive.")
                return
            
            message = self.system.book_room(room_number, guest_name, days)
            
            if "booked for" in message:
                messagebox.showinfo("Success", message)
                self.booking_room_entry.delete(0, tk.END)
                self.guest_name_entry.delete(0, tk.END)
                self.days_entry.delete(0, tk.END)
                self.refresh_room_list()
                self.refresh_available_rooms()
                self.refresh_bookings()
            else:
                messagebox.showerror("Error", message)
                
        except ValueError:
            messagebox.showerror("Error", "Please enter valid room number and number of days.")
    
    def unbook_room(self):
        selected_item = self.room_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a room to unbook.")
            return
        
        room_number = int(self.room_tree.item(selected_item)['values'][0])
        
        message = self.system.unbook_room(room_number)
        
        if "unbooked" in message:
            messagebox.showinfo("Success", message)
            self.refresh_room_list()
            self.refresh_available_rooms()
            self.refresh_bookings()
        else:
            messagebox.showerror("Error", message)
    
    def on_available_room_select(self, event):
        selected_item = self.available_tree.selection()
        if selected_item:
            room_number = self.available_tree.item(selected_item)['values'][0]
            self.booking_room_entry.delete(0, tk.END)
            self.booking_room_entry.insert(0, str(room_number))
    
    def refresh_room_list(self):
        for item in self.room_tree.get_children():
            self.room_tree.delete(item)
        
        for room in self.system.rooms:
            status = "Booked" if room.is_booked else "Available"
            self.room_tree.insert('', 'end', values=(room.number_type, f"${room.price:.2f}", status))
    
    def refresh_available_rooms(self):
        for item in self.available_tree.get_children():
            self.available_tree.delete(item)
        
        for room in self.system.rooms:
            if room.is_available():
                self.available_tree.insert('', 'end', values=(room.number_type, f"${room.price:.2f}"))
    
    def refresh_bookings(self):
        for item in self.bookings_tree.get_children():
            self.bookings_tree.delete(item)
        
        for booking in self.system.bookings:
            room_price = 0
            for room in self.system.rooms:
                if room.number_type == booking.number_type:
                    room_price = room.price
                    break
            
            total_bill = booking.calculate_bill(room_price)
            self.bookings_tree.insert('', 'end', values=(
                booking.number_type, 
                booking.name, 
                booking.days, 
                f"${total_bill:.2f}"
            ))

def main():
    root = tk.Tk()
    app = HotelGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

                            