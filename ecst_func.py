#### Import
import time
import pandas as pd
import pickle as pkl # to save dictionaries as py file
from datetime import datetime
from tkcalendar import DateEntry
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import tkinter as tk

#### Global variables
username = ""
password = ""

#### Data Preprocessing
## Convert to dictionary and save as py file. student_id : student_name

def csv_to_dict(csv_path: str, key_col: int, value_col: int):
    df = pd.read_csv(csv_path, index_col=None, header=None)
    data_dict = df.set_index(key_col)[value_col].to_dict()
    # Save dictionary
    with open("data/clean/hr_dict.pkl","wb") as f:   #wb mode (write binary)
        pkl.dump(data_dict, f)
    return data_dict

def load_dict(pkl_file: str):
    with open(pkl_file, "rb") as f:   #read binary
         dict = pkl.load(f)
    return dict   

####---------------------------------------------------------------------------------------------------------------------

#### Automatization with Selenium
def auto_mate_test(final_attendance):

    # Intervention minutes
    minutes = 30
    print('Hi ' +username + ' from auto_mate_test. You want to document a ' + intervention + ' intervention on ' + selectedDate)
    homeroom_roster = homeroom_dict
    
    # eCST Login
    time.sleep(3)
    driver = webdriver.Chrome('chromedriver.exe')
    wait = WebDriverWait(driver, 2)
    website = driver.get("https://access.austinisd.org/ACM/agreement.htm") 
    driver.find_element_by_xpath('//*[@id="uname"]').send_keys(username)  # Pass username
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="pwd"]').send_keys(password)    # Pass password
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="ecstSubmit"]').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="inner"]/form/input[1]').click()
     # Math Intervention
    if intervention == "Math":
        for i in final_attendance:
            driver.find_element_by_xpath('//*[@id="searchTable"]/tbody/tr[3]/td/input').send_keys(i)
            time.sleep(2)
            driver.find_element_by_xpath('//*[@id="searchTable"]/tbody/tr[7]/th/input').click()
            time.sleep(2)
            driver.find_element_by_xpath('//*[@id="inner"]/table[4]/tbody/tr[2]/td[1]/div[5]/ul/li[2]/a').click()
            time.sleep(2)

            # Check for empty box
            k = 0
            check_box = driver.find_element_by_name('aipMeetingMinutesDateList[' + str(k) + '].aipMeetingMinutesDate')
            check_value = check_box.get_attribute('value')


            if (check_value == ""):
                 driver.find_element_by_name('aipMeetingMinutesDateList[' + str(k) + '].aipMeetingMinutesDate').send_keys(selectedDate) # Date Box
                 driver.find_element_by_name('aipMeetingMinutesDateList[' + str(k) + '].aipMeetingMinutes').send_keys(minutes)  # Minutes Box  
                 time.sleep(2)
                 driver.find_element_by_xpath('//*[@id="aipForm"]/div[3]/input').click()   # Save
                 driver.find_element_by_xpath('//*[@id="logo"]').click()     # Go to student search page   
            else:
                k = k+1
                while (check_value !=""):
                     check_box = driver.find_element_by_name('aipMeetingMinutesDateList[' + str(k) + '].aipMeetingMinutesDate')
                     check_value = check_box.get_attribute('value')
                     k = k+1
                else:
                    driver.find_element_by_name('aipMeetingMinutesDateList[' + str(k) + '].aipMeetingMinutesDate').send_keys(selectedDate) # Date Box
                    driver.find_element_by_name('aipMeetingMinutesDateList[' + str(k) + '].aipMeetingMinutes').send_keys(minutes)  # Minutes Box  
                    time.sleep(3)
                    driver.find_element_by_xpath('//*[@id="aipForm"]/div[3]/input').click()   # Save
                    driver.find_element_by_xpath('//*[@id="logo"]').click()     # Go to student search page   

    # Reading Intervention
    if intervention == "Reading":
        for i in final_attendance:
            driver.find_element_by_xpath('//*[@id="searchTable"]/tbody/tr[3]/td/input').send_keys(i)
            time.sleep(2)
            driver.find_element_by_xpath('//*[@id="searchTable"]/tbody/tr[7]/th/input').click()
            time.sleep(2)
            driver.find_element_by_xpath('//*[@id="inner"]/table[4]/tbody/tr[2]/td[1]/div[5]/ul/li[1]/a').click()
            time.sleep(2)

            # Check for empty box
            k = 0
            check_box = driver.find_element_by_name('aipMeetingMinutesDateList[' + str(k) + '].aipMeetingMinutesDate')
            check_value = check_box.get_attribute('value')


            if (check_value == ""):
                 driver.find_element_by_name('aipMeetingMinutesDateList[' + str(k) + '].aipMeetingMinutesDate').send_keys(selectedDate) # Date Box
                 driver.find_element_by_name('aipMeetingMinutesDateList[' + str(k) + '].aipMeetingMinutes').send_keys(minutes)  # Minutes Box  
                 time.sleep(2)
                 driver.find_element_by_xpath('//*[@id="aipForm"]/div[3]/input').click()   # Save
                 driver.find_element_by_xpath('//*[@id="logo"]').click()     # Go to student search page   
            else:
                k = k+1
                while (check_value !=""):
                     check_box = driver.find_element_by_name('aipMeetingMinutesDateList[' + str(k) + '].aipMeetingMinutesDate')
                     check_value = check_box.get_attribute('value')
                     k = k+1
                else:
                    driver.find_element_by_name('aipMeetingMinutesDateList[' + str(k) + '].aipMeetingMinutesDate').send_keys(selectedDate) # Date Box
                    driver.find_element_by_name('aipMeetingMinutesDateList[' + str(k) + '].aipMeetingMinutes').send_keys(minutes)  # Minutes Box  
                    time.sleep(2)
                    driver.find_element_by_xpath('//*[@id="aipForm"]/div[3]/input').click()   # Save
                    driver.find_element_by_xpath('//*[@id="logo"]').click()     # Go to student search page  

    driver.close()
    cancel_button()

#### Functions for GUI
## Date
def cur_date():
    global date
    date = datetime.today().strftime('%m/%d/%Y')

## Get dictionary with homeroom roster data       
def get_dict(dict_callback):
    global homeroom_dict
    homeroom_dict = dict_callback 

## Get login input entered in window 1
def get_login_input():
    global username, password, intervention, input_array, selectedDate
    username = user_entry.get()
    password = password_entry.get()
    intervention =intervention_entry.get()
    inputs_array  = [username, password, intervention]
    selectedDate = calendar_entry.get()
    # Attendance frame
    window2(mainframe, bg_color)

## Button Actions
def cancel_button():
    return exit()
    
def continue_button():
    final_attendance=[]
    
    a = [int(i.get()) for i in attendance_var]
    l = 0
    for x in homeroom_dict:
        if a[l] == 1:
            final_attendance.append(x)
            l = l+1
        else:
            l = l+1
    #print(final_attendance)     
    auto_mate_test(final_attendance)

## Destroy frame to transition from window1 to window2
def destroy_frames():
    for widget in mainframe.winfo_children():
        widget.destroy()


####---------------------------------------------------------------------------------------------------------------------
#### GUI
## Attendance Window
def window2(mainframe, bg_color):
    global attendance_var
    destroy_frames()
    cur_date()
    # Title Frames
    frame2  = tk.Frame(mainframe, bg =bg_color)
    frame2.tkraise()
    frame2.pack_propagate(True)
    tk.Label(frame2, text = "Homeroom Roster Attendance", bg=bg_color,fg='#DDFFE7', font = ("TkMenuFonto", 14)).pack(pady=5)   #Homeroom Roster Attendance -  Title Label
    tk.Label(frame2, text = selectedDate, bg = bg_color, fg = "light grey", font = ("TkMenuFonto", 12)).pack(pady = 10)   # Date Label
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

## Login Window
def window1(frame1,bg_color):
    global user_entry, password_entry, intervention_entry, calendar_entry
    ### frame1 widgets
    frame1.pack()
    frame1.pack_propagate(False) 
    cur_date()
    

    tk.Label(  frame1, text = "eCST Login", bg=bg_color, fg='#DDFFE7' ,font = ("TkMenuFonto", 14)).pack(pady = 5)       # ecst Login - Title Label
    ### E number
    tk.Label(  frame1, text = "E Number: ", bg = bg_color, fg = "white", font = ("TkMenuFonto", 12)).pack(pady = 10)   
    user_entry = tk.Entry(  frame1, bg='white', width = 20)
    user_entry.pack(pady = 5)
    
    ### Password
    tk.Label(  frame1, text = "Password: ", bg = bg_color, fg = "white", font = ("TkMenuFonto", 12)).pack(pady = 10)
    password_entry = tk.Entry(  frame1, bg='white', width = 20, show = "*")
    password_entry.pack(pady = 5)

    ### Intervention
    tk.Label( frame1, text = "Intervention: ", bg = bg_color, fg = "white", font = ("TkMenuFonto", 12)).pack(pady = 10)
    intrvOptions = ['- Select -','Math', 'Reading']  
    intervention_entry = tk.StringVar(value = intrvOptions[0])                             
    dropdownIntrv = tk.OptionMenu( frame1, intervention_entry, *intrvOptions)
    dropdownIntrv.pack(pady = 5)     #Store credentials and intervention selection in an array

    #### Date 
    
    tk.Label( frame1, text = "Date: ", bg = bg_color, fg = "white", font = ("TkMenuFonto", 12)).pack(pady = 10)
    calendar_entry = DateEntry(frame1, selectmode ='day', date_pattern='mm/dd/yyyy')  
    calendar_entry.pack(pady=5)

    ## Login Button (New)        
    login_button= tk.Button( frame1, text = "Login",bg='light grey'  , command = get_login_input)
    login_button.pack(pady = 30)
    
## Main frame tkinter
def tk_root():
    global mainframe, frame1, bg_color
    root= tk.Tk()
    #root.resizable(False, False)
    bg_color = "#3d6466"
    mainframe = tk.Frame(root, bg= bg_color)
    mainframe.pack(fill= "both", expand = True)
    frame1  = tk.Frame(mainframe , width= 300 , height = 500, bg=bg_color)
    window1(frame1 , bg_color)

    root.mainloop()

#### -------------------------------------------------------------------------------------------------