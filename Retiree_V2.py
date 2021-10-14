from tkinter import *
import os
import tkinter
import tkinter.ttk
import tkinter.messagebox
import sqlite3
import datetime
import numpy as np
 

# Beginning of the application after login/register
def start():
	class Database:
	    def __init__(self):
	        self.dbConnection = sqlite3.connect("Retiree.db")
	        self.dbCursor = self.dbConnection.cursor()
	        

	        self.dbCursor.execute("""CREATE INDEX IF NOT EXISTS idx_Retiree_id ON Retiree (ret_id)""")
	        self.dbCursor.execute("""CREATE INDEX IF NOT EXISTS idx_name_lastname ON Retiree (name,last_name)""")

	        self.dbCursor.execute("""CREATE TABLE IF NOT EXISTS Retiree (ret_id INTEGER PRIMARY KEY AUTOINCREMENT,
	                                        name TEXT NOT NULL, 
	                                        last_name TEXT NOT NULL,
	                                        birth_date TEXT,
	                                        phone_number INTEGER,
	                                        email_address TEXT,
	                                        off_id INTEGER,
	                                        block_id INTEGER,
	                                        FOREIGN KEY (off_id)
	                                        REFERENCES Offspring (off_id),
	                                        FOREIGN KEY (block_id)
	                                        REFERENCES Block (block_id))""")
	        self.dbCursor.execute("""CREATE TABLE IF NOT EXISTS Offspring (off_id INTEGER PRIMARY KEY NOT NULL,
	                                        Retireeret_id INTEGER NOT NULL, 
	                                        off_name TEXT NOT NULL,
	                                        off_last_name TEXT NOT NULL,
	                                        off_phone_number INTEGER,
	                                        address_id INTEGER,
	                                        FOREIGN KEY (address_id)
	                                        REFERENCES Address (address_id))""")
	        self.dbCursor.execute("""CREATE TABLE IF NOT EXISTS Address (address_id INTEGER PRIMARY KEY NOT NULL,
	                                        province VARCHAR(255), 
	                                        city VARCHAR(255),
	                                        street VARCHAR(255),
	                                        zip_code VARCHAR(10),
	                                        flat INTEGER)""")
	        self.dbCursor.execute("""CREATE TABLE IF NOT EXISTS Block (block_id INTEGER,
	                                        block_section INTEGER, 
	                                        block_manager VARCHAR(255),
	                                        block_phone_number VARCHAR(11),
	                                        room_id INTEGER,
	                                        FOREIGN KEY (room_id)
	                                        REFERENCES Room (room_id))""")
	        self.dbCursor.execute("""CREATE TABLE IF NOT EXISTS Room (room_id INTEGER PRIMARY KEY NOT NULL,
	                                        room_number INTEGER, 
	                                        room_type CHARACTER(2),
	                                        room_fee DECIMAL(4,2))""")
	        self.dbCursor.execute("""CREATE TABLE IF NOT EXISTS Log ("" INTEGER,
	                                        name VARCHAR(255), 
	                                        last_name VARCHAR(255),
	                                        PRIMARY KEY("" AUTOINCREMENT))""")
	        
	        self.dbCursor.execute("""CREATE VIEW IF NOT EXISTS v_mostData AS SELECT ret_id,
	        	name,last_name,phone_number,off_name, off_last_name,block_section,block_manager,
	        	room_number,room_type,room_fee FROM Retiree 
	            INNER JOIN Offspring ON Retiree.off_id = Offspring.off_id
	            INNER JOIN Block ON Retiree.block_id = Block.block_id
	            INNER JOIN Room ON Block.room_id = Room.room_id UNION ALL SELECT * FROM Address""")

	        # self.dbCursor.execute("""CREATE TRIGGER IF NOT EXISTS LogTrigger AFTER UPDATE ON Retiree BEGIN 
	        #       INSERT INTO log VALUES (str(old.name),str(old.last_name),DATETIME('NOW')); END;""")

	    def __del__(self):
	        self.dbCursor.close()
	        self.dbConnection.close()

	    def InsertRetiree(self, name, last_name, birth_date, phone_number, email_address, off_id, block_id):
	        self.dbCursor.execute("""INSERT INTO Retiree 
	        (name, last_name, email_address, birth_date, phone_number, off_id, block_id)
	        VALUES (?,?,?,?,?,?,?)""", (name, last_name, birth_date, phone_number, email_address, off_id, block_id))
	        self.dbConnection.commit()

	    def InsertOff(self,off_id, off_name, off_last_name, off_phone_number, address_id, Retireeret_id):
	        self.dbCursor.execute("""INSERT INTO Offspring 
	        (off_id, off_name, off_last_name, off_phone_number, address_id, Retireeret_id)
	        VALUES (?,?,?,?,?,?)""", (off_id, off_name, off_last_name, off_phone_number, address_id, Retireeret_id))
	        self.dbConnection.commit()

	    def InsertAdd(self, address_id, province, city, street, zip_code, flat):
	        self.dbCursor.execute("""INSERT INTO Address 
	        (address_id, province, city, street, zip_code, flat)
	        VALUES (?,?,?,?,?,?)""", (address_id, province, city, street, zip_code, flat))
	        self.dbConnection.commit()

	    def InsertBlock(self, block_id, block_section, block_manager, block_phone_number, room_id):
	        self.dbCursor.execute("""INSERT INTO Block 
	        (block_id, block_section, block_manager, block_phone_number, room_id)
	        VALUES (?,?,?,?,?)""", (block_id, block_section, block_manager, block_phone_number, room_id))
	        self.dbConnection.commit()

	    def InsertRoom(self, room_id, room_number, room_type, room_fee):
	        self.dbCursor.execute("""INSERT INTO Room 
	        (room_id, room_number, room_type, room_fee)
	        VALUES (?,?,?,?)""", (room_id, room_number, room_type, room_fee))
	        self.dbConnection.commit()


	    def Update(self, name, last_name, birth_date, phone_number, email_address, off_id, block_id, ret_id):
	        self.dbCursor.execute("""UPDATE Retiree SET name = ?, last_name = ?, birth_date = ?, phone_number = ?, email_address = ?, off_id = ?, block_id = ? WHERE ret_id = ?""", (name, last_name, birth_date, phone_number, email_address, off_id, block_id,ret_id))
	        self.dbConnection.commit()


	    def Search(self, name, last_name):
	        self.dbCursor.execute("""SELECT ret_id,name,last_name,phone_number,off_name,
	            off_last_name,block_section,block_manager,room_number,room_type,room_fee FROM Retiree 
	            INNER JOIN Offspring ON Retiree.off_id = Offspring.off_id
	            INNER JOIN Block ON Retiree.block_id = Block.block_id
	            INNER JOIN Room ON Block.room_id = Room.room_id WHERE name = ? AND last_name = ?""", 
	            (name,last_name))
	        searchResults = self.dbCursor.fetchall()
	        return searchResults

	    def UpSearch(self, ret_id):
	        self.dbCursor.execute("SELECT * FROM Retiree WHERE ret_id = ? ", (ret_id,))
	        searchResults = self.dbCursor.fetchall()
	        return searchResults

	    
	    def Delete(self, name, last_name):
	        self.dbCursor.execute("DELETE FROM Retiree WHERE name = ? AND last_name = ?", (name,last_name))
	        self.dbConnection.commit()

	    def Display(self):
	        self.dbCursor.execute("""SELECT * FROM v_mostData""")        

	        records = self.dbCursor.fetchall()
	        return records

	    def statistics(self):
	        self.dbCursor.execute("""SELECT Room.room_fee FROM Retiree
	            INNER JOIN Block ON Block.block_id = Retiree.block_id 
	            INNER JOIN Room ON Room.room_id = Block.room_id""")
	        records = self.dbCursor.fetchall()
	        return records

	    def maxfee(self):
	        self.dbCursor.execute("""SELECT name,last_name,MAX(Room.room_fee) FROM Retiree
	            INNER JOIN Block ON Block.block_id = Retiree.block_id 
	            INNER JOIN Room ON Room.room_id = Block.room_id""")
	        records = self.dbCursor.fetchall()
	        return (records[0][0],records[0][1])

	    def minfee(self):
	        self.dbCursor.execute("""SELECT name,last_name,MIN(Room.room_fee) FROM Retiree
	            INNER JOIN Block ON Block.block_id = Retiree.block_id 
	            INNER JOIN Room ON Room.room_id = Block.room_id""")
	        records = self.dbCursor.fetchall()
	        return (records[0][0],records[0][1])

	a = Database()
	maxf = a.maxfee()
	minf = a.minfee()

	# Verifying the input values
	class Values:
	    def Validate(self,name, last_name, birth_date, phone_number, email_address, off_id, block_id):

	        if not (name.isalpha()):
	            return "name"
	        elif not (last_name.isalpha()):
	            return "last_name"
	        elif not (birth_date.isascii()):
	            return "birth_date"
	        elif not (phone_number.isascii()):
	            return "phone_number"
	        elif not (email_address.count("@") == 1) and (email_address.count(".") > 0):
	            return "email_address"
	        elif not (off_id.isascii()):
	            return "off_id"
	        elif not (block_id.isascii()):
	            return "block_id"
	        else:
	            return "SUCCESS"

	class ValuesOff:
	    def Validate(self,off_id, off_name, off_last_name, off_phone_number, address_id, Retireeret_id):
	        if not (off_id.isascii()):
	            return "off_id"
	        elif not (off_name.isalpha()):
	            return "off_name"
	        elif not (off_last_name.isalpha()):
	            return "off_last_name"
	        elif not (off_phone_number.isascii()):
	            return "off_phone_number"
	        elif not (address_id.isascii()):
	            return "address_id"
	        elif not (Retireeret_id.isascii()):
	            return "Retireeret_id"
	        else:
	            return "SUCCESS"


	class ValuesAdd:
	    def Validate(self, address_id, province, city, street, zip_code, flat):
	        if not (address_id.isascii()):
	            return "address_id"
	        elif not (province.isalpha()):
	            return "province"
	        elif not (city.isalpha()):
	            return "city"
	        elif not (street.isalpha() or street.isascii()):
	            return "street"
	        elif not (zip_code.isascii()):
	            return "zip_code"
	        elif not (flat.isascii()):
	            return "flat"
	        else:
	            return "SUCCESS"


	class ValuesBlock:
	    def Validate(self, block_id, block_section, block_manager, block_phone_number, room_id):
	        if not (block_id.isascii()):
	            return "block_id"
	        elif not (block_section.isascii()):
	            return "block_section"
	        elif not (block_manager.isascii()):
	            return "block_manager"
	        elif not (block_phone_number.isascii()):
	            return "block_phone_number"
	        elif not (room_id.isascii()):
	            return "room_id"
	        else:
	            return "SUCCESS"

	class ValuesRoom:
	    def Validate(self, room_id, room_number, room_type, room_fee):
	        if not (room_id.isascii()):
	            return "room_id"
	        elif not (room_number.isascii()):
	            return "room_number"
	        elif not (room_type.isalpha()):
	            return "room_type"
	        elif not (room_fee.isascii()):
	            return "room_fee"
	        else:
	            return "SUCCESS"

	class InsertWindow:
	    def __init__(self):
	        self.window = tkinter.Tk()
	        self.window.wm_title("Insert Retiree Data ")
	        bg_color = "dodger blue"
	        fg_color = "ghost white"

	        # Initializing all the variables
	        self.name = tkinter.StringVar()
	        self.last_name = tkinter.StringVar()
	        self.birth_date = tkinter.StringVar()
	        self.phone_number = tkinter.StringVar()
	        self.email_address = tkinter.StringVar()
	        self.off_id = tkinter.StringVar()
	        self.block_id = tkinter.StringVar()

	        # Labels

	        tkinter.Label(self.window, fg=fg_color, bg=bg_color, text="Retiree First Name", font=("Helvetica",10,"bold"), width=25).grid(pady=5, column=1, row=2)
	        tkinter.Label(self.window,  fg=fg_color, bg=bg_color, text="Retiree Last Name", font=("Helvetica",10,"bold"), width=25).grid(pady=5, column=1, row=3)
	        tkinter.Label(self.window,  fg=fg_color, bg=bg_color, font=("Helvetica",10,"bold"), text="Birthdate", width=25).grid(pady=5, column=1, row=4)
	        tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("Helvetica",10,"bold"), text="Phone Number", width=25).grid(pady=5, column=1, row=5)
	        tkinter.Label(self.window,  fg=fg_color, bg=bg_color, font=("Helvetica",10,"bold"),text="Email Address", width=25).grid(pady=5, column=1, row=6)
	        tkinter.Label(self.window,  fg=fg_color, bg=bg_color, font=("Helvetica",10,"bold"),text="Offspring ID", width=25).grid(pady=5, column=1, row=7)
	        tkinter.Label(self.window,  fg=fg_color, bg=bg_color, font=("Helvetica",10,"bold"),text="Block ID", width=25).grid(pady=5, column=1, row=8)

	        #self.ret_idEntry = tkinter.Entry(self.window, width=25, textvariable=self.ret_id)
	        self.nameEntry = tkinter.Entry(self.window, width=25, textvariable=self.name)
	        self.last_nameEntry = tkinter.Entry(self.window, width=25, textvariable=self.last_name)
	        self.birth_dateEntry = tkinter.Entry(self.window, width=25, textvariable=self.birth_date)
	        self.phone_numberEntry = tkinter.Entry(self.window, width=25, textvariable=self.phone_number)
	        self.email_addressEntry = tkinter.Entry(self.window, width=25, textvariable=self.email_address)
	        self.off_idEntry = tkinter.Entry(self.window, width=25, textvariable=self.off_id)
	        self.block_idEntry = tkinter.Entry(self.window, width=25, textvariable=self.block_id)

	        
	        self.nameEntry.grid(pady=5, column=3, row=2)
	        self.last_nameEntry.grid(pady=5, column=3, row=3)
	        self.phone_numberEntry.grid(pady=5, column=3, row=4)
	        self.email_addressEntry.grid(pady=5, column=3, row=5)
	        self.birth_dateEntry.grid(pady=5, column=3, row=6)
	        self.off_idEntry.grid(pady=5, column=3, row=7)
	        self.block_idEntry.grid(pady=5, column=3, row=8)


	        # Button widgets

	        tkinter.Button(self.window, width=10, fg=fg_color, bg=bg_color, 
	                       font=("Helvetica",10,"bold"), text="Insert", 
	                       command=self.Insert).grid(pady=15, padx=5, column=1, row=9)
	        tkinter.Button(self.window, width=10, fg=fg_color, bg=bg_color, 
	                       font=("Helvetica",10,"bold"), text="Reset", 
	                       command=self.Reset).grid(pady=15, padx=5, column=2, row=9)
	        tkinter.Button(self.window, width=10, fg=fg_color, bg=bg_color, 
	                       font=("Helvetica",10,"bold"), text="Close", 
	                       command=self.window.destroy).grid(pady=15, padx=5, column=3, row=9)

	        self.window.mainloop()


	    def Insert(self):
	        self.values = Values()
	        self.database = Database()
	        self.test = self.values.Validate(self.nameEntry.get(), self.last_nameEntry.get(), self.birth_dateEntry.get(),
	                                         self.phone_numberEntry.get(), self.email_addressEntry.get(), self.off_idEntry.get(), self.block_idEntry.get())
	        if (self.test == "SUCCESS"):
	            self.database.InsertRetiree(self.nameEntry.get(), self.last_nameEntry.get(), self.birth_dateEntry.get(),
	                                         self.phone_numberEntry.get(), self.email_addressEntry.get(), self.off_idEntry.get(), self.block_idEntry.get())
	            tkinter.messagebox.showinfo("Inserted data", "The retiree has been successfully added")
	        else:
	            self.valueErrorMessage = "Invalid input in field " + self.test
	            tkinter.messagebox.showerror("Value Error", self.valueErrorMessage)

	    def Reset(self):
	        self.ret_idEntry.delete(0, tkinter.END)
	        self.nameEntry.delete(0, tkinter.END)
	        self.last_nameEntry.delete(0, tkinter.END)
	        self.phone_numberEntry.delete(0, tkinter.END)
	        self.email_addressEntry.delete(0, tkinter.END)
	        self.birth_dateEntry.delete(0, tkinter.END)
	        self.off_idEntry.delete(0, tkinter.END)
	        self.block_idEntry.delete(0, tkinter.END)


	# Insert window for Offspring table

	class InsertWindowOff:
	    def __init__(self):
	        self.window = tkinter.Tk()
	        self.window.wm_title("Insert Offspring Data ")
	        bg_color = "dodger blue"
	        fg_color = "ghost white"

	        # Initializing all the variables

	        self.off_id = tkinter.StringVar()
	        self.off_name = tkinter.StringVar()
	        self.off_last_name = tkinter.StringVar()
	        self.off_phone_number = tkinter.StringVar()
	        self.address_id = tkinter.StringVar()
	        self.Retireeret_id = tkinter.StringVar()


	        # Labels
	        tkinter.Label(self.window, fg=fg_color, bg=bg_color, text="Offspring ID", font=("Helvetica",10,"bold"), width=25).grid(pady=5, column=1, row=1)        
	        tkinter.Label(self.window, fg=fg_color, bg=bg_color, text="Offspring First Name", font=("Helvetica",10,"bold"), width=25).grid(pady=5, column=1, row=2)
	        tkinter.Label(self.window,  fg=fg_color, bg=bg_color, text="Offspring Last Name", font=("Helvetica",10,"bold"), width=25).grid(pady=5, column=1, row=3)
	        tkinter.Label(self.window,  fg=fg_color, bg=bg_color, font=("Helvetica",10,"bold"), text="Phone Number", width=25).grid(pady=5, column=1, row=4)
	        tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("Helvetica",10,"bold"), text="Address ID", width=25).grid(pady=5, column=1, row=5)
	        tkinter.Label(self.window,  fg=fg_color, bg=bg_color, font=("Helvetica",10,"bold"),text="Retiree ID", width=25).grid(pady=5, column=1, row=6)


	        self.off_idEntry = tkinter.Entry(self.window, width=25, textvariable=self.off_id)
	        self.off_nameEntry = tkinter.Entry(self.window, width=25, textvariable=self.off_name)
	        self.off_last_nameEntry = tkinter.Entry(self.window, width=25, textvariable=self.off_last_name)
	        self.off_phone_numberEntry = tkinter.Entry(self.window, width=25, textvariable=self.off_phone_number)
	        self.address_idEntry = tkinter.Entry(self.window, width=25, textvariable=self.address_id)
	        self.Retireeret_idEntry = tkinter.Entry(self.window, width=25, textvariable=self.Retireeret_id)
	        

	        self.off_idEntry.grid(pady=5, column=3, row=1)
	        self.off_nameEntry.grid(pady=5, column=3, row=2)
	        self.off_last_nameEntry.grid(pady=5, column=3, row=3)
	        self.off_phone_numberEntry.grid(pady=5, column=3, row=4)
	        self.address_idEntry.grid(pady=5, column=3, row=5)
	        self.Retireeret_idEntry.grid(pady=5, column=3, row=6)

	        # Button widgets
	        tkinter.Button(self.window, width=10, fg=fg_color, bg=bg_color, 
	                       font=("Helvetica",10,"bold"), text="Insert", 
	                       command=self.InsertOff).grid(pady=15, padx=5, column=1, row=7)
	        tkinter.Button(self.window, width=10, fg=fg_color, bg=bg_color, 
	                       font=("Helvetica",10,"bold"), text="Reset", 
	                       command=self.Reset).grid(pady=15, padx=5, column=2, row=7)
	        tkinter.Button(self.window, width=10, fg=fg_color, bg=bg_color, 
	                       font=("Helvetica",10,"bold"), text="Close", 
	                       command=self.window.destroy).grid(pady=15, padx=5, column=3, row=7)

	        self.window.mainloop()


	    def InsertOff(self):
	        self.values = ValuesOff()
	        self.database = Database()
	        self.test = self.values.Validate(self.off_idEntry.get(), self.off_nameEntry.get(), self.off_last_nameEntry.get(), self.off_phone_numberEntry.get(),
	                                         self.address_idEntry.get(), self.Retireeret_idEntry.get())
	        if (self.test == "SUCCESS"):
	            self.database.InsertOff(self.off_idEntry.get(), self.off_nameEntry.get(), self.off_last_nameEntry.get(), self.off_phone_numberEntry.get(),
	                                         self.address_idEntry.get(), self.Retireeret_idEntry.get())
	            tkinter.messagebox.showinfo("Inserted data", "Your offspring has been successfully added")
	        else:
	            self.valueErrorMessage = "Invalid input in field " + self.test
	            tkinter.messagebox.showerror("Value Error", self.valueErrorMessage)

	    def Reset(self):
	        self.off_idEntry.delete(0, tkinter.END)
	        self.off_nameEntry.delete(0, tkinter.END)
	        self.off_last_nameEntry.delete(0, tkinter.END)
	        self.off_phone_numberEntry.delete(0, tkinter.END)
	        self.address_idEntry.delete(0, tkinter.END)
	        self.Retireeret_idEntry.delete(0, tkinter.END)


	# Insert window for Address table

	class InsertWindowAdd:
	    def __init__(self):
	        self.window = tkinter.Tk()
	        self.window.wm_title("Insert Address Data ")
	        bg_color = "dodger blue"
	        fg_color = "ghost white"

	        # Initializing all the variables

	        self.address_id = tkinter.StringVar()
	        self.province = tkinter.StringVar()
	        self.city = tkinter.StringVar()
	        self.street = tkinter.StringVar()
	        self.zip_code = tkinter.StringVar()
	        self.flat = tkinter.StringVar()


	        # Labels
	        tkinter.Label(self.window, fg=fg_color, bg=bg_color, text="Address ID", font=("Helvetica",10,"bold"), width=25).grid(pady=5, column=1, row=1)
	        tkinter.Label(self.window, fg=fg_color, bg=bg_color, text="Province", font=("Helvetica",10,"bold"), width=25).grid(pady=5, column=1, row=2)
	        tkinter.Label(self.window,  fg=fg_color, bg=bg_color, text="City", font=("Helvetica",10,"bold"), width=25).grid(pady=5, column=1, row=3)
	        tkinter.Label(self.window,  fg=fg_color, bg=bg_color, font=("Helvetica",10,"bold"), text="Street", width=25).grid(pady=5, column=1, row=4)
	        tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("Helvetica",10,"bold"), text="Zip code", width=25).grid(pady=5, column=1, row=5)
	        tkinter.Label(self.window,  fg=fg_color, bg=bg_color, font=("Helvetica",10,"bold"),text="Flat", width=25).grid(pady=5, column=1, row=6)


	        self.address_idEntry = tkinter.Entry(self.window, width=25, textvariable=self.address_id)
	        self.provinceEntry = tkinter.Entry(self.window, width=25, textvariable=self.province)
	        self.cityEntry = tkinter.Entry(self.window, width=25, textvariable=self.city)
	        self.streetEntry = tkinter.Entry(self.window, width=25, textvariable=self.street)
	        self.zip_codeEntry = tkinter.Entry(self.window, width=25, textvariable=self.zip_code)
	        self.flatEntry = tkinter.Entry(self.window, width=25, textvariable=self.flat)
	        

	        
	        self.address_idEntry.grid(pady=5, column=3, row=1)
	        self.provinceEntry.grid(pady=5, column=3, row=2)
	        self.cityEntry.grid(pady=5, column=3, row=3)
	        self.streetEntry.grid(pady=5, column=3, row=4)
	        self.zip_codeEntry.grid(pady=5, column=3, row=5)
	        self.flatEntry.grid(pady=5, column=3, row=6)


	        # Button widgets

	        tkinter.Button(self.window, width=10, fg=fg_color, bg=bg_color, 
	                       font=("Helvetica",10,"bold"), text="Insert", 
	                       command=self.InsertAdd).grid(pady=15, padx=5, column=1, row=7)
	        tkinter.Button(self.window, width=10, fg=fg_color, bg=bg_color, 
	                       font=("Helvetica",10,"bold"), text="Reset", 
	                       command=self.Reset).grid(pady=15, padx=5, column=2, row=7)
	        tkinter.Button(self.window, width=10, fg=fg_color, bg=bg_color, 
	                       font=("Helvetica",10,"bold"), text="Close", 
	                       command=self.window.destroy).grid(pady=15, padx=5, column=3, row=7)

	        self.window.mainloop()


	    def InsertAdd(self):
	        self.values = ValuesAdd()
	        self.database = Database()
	        self.test = self.values.Validate(self.address_idEntry.get(), self.provinceEntry.get(), self.cityEntry.get(), self.streetEntry.get(),
	                                         self.zip_codeEntry.get(), self.flatEntry.get())
	        if (self.test == "SUCCESS"):
	            self.database.InsertAdd(self.address_idEntry.get(), self.provinceEntry.get(), self.cityEntry.get(), self.streetEntry.get(),
	                                         self.zip_codeEntry.get(), self.flatEntry.get())
	            tkinter.messagebox.showinfo("Inserted data", "Your address has been successfully added")
	        else:
	            self.valueErrorMessage = "Invalid input in field " + self.test
	            tkinter.messagebox.showerror("Value Error", self.valueErrorMessage)

	    def Reset(self):
	        self.address_idEntry.delete(0, tkinter.END)
	        self.provinceEntry.delete(0, tkinter.END)
	        self.cityEntry.delete(0, tkinter.END)
	        self.streetEntry.delete(0, tkinter.END)
	        self.zip_codeEntry.delete(0, tkinter.END)
	        self.flatEntry.delete(0, tkinter.END)

	# Insert window for Block table

	class InsertWindowBlock:
	    def __init__(self):
	        self.window = tkinter.Tk()
	        self.window.wm_title("Insert Block Data ")
	        bg_color = "dodger blue"
	        fg_color = "ghost white"


	        self.block_id = tkinter.StringVar()
	        self.block_section = tkinter.StringVar()
	        self.block_manager = tkinter.StringVar()
	        self.block_phone_number = tkinter.StringVar()
	        self.room_id = tkinter.StringVar()


	        # Labels

	        tkinter.Label(self.window, fg=fg_color, bg=bg_color, text="Block ID", font=("Helvetica",10,"bold"), width=25).grid(pady=5, column=1, row=1)
	        tkinter.Label(self.window, fg=fg_color, bg=bg_color, text="Block section", font=("Helvetica",10,"bold"), width=25).grid(pady=5, column=1, row=2)
	        tkinter.Label(self.window,  fg=fg_color, bg=bg_color, text="Block manager", font=("Helvetica",10,"bold"), width=25).grid(pady=5, column=1, row=3)
	        tkinter.Label(self.window,  fg=fg_color, bg=bg_color, font=("Helvetica",10,"bold"), text="Block phone number", width=25).grid(pady=5, column=1, row=4)
	        tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("Helvetica",10,"bold"), text="Room ID", width=25).grid(pady=5, column=1, row=5)


	        self.block_idEntry = tkinter.Entry(self.window, width=25, textvariable=self.block_id)
	        self.block_sectionEntry = tkinter.Entry(self.window, width=25, textvariable=self.block_section)
	        self.block_managerEntry = tkinter.Entry(self.window, width=25, textvariable=self.block_manager)
	        self.block_phone_numberEntry = tkinter.Entry(self.window, width=25, textvariable=self.block_phone_number)
	        self.room_idEntry = tkinter.Entry(self.window, width=25, textvariable=self.room_id)
	        

	        
	        self.block_idEntry.grid(pady=5, column=3, row=1)
	        self.block_sectionEntry.grid(pady=5, column=3, row=2)
	        self.block_managerEntry.grid(pady=5, column=3, row=3)
	        self.block_phone_numberEntry.grid(pady=5, column=3, row=4)
	        self.room_idEntry.grid(pady=5, column=3, row=5)


	        # Button widgets

	        tkinter.Button(self.window, width=10, fg=fg_color, bg=bg_color, 
	                       font=("Helvetica",10,"bold"), text="Insert", 
	                       command=self.InsertBlock).grid(pady=15, padx=5, column=1, row=7)
	        tkinter.Button(self.window, width=10, fg=fg_color, bg=bg_color, 
	                       font=("Helvetica",10,"bold"), text="Reset", 
	                       command=self.Reset).grid(pady=15, padx=5, column=2, row=7)
	        tkinter.Button(self.window, width=10, fg=fg_color, bg=bg_color, 
	                       font=("Helvetica",10,"bold"), text="Close", 
	                       command=self.window.destroy).grid(pady=15, padx=5, column=3, row=7)

	        self.window.mainloop()


	    def InsertBlock(self):
	        self.values = ValuesBlock()
	        self.database = Database()
	        self.test = self.values.Validate(self.block_idEntry.get(), self.block_sectionEntry.get(), self.block_managerEntry.get(), self.block_phone_numberEntry.get(),
	                                         self.room_idEntry.get())
	        if (self.test == "SUCCESS"):
	            self.database.InsertBlock(self.block_idEntry.get(), self.block_sectionEntry.get(), self.block_managerEntry.get(), self.block_phone_numberEntry.get(),
	                                         self.room_idEntry.get())
	            tkinter.messagebox.showinfo("Inserted data", "Your block has been successfully added")
	        else:
	            self.valueErrorMessage = "Invalid input in field " + self.test
	            tkinter.messagebox.showerror("Value Error", self.valueErrorMessage)

	    def Reset(self):
	        self.block_idEntry.delete(0, tkinter.END)
	        self.block_sectionEntry.delete(0, tkinter.END)
	        self.block_managerEntry.delete(0, tkinter.END)
	        self.block_phone_numberEntry.delete(0, tkinter.END)
	        self.room_idEntry.delete(0, tkinter.END)


	# Insert window for Room table

	class InsertWindowRoom:
	    def __init__(self):
	        self.window = tkinter.Tk()
	        self.window.wm_title("Insert Room Data ")
	        bg_color = "dodger blue"
	        fg_color = "ghost white"


	        self.room_id = tkinter.StringVar()
	        self.room_number = tkinter.StringVar()
	        self.room_type = tkinter.StringVar()
	        self.room_fee = tkinter.StringVar()


	        # Labels
	        tkinter.Label(self.window, fg=fg_color, bg=bg_color, text="Room ID", font=("Helvetica",10,"bold"), width=25).grid(pady=5, column=1, row=1)
	        tkinter.Label(self.window, fg=fg_color, bg=bg_color, text="Room number", font=("Helvetica",10,"bold"), width=25).grid(pady=5, column=1, row=2)
	        tkinter.Label(self.window,  fg=fg_color, bg=bg_color, text="Room type", font=("Helvetica",10,"bold"), width=25).grid(pady=5, column=1, row=3)
	        tkinter.Label(self.window,  fg=fg_color, bg=bg_color, font=("Helvetica",10,"bold"), text="Room fee", width=25).grid(pady=5, column=1, row=4)


	        self.room_idEntry = tkinter.Entry(self.window, width=25, textvariable=self.room_id)
	        self.room_numberEntry = tkinter.Entry(self.window, width=25, textvariable=self.room_number)
	        self.room_typeEntry = tkinter.Entry(self.window, width=25, textvariable=self.room_type)
	        self.room_feeEntry = tkinter.Entry(self.window, width=25, textvariable=self.room_fee)
	        

	        
	        self.room_idEntry.grid(pady=5, column=3, row=1)
	        self.room_numberEntry.grid(pady=5, column=3, row=2)
	        self.room_typeEntry.grid(pady=5, column=3, row=3)
	        self.room_feeEntry.grid(pady=5, column=3, row=4)


	        # Button widgets

	        tkinter.Button(self.window, width=10, fg=fg_color, bg=bg_color, 
	                       font=("Helvetica",10,"bold"), text="Insert", 
	                       command=self.InsertRoom).grid(pady=15, padx=5, column=1, row=5)
	        tkinter.Button(self.window, width=10, fg=fg_color, bg=bg_color, 
	                       font=("Helvetica",10,"bold"), text="Reset", 
	                       command=self.Reset).grid(pady=15, padx=5, column=2, row=5)
	        tkinter.Button(self.window, width=10, fg=fg_color, bg=bg_color, 
	                       font=("Helvetica",10,"bold"), text="Close", 
	                       command=self.window.destroy).grid(pady=15, padx=5, column=3, row=5)

	        self.window.mainloop()


	    def InsertRoom(self):
	        self.values = ValuesRoom()
	        self.database = Database()
	        self.test = self.values.Validate(self.room_idEntry.get(), self.room_numberEntry.get(), self.room_typeEntry.get(), self.room_feeEntry.get())
	        
	        if (self.test == "SUCCESS"):
	            self.database.InsertRoom(self.room_idEntry.get(), self.room_numberEntry.get(), self.room_typeEntry.get(), self.room_feeEntry.get())
	            tkinter.messagebox.showinfo("Inserted data", "Your room has been successfully added")
	        else:
	            self.valueErrorMessage = "Invalid input in field " + self.test
	            tkinter.messagebox.showerror("Value Error", self.valueErrorMessage)

	    def Reset(self):
	        self.room_idEntry.delete(0, tkinter.END)
	        self.room_numberEntry.delete(0, tkinter.END)
	        self.room_typeEntry.delete(0, tkinter.END)
	        self.room_feeEntry.delete(0, tkinter.END)

	class UpdateWindow:
	    def __init__(self, ret_id):
	        self.window = tkinter.Tk()
	        self.window.wm_title("Update data")
	        bg_color = "dodger blue"
	        fg_color = "ghost white"
	        

	        #Initializing all the variables

	        self.ret_id = ret_id
	        self.name = tkinter.StringVar()
	        self.last_name = tkinter.StringVar()
	        self.birth_date = tkinter.StringVar()
	        self.phone_number = tkinter.StringVar()
	        self.email_address = tkinter.StringVar()
	        self.off_id = tkinter.StringVar()
	        self.block_id = tkinter.StringVar()


	        # Labels

	        tkinter.Label(self.window, fg=fg_color, bg=bg_color, text="Retiree ID", font=("Helvetica", 10, "bold"),
	                      width=25).grid(pady=5, column=1, row=1)
	        tkinter.Label(self.window, fg=fg_color, bg=bg_color, text="Retiree First Name",
	                      font=("Helvetica", 10, "bold"), width=25).grid(pady=5, column=1, row=2)
	        tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("Helvetica", 10, "bold"),
	                      text="Retiree Last Name", width=25).grid(pady=5, column=1, row=3)
	        tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("Helvetica", 10, "bold"), text="Birthdate",
	                      width=25).grid(pady=5, column=1, row=4)
	        tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("Helvetica", 10, "bold"),
	                      text="Phone Number", width=25).grid(pady=5, column=1, row=5)
	        tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("Helvetica", 10, "bold"), text="Email Address",
	                      width=25).grid(pady=5, column=1, row=6)
	        tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("Helvetica", 10, "bold"),
	                      text="Offspring ID", width=25).grid(pady=5, column=1, row=7)
	        tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("Helvetica", 10, "bold"),
	                      text="Block ID", width=25).grid(pady=5, column=1, row=8)

	        # Set previous values

	        self.database = Database()
	        self.searchResults = self.database.UpSearch(ret_id)
	        tkinter.Label(self.window, text=self.searchResults[0][0], width=25).grid(pady=5, column=2, row=1)
	        tkinter.Label(self.window, text=self.searchResults[0][1], width=25).grid(pady=5, column=2, row=2)
	        tkinter.Label(self.window, text=self.searchResults[0][2], width=25).grid(pady=5, column=2, row=3)
	        tkinter.Label(self.window, text=self.searchResults[0][3], width=25).grid(pady=5, column=2, row=4)
	        tkinter.Label(self.window, text=self.searchResults[0][4], width=25).grid(pady=5, column=2, row=5)
	        tkinter.Label(self.window, text=self.searchResults[0][5], width=25).grid(pady=5, column=2, row=6)
	        tkinter.Label(self.window, text=self.searchResults[0][6], width=25).grid(pady=5, column=2, row=7)
	        tkinter.Label(self.window, text=self.searchResults[0][7], width=25).grid(pady=5, column=2, row=8)



	        self.ret_idEntry = tkinter.Entry(self.window, width=25, textvariable=self.ret_id)
	        self.nameEntry = tkinter.Entry(self.window, width=25, textvariable=self.name)
	        self.last_nameEntry = tkinter.Entry(self.window, width=25, textvariable=self.last_name)
	        self.birth_dateEntry = tkinter.Entry(self.window, width=25, textvariable=self.birth_date)
	        self.phone_numberEntry = tkinter.Entry(self.window, width=25, textvariable=self.phone_number)
	        self.email_addressEntry = tkinter.Entry(self.window, width=25, textvariable=self.email_address)
	        self.off_idEntry = tkinter.Entry(self.window, width=25, textvariable=self.off_id)
	        self.block_idEntry = tkinter.Entry(self.window, width=25, textvariable=self.block_id)

	   

	        self.ret_idEntry.grid(pady=5, column=3, row=1)
	        self.nameEntry.grid(pady=5, column=3, row=2)
	        self.last_nameEntry.grid(pady=5, column=3, row=3)
	        self.birth_dateEntry.grid(pady=5, column=3, row=4)
	        self.phone_numberEntry.grid(pady=5, column=3, row=5)
	        self.email_addressEntry.grid(pady=5, column=3, row=6)
	        self.off_idEntry.grid(pady=5, column=3, row=7)
	        self.block_idEntry.grid(pady=5, column=3, row=8)

	        # Button

	        tkinter.Button(self.window, width=10, fg=fg_color, bg=bg_color, 
	                       font=("Helvetica",10,"bold"), text="Update", 
	                       command=self.Update).grid(pady=15, padx=5, column=1, row=9)
	        tkinter.Button(self.window, width=10, fg=fg_color, bg=bg_color, 
	                       font=("Helvetica",10,"bold"), text="Reset", 
	                       command=self.Reset).grid(pady=15, padx=5, column=2, row=9)
	        tkinter.Button(self.window, width=10, fg=fg_color, bg=bg_color, 
	                       font=("Helvetica",10,"bold"), text="Close", 
	                       command=self.window.destroy).grid(pady=15, padx=5, column=3, row=9)

	        self.window.mainloop()


	    def Update(self):
	        self.database = Database()
	        self.database.Update(self.nameEntry.get(),self.last_nameEntry.get(), self.birth_dateEntry.get(), 
	        	self.phone_numberEntry.get(), self.email_addressEntry.get(), self.off_idEntry.get(), self.block_idEntry.get(), self.ret_id)
	        tkinter.messagebox.showinfo("Updated data", "Successfully updated the above data in the database")

	    def Reset(self):
	        self.ret_idEntry.delete(0, tkinter.END)
	        self.nameEntry.delete(0, tkinter.END)
	        self.last_nameEntry.delete(0, tkinter.END)
	        self.phone_numberEntry.delete(0, tkinter.END)
	        self.email_addressEntry.delete(0, tkinter.END)
	        self.birth_dateEntry.delete(0, tkinter.END)
	        self.off_idEntry.delete(0, tkinter.END)
	        self.block_idEntry.delete(0, tkinter.END)
	        


	class DatabaseView:
	    def __init__(self, data):
	        self.databaseViewWindow = tkinter.Tk()
	        self.databaseViewWindow.wm_title("Database View")

	        # Label widgets

	        tkinter.Label(self.databaseViewWindow, text="Database View Window", width=25).grid(pady=5, column=1, row=1)

	        self.databaseView = tkinter.ttk.Treeview(self.databaseViewWindow)
	        self.databaseView.grid(pady=5, column=1, row=2)
	        self.databaseView["show"] = "headings"
	        self.databaseView["columns"] = (
	        "ret_id", "name", "last_name", "phone_number", "off_name", "off_last_name", "block_section", 
	        "block_manager", "room_number", "room_type", "room_fee")

	        # Treeview column headings

	        self.databaseView.heading("ret_id", text="Retiree ID")
	        self.databaseView.heading("name", text="First Name")
	        self.databaseView.heading("last_name", text="Last Name")
	        self.databaseView.heading("phone_number", text="Phone")
	        self.databaseView.heading("off_name", text="Offspring Name")
	        self.databaseView.heading("off_last_name", text="Offspring Last Name")
	        self.databaseView.heading("block_section", text="Block Section")
	        self.databaseView.heading("block_manager", text="Block Manager")
	        self.databaseView.heading("room_number", text="Room Number")
	        self.databaseView.heading("room_type", text="Room Type")
	        self.databaseView.heading("room_fee", text="Room Fee")


	        # Treeview columns

	        self.databaseView.column("ret_id", width=75)
	        self.databaseView.column("name", width=100)
	        self.databaseView.column("last_name", width=100)
	        self.databaseView.column("phone_number", width=100)
	        self.databaseView.column("off_name", width=100)
	        self.databaseView.column("off_last_name", width=120)
	        self.databaseView.column("block_section", width=100)
	        self.databaseView.column("block_manager", width=100)
	        self.databaseView.column("room_number", width=100)
	        self.databaseView.column("room_type", width=100)
	        self.databaseView.column("room_fee", width=100)


	        for record in data:
	            self.databaseView.insert('', 'end', values=(record))

	        self.databaseViewWindow.mainloop()

	class StatisticsView:
	    def __init__(self, data):
	        self.statisticsViewWindow = tkinter.Tk()
	        self.statisticsViewWindow.wm_title("Statistics View")

	        # Label widgets

	        tkinter.Label(self.statisticsViewWindow, text="Statistics View Window", width=25).grid(pady=8, column=1, row=1)
	        self.statisticsView = tkinter.ttk.Treeview(self.statisticsViewWindow)
	        self.statisticsView.grid(pady=8, column=1, row=2)
	        self.statisticsView["show"] = "headings"
	        self.statisticsView["columns"] = ("a","b","c")

	        # Treeview column headings

	        self.statisticsView.heading("a", text="Description")
	        self.statisticsView.heading("b", text="Value")
	        self.statisticsView.heading("c", text="Retiree")


	        self.statisticsView.column("a", width=120)
	        self.statisticsView.column("b", width=120)
	        self.statisticsView.column("c", width=120)

	        for record in data[0]:
	            self.statisticsView.insert('', 'end', value=("Average room fee",round(np.mean(data),2)))
	            self.statisticsView.insert('', 'end', value=("Max room fee",max(data),maxf))
	            self.statisticsView.insert('', 'end', value=("Min room fee",min(data),minf))
	            self.statisticsView.insert('', 'end', value=("SD for room fee",round(np.std(data),2)))
	            self.statisticsView.insert('', 'end', value=("IQR for room fee",np.subtract(*np.percentile(data, [75, 25]))))


	        self.statisticsViewWindow .mainloop()

	class SearchDeleteWindow:
	    def __init__(self, task):
	        self.window = tkinter.Tk()
	        self.window.wm_title(task + " data")

	        # Initializing all the variables

	        self.id = tkinter.StringVar()
	        self.name = tkinter.StringVar()
	        self.last_name = tkinter.StringVar()
	        self.heading = "Please enter Retiree info to " + task

	        # Labels

	        tkinter.Label(self.window, text=self.heading, width=50).grid(pady=5, row=1)
	        tkinter.Label(self.window, text="Name", width=50).grid(pady=10, row=2)
	        tkinter.Label(self.window, text="Last name", width=50).grid(pady=5, row=4)

	        # Entry widgets

	        self.nameEntry = tkinter.Entry(self.window, width=15, textvariable=self.name)
	        self.nameEntry.grid(pady=5, row=3)
	        self.last_nameEntry = tkinter.Entry(self.window, width=15, textvariable=self.last_name)
	        self.last_nameEntry.grid(pady=5, row=6)

	        # Button widgets

	        if (task == "Search"):
	            tkinter.Button(self.window, width=20, text=task, command=self.Search).grid(pady=8, row=7)
	        elif (task == "Delete"):
	            tkinter.Button(self.window, width=20, text=task, command=self.Delete).grid(pady=8, row=7)

	    def Search(self):
	        self.database = Database()
	        self.data = self.database.Search(self.nameEntry.get(),self.last_nameEntry.get())
	        self.databaseView = DatabaseView(self.data)

	    def Delete(self):
	        self.database = Database()
	        self.database.Delete(self.nameEntry.get(),self.last_nameEntry.get())
	        tkinter.messagebox.showinfo("Deleted data", "Successfully Deleted the Retiree data from the database")



	class HomePage:
	    def __init__(self):
	        self.homePageWindow = tkinter.Tk()
	        self.homePageWindow.wm_title("Retiree Information Home Page")
	        self.homePageWindow.configure(bg = "gray20")
	        bg_color = "dodger blue"
	        fg_color = "gray97"
	        lbl_color = 'GREEN'
	        tkinter.Label(self.homePageWindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color, text="Home Page", font=("Helvetica",20,"bold"), width=50).grid(pady=11,columnspan=8)

	        tkinter.Button(self.homePageWindow, width=10, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color, text="Retiree", font=("Helvetica",15,"bold"), command=self.Insert).grid(pady=11, column=1, row=1)
	        tkinter.Button(self.homePageWindow, width=10, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color, text="Offspring", font=("Helvetica",15,"bold"), command=self.InsertOff).grid(pady=11, column=2, row=1)
	        tkinter.Button(self.homePageWindow, width=10, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color, text="Address", font=("Helvetica",15,"bold"), command=self.InsertAdd).grid(pady=11, column=3, row=1)
	        tkinter.Button(self.homePageWindow, width=10, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color, text="Block", font=("Helvetica",15,"bold"), command=self.InsertBlock).grid(pady=11, column=4, row=1)
	        tkinter.Button(self.homePageWindow, width=10, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color, text="Room", font=("Helvetica",15,"bold"), command=self.InsertRoom).grid(pady=11, column=5, row=1)

	        tkinter.Button(self.homePageWindow, width=20, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color, text="Search", font=("Helvetica",15,"bold"), command=self.Search).grid(pady=11, column=1, row=2, columnspan=5)
	        tkinter.Button(self.homePageWindow, width=20, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color, text="Update", font=("Helvetica",15,"bold"), command=self.Update).grid(pady=11, column=1, row=3, columnspan=5)
	        tkinter.Button(self.homePageWindow, width=20, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color, text="Delete", font=("Helvetica",15,"bold"), command=self.Delete).grid(pady=11, column=1, row=4, columnspan=5)
	        tkinter.Button(self.homePageWindow, width=20, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color, text="Display", font=("Helvetica",15,"bold"), command=self.Display).grid(pady=11, column=1,row=5, columnspan=5)
	        tkinter.Button(self.homePageWindow, width=20, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color, text="Statistics", font=("Helvetica",15,"bold"), command=self.statistics).grid(pady=11, column=1,row=6, columnspan=5)
	        tkinter.Button(self.homePageWindow, width=20, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color, text="Exit", font=("Helvetica",15,"bold"), command=self.homePageWindow.destroy).grid(pady=11,column=1,row=7, columnspan=5)

	        

	        self.homePageWindow.mainloop()

	    def Insert(self):
	        self.insertWindow = InsertWindow()

	    def InsertAdd(self):
	        self.insertWindow = InsertWindowAdd()

	    def InsertOff(self):
	        self.insertWindow = InsertWindowOff()

	    def InsertBlock(self):
	        self.insertWindow = InsertWindowBlock()

	    def InsertRoom(self):
	        self.insertWindow = InsertWindowRoom()

	    def Update(self):
	        self.updateIDWindow = tkinter.Tk()
	        self.updateIDWindow.wm_title("Update data")

	        # Initializing all the variables
	        self.ret_id = tkinter.StringVar()

	        # Label

	        tkinter.Label(self.updateIDWindow, text="Enter the retiree ID to update", width=50).grid(pady=10, row=1)

	        # Entry widgets

	        self.ret_id = tkinter.Entry(self.updateIDWindow, width=5, textvariable=self.ret_id)

	        self.ret_id.grid(pady=10, row=2)

	        # Button widgets

	        tkinter.Button(self.updateIDWindow, width=20, text="Update", command=self.updateID).grid(pady=5, row=3)

	        self.updateIDWindow.mainloop()

	    def updateID(self):
	        self.updateWindow = UpdateWindow(self.ret_id.get())
	        self.updateIDWindow.destroy()

	    def Search(self):
	        self.searchWindow = SearchDeleteWindow("Search")

	    def Delete(self):

	        self.deleteWindow = SearchDeleteWindow("Delete")


	    def Display(self):
	        self.database = Database()
	        self.data = self.database.Display()
	        self.displayWindow = DatabaseView(self.data)

	    def statistics(self):
	        self.database = Database()
	        self.data = self.database.statistics()
	        self.displayWindow = StatisticsView(self.data)

	    def maxfee(self):
	        self.database = Database()
	        self.data = self.database.maxfee()
	        self.displayWindow = StatisticsView(self.data)    	


	homePage = HomePage()



# Designing window for registration
 
def register():
    global register_screen
    register_screen = Toplevel(main_screen)
    register_screen.title("Register")
    register_screen.geometry("300x250")
 
    global username
    global password
    global username_entry
    global password_entry
    username = StringVar()
    password = StringVar()
 
    Label(register_screen, text="Please enter details to register").pack(pady = 5)
    Label(register_screen, text="").pack()
    username_lable = Label(register_screen, text="Username * ")
    username_lable.pack()
    username_entry = Entry(register_screen, textvariable=username)
    username_entry.pack()
    password_lable = Label(register_screen, text="Password * ")
    password_lable.pack()
    password_entry = Entry(register_screen, textvariable=password, show='*')
    password_entry.pack()
    Label(register_screen, text="").pack()
    Button(register_screen, text="Register", width=10, font=("Helvetica",10,"bold"),fg="ghost white", bg="dodger blue",height=1, command = register_user).pack()
 
 
# Designing window for login 
 
def login():
    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.title("Login")
    login_screen.geometry("300x250")
    Label(login_screen, text="Please enter details to login").pack(pady = 5)
    Label(login_screen, text="").pack()
 
    global username_verify
    global password_verify
 
    username_verify = StringVar()
    password_verify = StringVar()
 
    global username_login_entry
    global password_login_entry
 
    Label(login_screen, text="Username * ").pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.pack()
    Label(login_screen, text="").pack()
    Label(login_screen, text="Password * ").pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify, show= '*')
    password_login_entry.pack()
    Label(login_screen, text="").pack()
    Button(login_screen, text="Login", width=10, font=("Helvetica",10,"bold"),fg="ghost white", bg="dodger blue",height=1, command = login_verify).pack()


 
# Implementing event on register button
 
def register_user():
 
    username_info = username.get()
    password_info = password.get()
 
    file = open(username_info, "w")
    file.write(username_info + "\n")
    file.write(password_info)
    file.close()
 
    username_entry.delete(0, END)
    password_entry.delete(0, END)
 
    Label(register_screen, text="Registration Success", fg="green", font=("Helvetica", 13)).pack()
 
# Implementing event on login button 
 
def login_verify():
    username1 = username_verify.get()
    password1 = password_verify.get()
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)
 
    list_of_files = os.listdir()
    if username1 in list_of_files:
        file1 = open(username1, "r")
        verify = file1.read().splitlines()
        if password1 in verify:
            login_sucess()
            start()
 
        else:
            password_not_recognised()
 
    else:
        user_not_found()
 
# Designing popup for login success
 
def login_sucess():
    global login_success_screen
    login_success_screen = Toplevel(login_screen)
    login_success_screen.title("Success")
    login_success_screen.geometry("150x100")
    Label(login_success_screen, text="Login Success").pack(pady = 10)
    Button(login_success_screen, text="OK", font=("Helvetica",10,"bold"),fg="ghost white", bg="dodger blue",height=1,command=delete_login_success).pack()

 
# Designing popup for login invalid password
 
def password_not_recognised():
    global password_not_recog_screen
    password_not_recog_screen = Toplevel(login_screen)
    password_not_recog_screen.title("Success")
    password_not_recog_screen.geometry("150x100")
    Label(password_not_recog_screen, text="Invalid Password ").pack(pady=15)
    Button(password_not_recog_screen, font=("Helvetica",10,"bold"),fg="ghost white", bg="dodger blue",height=1,text="OK", command=delete_password_not_recognised).pack()
 
# Designing popup for user not found
 
def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(login_screen)
    user_not_found_screen.title("Success")
    user_not_found_screen.geometry("150x100")
    Label(user_not_found_screen, text="User Not Found").pack(pady=15)
    Button(user_not_found_screen, text="OK", font=("Helvetica",10,"bold"),fg="ghost white", bg="dodger blue",height=1 ,command=delete_user_not_found_screen).pack()
 
# Deleting popups
 
def delete_login_success():
    login_success_screen.destroy()
 
 
def delete_password_not_recognised():
    password_not_recog_screen.destroy()
 
 
def delete_user_not_found_screen():
    user_not_found_screen.destroy()
 
 
# Designing Main(first) window
 
def main_account_screen():
    global main_screen
    main_screen = Tk()
    main_screen.geometry("300x250")
    main_screen.title("Account Login")
    main_screen.configure(bg = "gray20")
    Label(text="Please select", fg="gray97",bg="dodger blue", width="500", height="2", font=("Helvetica", 13,"bold")).pack()
 
    Button(fg="gray97", bg="dodger blue", text="Login", font=("Helvetica",13,"bold"), height="2", width="20", command = login).pack(padx = 10, pady=30)
    #Label(text="").pack()
    Button(fg="gray97", bg="dodger blue", text="Register", font=("Helvetica",13,"bold"), height="2", width="20", command=register).pack(padx=10)
    #Button(self.homePageWindow, width=20, relief=tkinter.GROOVE, , command=self.homePageWindow.destroy).grid(pady=11,column=1,row=7, columnspan=5)
    main_screen.mainloop()
 
 
main_account_screen()

