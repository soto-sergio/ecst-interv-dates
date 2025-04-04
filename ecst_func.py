import time
import pandas as pd
import pickle as pkl
from datetime import datetime
from tkcalendar import DateEntry
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import tkinter as tk

# Global Variables
username, password, intervention, selectedDates = "", "", "", []
homeroom_dict = {}

# Data Preprocessing (unchanged)
def csv_to_dict(csv_path: str, key_col: int, value_col: int):
    """Convert CSV to dictionary and save as pickle."""
    df = pd.read_csv(csv_path, header=None)
    data_dict = df.set_index(key_col)[value_col].to_dict()

    with open("data/clean/hr_dict.pkl", "wb") as f:
        pkl.dump(data_dict, f)

    return data_dict

def load_dict(pkl_file: str):
    """Load dictionary from pickle file."""
    with open(pkl_file, "rb") as f:
        return pkl.load(f)

def get_dict(dict_callback):
    """Store dictionary globally for later use."""
    global homeroom_dict
    homeroom_dict = dict_callback

# Selenium Automation
def auto_mate_test(final_attendance):
    """Automate data entry using Selenium."""
    minutes = 45

    print(f"Hi {username}, you want to document a {intervention} intervention on {selectedDates}")

    # Open browser and login
    time.sleep(3)
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get("https://access.austinisd.org/ACM/agreement.htm")
    
    wait = WebDriverWait(driver, 10)
    driver.find_element(By.ID, "uname").send_keys(username)
    driver.find_element(By.ID, "pwd").send_keys(password)
    driver.find_element(By.ID, "ecstSubmit").click()
    time.sleep(2)
    # Navigate to student search
    driver.find_element(By.XPATH, '//*[@id="inner"]/form/input[1]').click()


   # Process each student
    for student_id in final_attendance:
        driver.find_element(By.XPATH, '//*[@id="searchTable"]/tbody/tr[3]/td/input').send_keys(student_id)
        driver.find_element(By.XPATH, '//*[@id="searchTable"]/tbody/tr[7]/th/input').click()
        time.sleep(2)

    # Select intervention type
        #try:
        #    if intervention == "Math":
        #        try:
        #             link = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="inner"]/table[4]/tbody/tr[2]/td[1]/div[5]/ul/li[1]/a')))
        #             link.click()
        #         except Exception:
        #             link = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="inner"]/table[4]/tbody/tr[2]/td[1]/div[6]/ul/li[1]/a')))
        #             link.click()
        #     else:  # Reading intervention
        #         try:
        #             link = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="inner"]/table[4]/tbody/tr[2]/td[1]/div[5]/ul/li[2]/a')))
        #             link.click()
        #         except Exception:
        #             link = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="inner"]/table[4]/tbody/tr[2]/td[1]/div[6]/ul/li[2]/a')))
        #             link.click()
        # except Exception:
        #     print("Intervention link not found.")
        #     continue  # Skip to the next student if the intervention link is missing
        try:
            if intervention == "Math":
                link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'aipEdit.htm') and contains(@href, 'type=M')]")))
            else:  # Reading intervention
                link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'aipEdit.htm') and contains(@href, 'type=R')]")))

            link.click()
        except Exception:
            print(f"Intervention link not found for student {student_id}. Skipping to next student.")
            continue  # Skip to the next student if the intervention link is missing


    # Process all date batches before moving to the next student
        
       # Process dates in batches of 5
        for i in range(0, len(selectedDates), 5):
            batch = selectedDates[i:i + 5]
            k = 0  # Reset k for each batch

            for date in batch:
                while True:
                    try:
                        # Wait for the date field to be visible and interactable
                        date_box = wait.until(EC.visibility_of_element_located((By.NAME, f'aipMeetingMinutesDateList[{k}].aipMeetingMinutesDate')))

                        # Check if the field is empty and then fill it
                        if not date_box.get_attribute("value"):
                            date_box.send_keys(date)
                            driver.find_element(By.NAME, f'aipMeetingMinutesDateList[{k}].aipMeetingMinutes').send_keys(minutes)
                            k += 1  # Move to the next field after filling this one
                            break  # Break the inner while loop after entering the date
                        else:
                            k += 1  # If field is filled, check the next one
                    except Exception as e:
                        print(f"Error while processing date field: {e}")
                        time.sleep(1)  # Wait a bit before retrying
                        continue  # Continue to the next date field attempt

            # Save after every batch of 5 dates
            try:
                time.sleep(3)
                save_button = driver.find_element(By.XPATH, "//input[@name='action'][@value='Save']")
                save_button.click()
                time.sleep(2)  # Wait for save action to complete

                # Ensure we're still on the same page before entering the next batch
                wait.until(EC.presence_of_element_located((By.NAME, f'aipMeetingMinutesDateList[0].aipMeetingMinutesDate')))
        
            except Exception as e:
                print(f"Error while saving: {e}")
                break  # If saving fails, break the loop to stop further processing

    # Final save after entering all dates
        try:
            time.sleep(3)
            save_button = driver.find_element(By.XPATH, "//input[@name='action'][@value='Save']")
            save_button.click()
            time.sleep(2)  # Ensure the final save is completed
        except Exception as e:
            print(f"Error while saving for the student: {e}")

    # Move to next student only after all dates are entered
        try: 
            time.sleep(3)
            # Scroll and click the homepage link to go back
            logo_link = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/table[1]/tbody/tr[1]/td[1]/a')))
            driver.execute_script("arguments[0].scrollIntoView();", logo_link)
            logo_link.click()
            print(f"Returned to the homepage after processing student {student_id}.")
        except Exception as e:
            print(f"Error navigating back to home for student {student_id}: {e}")
            break  # If it fails to return to home, stop further processing
    
    driver.quit()  # Close the browser after processing all students

# GUI Functions
def get_login_input():
    """Retrieve login details from user input."""
    global username, password, intervention, selectedDates
    username = user_entry.get()
    password = password_entry.get()
    intervention = intervention_entry.get()  # Get selected intervention (Math or Reading)
    selectedDates = date_listbox.get(0, tk.END)  # Get all selected dates from the Listbox

    window2(mainframe, "#152D2E")

def continue_button():
    """Process attendance selection and start automation."""
    final_attendance = [k for k, var in zip(homeroom_dict.keys(), attendance_var) if var.get()]
    auto_mate_test(final_attendance)

def cancel_button():
    """Exit the application."""
    exit()

def destroy_frames():
    """Destroy existing GUI elements."""
    for widget in mainframe.winfo_children():
        widget.destroy()

# GUI Windows
def window1(frame1, bg_color):
    """Login window."""
    global user_entry, password_entry, intervention_entry, calendar_entry, date_listbox

    frame1.pack()
    tk.Label(frame1, text="eCST Login", bg=bg_color, fg='#DDFFE7', font=("TkMenuFonto", 14)).pack(pady=5)

    tk.Label(frame1, text="E Number:", bg=bg_color, fg="white").pack(pady=10)
    user_entry = tk.Entry(frame1, width=20)
    user_entry.pack()

    tk.Label(frame1, text="Password:", bg=bg_color, fg="white").pack(pady=10)
    password_entry = tk.Entry(frame1, width=20, show="*")
    password_entry.pack()

    tk.Label(frame1, text="Intervention:", bg=bg_color, fg="white").pack(pady=10)
    intervention_entry = tk.StringVar(value='- Select -')
    tk.OptionMenu(frame1, intervention_entry, "Math", "Reading").pack()

    tk.Label(frame1, text="Dates:", bg=bg_color, fg="white").pack(pady=10)
    
    # Date Entry and Listbox for selected dates
    date_entry = DateEntry(frame1, selectmode='day', date_pattern='mm/dd/yyyy')
    date_entry.pack()

    def add_date():
        """Add selected date to the listbox."""
        selected_date = date_entry.get()
        if selected_date:
            date_listbox.insert(tk.END, selected_date)

    def remove_date():
        """Remove selected date from the listbox."""
        try:
            selected_index = date_listbox.curselection()
            date_listbox.delete(selected_index)
        except IndexError:
            pass

    # Buttons to add or remove dates
    tk.Button(frame1, text="Add Date", command=add_date).pack(pady=5)
    tk.Button(frame1, text="Remove Date", command=remove_date).pack(pady=5)

    # Listbox to display selected dates
    date_listbox = tk.Listbox(frame1, selectmode=tk.MULTIPLE, height=5, width=20)
    date_listbox.pack(pady=10)

    tk.Button(frame1, text="Login", command=get_login_input).pack(pady=10)

def window2(mainframe, bg_color):
    """Attendance selection window."""
    global attendance_var
    destroy_frames()

    tk.Label(mainframe, text="Homeroom Roster Attendance", bg=bg_color, fg='#DDFFE7').pack(pady=5)

    attendance_var = [tk.IntVar(value=1) for _ in homeroom_dict]  # Ensures all are defaulted to "Present"


    # Title Frames
    frame2  = tk.Frame(mainframe, bg =bg_color)
    frame2.tkraise()
    frame2.pack_propagate(True)
    tk.Label(frame2, text = "Homeroom Roster Attendance", bg=bg_color,fg='#DDFFE7', font = ("TkMenuFonto", 14)).pack(pady=5)   #Homeroom Roster Attendance -  Title Label
    tk.Label(frame2, text = selectedDates, bg = bg_color, fg = "light grey", font = ("TkMenuFonto", 12)).pack(pady = 10)   # Date Label
    frame2.pack()

    # Horizontal Frame with Labels Studen name, Present , Absent
    frame3 = tk.Frame(mainframe,bg=bg_color)
    tk.Label(frame3, text = "Student Name", width = 35 , bg='light grey',padx = 10, pady =10 ).grid(row=0, column=0, padx=5, pady=10, sticky = "nsew")
    tk.Label(frame3, text = "Present / Absent", width = 30,  bg='light grey',padx = 10, pady =10 ).grid(row=0, column=1, padx=5, pady=10, sticky = "nsew")
    
    frame3.grid_columnconfigure(0,weight = 1)
    frame3.grid_columnconfigure(1,weight = 1)
    frame3.pack(fill = "x")

    # Grid data with Student Name, and RoundButtons
    homeroom_roster = homeroom_dict
    frame4 = tk.Frame(mainframe,bg='#152D2E')
    
    attendance_var = [tk.IntVar() for j in range(len(homeroom_roster))]
    k = 0
    for i in homeroom_roster:
        stu_label = tk.Label(frame4, text = homeroom_roster[i], bg='#152D2E', fg = "light grey", font = ("TkMenuFonto", 10))
        stu_label.grid(row = k, column = 0, sticky = "w", padx = 10)
        # Create buttons
        b1 = tk.Radiobutton(frame4, variable =attendance_var[k], activebackground ='#152D2E',activeforeground='light grey', selectcolor='black', bg='#152D2E', fg = 'light grey', text = "Present", value = 1).grid(row = k, column = 1, sticky = "nsew", padx = 10)        # Present
        b2 = tk.Radiobutton(frame4, variable =attendance_var[k], activebackgroun='#152D2E', activeforeground='light grey', selectcolor='black' , bg='#152D2E',fg = 'light grey',text = "Absent", value = 0).grid(row = k, column = 2 , sticky = "nsew", padx = 5)         # Absent
        attendance_var[k].set(1)
        k = k+1

    frame4.grid_columnconfigure(0,weight = 1)
    frame4.grid_columnconfigure(1,weight = 1)
    frame4.grid_columnconfigure(2,weight = 1)
    frame4.pack(fill="x")
    
    frame5 = tk.Frame(mainframe,bg=bg_color)
    tk.Button(frame5, text= "Continue", command = continue_button, bg='light grey').grid(row=0, column = 1, pady = 20 , padx = 100, sticky = "nesw" )
    tk.Button(frame5, text= "Cancel", command = cancel_button, bg = 'light grey').grid(row = 0, column =0, pady=20 ,padx = 100, sticky = "nesw" )
    
    frame5.grid_columnconfigure(0,weight = 1)
    frame5.grid_columnconfigure(1,weight = 1)
    frame5.pack(fill="x")


## Main frame tkinter
def tk_root():
    global mainframe, frame1, bg_color
    root= tk.Tk()
    #root.resizable(False, False)
    bg_color = "#3d6466"
    mainframe = tk.Frame(root, bg= bg_color)
    mainframe.pack(fill= "both", expand = True)
    frame1  = tk.Frame(mainframe , width= 400 , height = 600, bg=bg_color)
    window1(frame1 , bg_color)

    root.mainloop()