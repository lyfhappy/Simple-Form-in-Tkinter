from tkinter import *
from tkinter import messagebox
import mysql.connector


# Connect to the MySQL database
db_connection = mysql.connector.connect(
    host="127.0.0.1",     # e.g., localhost or IP
    user="root",     # e.g., root
    password="299792458sS@", # Your password
    database="testdb"  # Name of your database
)


def submit_form():
    name = name_entry.get()
    mobile = mobile_entry.get()
    gender = gender_var.get()
    selected_course = course_var.get()
    selected_grade = grade_var.get()
    
    # Validation
    if not name or not mobile:
        messagebox.showerror("Input Error", "Please fill out Name and Mobile Number.")
        return
    if not selected_course:
        messagebox.showerror("Input Error", "Please select a course.")
        return
    if selected_grade == "Select Grade":
        messagebox.showerror("Input Error", "Please select a grade.")
        return
    if not gender:
        messagebox.showerror("Input Error", "Please select your gender.")
        return

    # Display user input in a message box
    user_info = (
        f"Name: {name}\n"
        f"Mobile Number: {mobile}\n"
        f"Gender: {gender}\n"
        f"Selected Course: {selected_course}\n"
        f"Selected Grade: {selected_grade}"
    )
    messagebox.showinfo("Submitted Details", user_info)
    try:
        cursor = db_connection.cursor()
        sql1 = "INSERT INTO personalinfo(name,mobile_num,grade,gender,Misc) VALUES (%s, %s, %s, %s, %s)"
        val1 = (name,mobile,selected_grade,gender,selected_course)
        cursor.execute(sql1, val1)

        db_connection.commit()
    except mysql.connector.Error as error:
        print(f"Error: {error}")
        db_connection.rollback()
    
    finally :
        # Close the connection
        print(f"Data Inserted: {cursor.lastrowid}")
        cursor.close()
    
def search_form():
    name1 = name_entry.get()
    mobile1 = mobile_entry.get()
    # Validation
    #if not name1 or not mobile1:
        #messagebox.showerror("Input Error", "Please fill out Name and Mobile Number.")
        #return
    try:
       cursor = db_connection.cursor()

        # Build SQL query dynamically
       sql = "SELECT name, mobile_num, grade, gender, Misc FROM personalinfo WHERE 1=1"
       if name1:
            sql += f" AND name LIKE '%{name1}%'"
       if mobile1:
            sql += f" AND mobile_num LIKE '%{mobile1}%'"

        # Execute the query
       cursor.execute(sql)
       myresult = cursor.fetchall()

        # Prepare results for display
       if not myresult:
            messagebox.showinfo("No Results", "No matching records found.")
       else:
            user_info = "\n".join(
                f"Name: {x[0]}, Mobile: {x[1]}, Grade: {x[2]}, Gender: {x[3]}, Misc: {x[4]}"
                for x in myresult
            )
            messagebox.showinfo("Search Results", user_info)
    except mysql.connector.Error as error:
        print(f"Error: {error}")
        db_connection.rollback()
    
    finally :
        cursor.close() 

#Create Main Window
window = Tk()
window.geometry("500x500")
window.resizable(False,False)
window.title("Mentors Eduserv")
window.config(bg="black")
# Create a cursor object to interact with the database
cursor = db_connection.cursor()

#Set Window Icon
try: 
  p1 = PhotoImage(file='MElogo.png')
  window.iconphoto(False,p1)
except TclError:
  print("MElogo.png not found. Ensure the file is in the same directory.")

#Creates a Border Around
# Inner frame (acts as the main content area)
inner_frame = Frame(window, bg="lightblue", bd=0)
inner_frame.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.98)  # Adjusted to leave a border around it

title_bar = Frame(inner_frame, relief="raised", bd=0)
title_bar.grid(row=0,column=0,columnspan=4,sticky="EW",padx=5,pady=5)

title_label = Label(title_bar, text="Admissions", bg="black",fg="white",anchor="center",font=("Arial",10))
title_label.grid(row=0,column=2,columnspan=2,sticky="EW",pady=5,padx=10)
# Configure column weights for the main window
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=2)
window.grid_columnconfigure(2, weight=1)

#Personal Details Section
details_label = Label(inner_frame,text="Personal Details",bg="lightblue",font=("Arial",10))
details_label.grid(row=1,column=0,columnspan=2,pady=10)

#Name Entry
name_label = Label(inner_frame,text="Name:",bg="lightblue", font=("Arial",8))
name_label.grid(row=2,column=0,sticky="e",padx=5,pady=5)
name_entry = Entry(inner_frame,width=30)
name_entry.grid(row=2,column=1,sticky="w",padx=5,pady=5)

#Mobile Number
mobile_entry = Label(inner_frame,text="Mobile Number:",bg="lightblue", font=("Arial",8))
mobile_entry.grid(row=3,column=0,sticky="e",padx=5,pady=5)
mobile_entry = Entry(inner_frame,width=30)
mobile_entry.grid(row=3,column=1,sticky="w",padx=5,pady=5)

#Course Selection 
course_label = Label(inner_frame, text="Select Course:", bg="lightblue", font=("Arial", 8))
course_label.grid(row=4, column=0, sticky="e", padx=5, pady=5)

#Course Selection Dropdown
course_var = StringVar()
course_var.set("Select Course")
courses = ["Engineering", "Medical","Foundation"]
grade_menu = OptionMenu(inner_frame,course_var, *courses)
grade_menu.config(width=26, bg="white", font=("Arial", 10))
grade_menu.grid(row=4, column=1, padx=5, pady=5)

#Grade Selection 
grade_label = Label(inner_frame, text="Select Grade:", bg="lightblue", font=("Arial", 8))
grade_label.grid(row=6, column=0, sticky="e", padx=5, pady=5)

#Grade Selection Dropdown
grade_var = StringVar()
grade_var.set("Select Grade")
grades = ["9th", "10th", "11th","12th","12th Passed"]
grade_menu = OptionMenu(inner_frame,grade_var, *grades)
grade_menu.config(width=26, bg="white", font=("Arial", 10))
grade_menu.grid(row=6, column=1, padx=5, pady=5)

#Gender Selection
gender_var = StringVar(inner_frame,value="Male")  # Holds the selected gender value
male_radiobutton = Radiobutton(inner_frame, text="Male", variable=gender_var, value="Male", bg="lightblue")
male_radiobutton.grid(row=8, column=1, sticky="w", padx=5)
female_radiobutton = Radiobutton(inner_frame, text="Female", variable=gender_var, value="Female", bg="lightblue")
female_radiobutton.grid(row=9, column=1, sticky="w", padx=5)

# Placeholder for Submit Button (optional)
submit_button = Button(inner_frame, text="Submit", bg="darkgreen", fg="white", font=("Arial", 12),command=submit_form)
submit_button.grid(row=10, column=0, sticky="EW",columnspan=2,pady=20,padx=5)

# Search Button 
search_button = Button(inner_frame,text="Search", bg="darkgreen", fg="white", font=("Arial", 12),command=search_form)
search_button.grid(row=10, column=2,sticky="E", columnspan=2,pady=20,padx = 5)

window.mainloop()
