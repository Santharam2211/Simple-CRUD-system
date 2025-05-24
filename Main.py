from tkinter import *
from tkinter import ttk, messagebox
from db import Database
import re
from PIL import Image, ImageTk

db = Database("Employee.db")
root = Tk()
root.title("Employee Management System")
root.geometry("1920x1080")
root.config(bg="#2c3e50")
root.state("zoomed")

name = StringVar()
age = StringVar()
doj = StringVar()
gender = StringVar()
email = StringVar()
contact = StringVar()

# Entries Frame
entries_frame = Frame(root, bg="#535c68")
entries_frame.pack(side=TOP, fill=X)

# Left form side
form_frame = Frame(entries_frame, bg="#535c68")
form_frame.grid(row=0, column=0, sticky="nw")

title = Label(form_frame, text="Employee Management System", font=("Calibri", 18, "bold"), bg="#535c68", fg="white")
title.grid(row=0, columnspan=2, padx=10, pady=20, sticky="w")

lblName = Label(form_frame, text="Name", font=("Calibri", 16), bg="#535c68", fg="white")
lblName.grid(row=1, column=0, padx=10, pady=10, sticky="w")
txtName = Entry(form_frame, textvariable=name, font=("Calibri", 16), width=30)
txtName.grid(row=1, column=1, padx=10, pady=10, sticky="w")

lblAge = Label(form_frame, text="Age", font=("Calibri", 16), bg="#535c68", fg="white")
lblAge.grid(row=1, column=2, padx=10, pady=10, sticky="w")
txtAge = Entry(form_frame, textvariable=age, font=("Calibri", 16), width=30)
txtAge.grid(row=1, column=3, padx=10, pady=10, sticky="w")

lbldoj = Label(form_frame, text="D.O.J", font=("Calibri", 16), bg="#535c68", fg="white")
lbldoj.grid(row=2, column=0, padx=10, pady=10, sticky="w")
txtDoj = Entry(form_frame, textvariable=doj, font=("Calibri", 16), width=30)
txtDoj.grid(row=2, column=1, padx=10, pady=10, sticky="w")

lblEmail = Label(form_frame, text="Email", font=("Calibri", 16), bg="#535c68", fg="white")
lblEmail.grid(row=2, column=2, padx=10, pady=10, sticky="w")
txtEmail = Entry(form_frame, textvariable=email, font=("Calibri", 16), width=30)
txtEmail.grid(row=2, column=3, padx=10, pady=10, sticky="w")

lblGender = Label(form_frame, text="Gender", font=("Calibri", 16), bg="#535c68", fg="white")
lblGender.grid(row=3, column=0, padx=10, pady=10, sticky="w")
comboGender = ttk.Combobox(form_frame, font=("Calibri", 16), width=28, textvariable=gender, state="readonly")
comboGender['values'] = ("Male", "Female", "Other")
comboGender.grid(row=3, column=1, padx=10, sticky="w")

lblContact = Label(form_frame, text="Contact No", font=("Calibri", 16), bg="#535c68", fg="white")
lblContact.grid(row=3, column=2, padx=10, pady=10, sticky="w")
txtContact = Entry(form_frame, textvariable=contact, font=("Calibri", 16), width=30)
txtContact.grid(row=3, column=3, padx=10, sticky="w")

lblAddress = Label(form_frame, text="Address", font=("Calibri", 16), bg="#535c68", fg="white")
lblAddress.grid(row=4, column=0, padx=10, pady=10, sticky="w")
txtAddress = Text(form_frame, width=85, height=5, font=("Calibri", 16))
txtAddress.grid(row=5, column=0, columnspan=4, padx=10, sticky="w")

# Image on right top
image_frame = Frame(entries_frame, bg="#535c68")
image_frame.grid(row=0, column=1, padx=20, pady=20, sticky="ne")

image = Image.open("D:/Project/picture.webp")  # Update path if needed
image = image.resize((500, 450))
photo = ImageTk.PhotoImage(image)
image_label = Label(image_frame, image=photo, bg="#535c68")
image_label.image = photo
image_label.pack()

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

def getData(event):
    selected_row = tv.focus()
    data = tv.item(selected_row)
    global row
    row = data["values"]
    name.set(row[1])
    age.set(row[2])
    doj.set(row[3])
    email.set(row[4])
    gender.set(row[5])
    contact.set(row[6])
    txtAddress.delete(1.0, END)
    txtAddress.insert(END, row[7])

def displayAll():
    tv.delete(*tv.get_children())
    for row in db.fetch():
        tv.insert("", END, values=row)

def add_employee():
    if (txtName.get() == "" or txtAge.get() == "" or txtDoj.get() == "" or 
        txtEmail.get() == "" or comboGender.get() == "" or txtContact.get() == "" or 
        txtAddress.get(1.0, END).strip() == ""):
        messagebox.showerror("Error", "Please fill all the details")
        return
    if len(txtContact.get()) != 10:
        messagebox.showerror("Error", "Enter 10-digit contact number")
        return
    if not is_valid_email(txtEmail.get()):
        messagebox.showerror("Error", "Invalid email format")
        return
    db.insert(txtName.get(), txtAge.get(), txtDoj.get(), txtEmail.get(), comboGender.get(), txtContact.get(),
              txtAddress.get(1.0, END).strip())
    messagebox.showinfo("Success", "Employee Added")
    clearAll()
    displayAll()

def update_employee():
    if (txtName.get() == "" or txtAge.get() == "" or txtDoj.get() == "" or 
        txtEmail.get() == "" or comboGender.get() == "" or txtContact.get() == "" or 
        txtAddress.get(1.0, END).strip() == ""):
        messagebox.showerror("Error", "Please fill all the details")
        return
    if len(txtContact.get()) != 10:
        messagebox.showerror("Error", "Enter 10-digit contact number")
        return
    if not is_valid_email(txtEmail.get()):
        messagebox.showerror("Error", "Invalid email format")
        return
    db.update(row[0], txtName.get(), txtAge.get(), txtDoj.get(), txtEmail.get(), comboGender.get(), txtContact.get(),
              txtAddress.get(1.0, END).strip())
    messagebox.showinfo("Success", "Record Updated")
    clearAll()
    displayAll()

def delete_employee():
    db.remove(row[0])
    clearAll()
    displayAll()

def clearAll():
    name.set("")
    age.set("")
    doj.set("")
    gender.set("")
    email.set("")
    contact.set("")
    txtAddress.delete(1.0, END)

# Button Frame
btn_frame = Frame(form_frame, bg="#535c68")
btn_frame.grid(row=6, column=0, columnspan=4, padx=10, pady=10, sticky="w")
Button(btn_frame, command=add_employee, text="Add", width=15, font=("Calibri", 16, "bold"), fg="white", bg="#16a085").grid(row=0, column=0)
Button(btn_frame, command=update_employee, text="Update", width=15, font=("Calibri", 16, "bold"), fg="white", bg="#2980b9").grid(row=0, column=1, padx=10)
Button(btn_frame, command=delete_employee, text="Delete", width=15, font=("Calibri", 16, "bold"), fg="white", bg="#c0392b").grid(row=0, column=2, padx=10)
Button(btn_frame, command=clearAll, text="Clear", width=15, font=("Calibri", 16, "bold"), fg="white", bg="#f39c12").grid(row=0, column=3, padx=10)

# Table Frame
tree_frame = Frame(root, bg="#ecf0f1")
tree_frame.place(x=0, y=500, width=1535, height=520)
style = ttk.Style()
style.configure("mystyle.Treeview", font=('Calibri', 14), rowheight=40)
style.configure("mystyle.Treeview.Heading", font=('Calibri', 15, "bold"))
tv = ttk.Treeview(tree_frame, columns=(1,2,3,4,5,6,7,8), style="mystyle.Treeview")
tv.heading("1", text="ID")
tv.heading("2", text="Name")
tv.heading("3", text="Age")
tv.heading("4", text="D.O.J")
tv.heading("5", text="Email")
tv.heading("6", text="Gender")
tv.heading("7", text="Contact")
tv.heading("8", text="Address")
for i in range(1, 9): tv.column(str(i), anchor=W)
tv['show'] = 'headings'
tv.bind("<ButtonRelease-1>", getData)
tv.pack(fill=BOTH, expand=True)

displayAll()
root.mainloop()

