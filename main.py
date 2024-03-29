from classes import University, Country
import tkinter as tk
from bs4 import BeautifulSoup
import csv
import datetime
from col import cost_of_living
import datetime

# --- Get date --- #

def get_current_date():
    current_date = datetime.date.today()
    return str(current_date)



# --- Calculations --- #
def cleanup_dollars(cost): # this function reformats the data stored in the csv file to be used in calculations:
    cost = cost.replace("Free", "0")
    cost = cost.replace("$", "")
    cost = cost.replace(",", "")
    cost = cost.replace("USD / year", "")
    cost = int(cost)
    return cost

def cleanup_duration(duration): # this function reformats the data stored in the csv file to be used in calculations:  
    duration = duration.replace("years", "")
    duration = duration.replace("year", "")
    duration = duration.replace(" ", "")
    duration = duration.replace("Â½", ".5")
    duration = float(duration)
    return duration

def cleanup_data(lst): # this function reformats the data stored in the csv file to be used in calculations:
    clean_dollar = cleanup_dollars(lst[0][3])
    clean_year = cleanup_duration(lst[0][4])
    lst[0][3] = clean_dollar
    lst[0][4] = clean_year
    return lst

# --- Functions --- #
def write_csv(school): # this function writes the list of list objects to a csv file
    with open("schools.csv", "a", newline='') as stream:
        writer = csv.writer(stream)
        writer.writerows(iter(school))



def read_csv(): # this function reads the csv file and prints it to the console
    with open("schools.csv", "r") as stream:
        reader = csv.reader(stream)
        for row in reader:
            print(row)

def create_list(list1, list2, list3, list4, list5): # this function creates a list of list objects of the Schools
    global uni_lists
    uni_lists = []
    for i in range(len(list1)):
        school = University(list1[i].text, list2[i].text, list3[i].text, list4[i].text, list5[i].text)
        uni_lists.append(school)
    return uni_lists

def scrape_data(website): # this function scrapes the data from an html (webstie) and writes it to a csv file
    with open(website, 'r') as html_file:
        content = html_file.read()
        soup = BeautifulSoup(content, 'lxml')
        university_list = soup.find_all('strong', class_='OrganisationName')
        university_locations = soup.find_all('strong', class_='OrganisationLocation')
        program_name = soup.find_all('h2', class_='StudyName')
        univeristy_costs = soup.find_all('div', class_=['TuitionValue', 'TuitionValueScholarshipDiscount'])
        uni_duration = soup.find_all('div', class_='DurationValue')
        create_list(university_list, university_locations, program_name, univeristy_costs, uni_duration)
        write_csv(uni_lists)
        return university_list, university_locations, program_name, univeristy_costs, uni_duration


def get_website(): # this function gets the website from the user--is html for now for safety reasons
    global website
    try:
        website = input_site.get("1.0", "end-1c")
        website != ""
        scrape_data(website)
        add_dropdown()
    except:
        raise ValueError("Please enter a valid website")

def get_list_options(): # this function gets the list of options for the drop down menu
    list_options = []
    with open("schools.csv", "r") as stream:
        if stream.readline() == "":
            no_data = ['No data']
            return no_data
        else:
            reader = csv.reader(stream)
            for row in reader:
                list_options.append(f"{row[0]}: {row[2]}")
        return list_options
    
def add_dropdown(): # this function adds the drop down menu to the GUI
        global clicked
        clicked = tk.StringVar()
        clicked.set("Select a program")
        global drop
        drop = tk.OptionMenu(m, clicked, *get_list_options())
        drop.grid(row=3, columnspan=7, sticky="ew")

def update_choice_label(list): # this function updates the choice label
    new_line = '\n'
    tab = '\t'
    cost = list[0][3] * list[0][4]
    cost = '{:,.2f}'.format(cost)
    display_choice_label.config(text=f"Program selected: {list[0][0]}: {list[0][2]}")
    display_duration_label.config(text=f"Duration: {list[0][4]} years")
    display_annual_tuition_label.config(text=f"Annual Tuition: ${'{:,.2f}'.format(list[0][3])}")
    display_col_label.config(text = f"{list[0][1]}")
    col_list = calculate_col(list, cost_of_living)
    if col_list == None:
        display_col_label.config(text = f"COL: No data")
        tuition_total= list[0][3] * list[0][4]
        display_tuition_label.config(text = f"Total tuition for years studying: ${'{:,.2f}'.format(-1*tuition_total)}")
        display_salary_label.config(text = f"Salary: No data")
        display_living_expenses_label.config(text = f"Living Expenses: No data")
    else:
        salary = (5-int(list[0][4]))*col_list[3]
        tuition_total= ((list[0][3] * list[0][4])*-1)
        living_expenses = (60*(col_list[1]+col_list[2])*-1)
        living_while_studying_expenses = tuition_total + ((living_expenses/5) * list[0][4])
        five_year_total = salary + tuition_total + living_expenses # this calculates the total cost of living for 5 years ((5-study years)*salary) - (5 * cost of living)-(tuition*years of study))
        display_tuition_label.config(text = f"Total tuition for years studying: ${'{:,.2f}'.format(tuition_total)}")
        display_salary_label.config(text = f"Total earnings for years working: ${'{:,.2f}'.format(salary)}")
        display_living_expenses_label.config(text = f"Living Expenses for all years: ${'{:,.2f}'.format(living_expenses)}")
        if five_year_total < 0:
            display_col_label.config(text = f"To begin, you'll need ${'{:,.2f}'.format(-1*living_while_studying_expenses)} prior to working to afford living expenses and tuition while studying. Over 5 years, the whole endeavor will have cost you ${'{:,.2f}'.format(-1*five_year_total)}.")
        else:
            display_col_label.config(text = f"To begin, you'll need ${'{:,.2f}'.format(-1*living_while_studying_expenses)} prior to working to afford living expenses and tuition while studying. Over 5 years, the whole endeavor will allow you to gross ${'{:,.2f}'.format(five_year_total)}.")

def clear_csv(): # this function clears the csv file
    with open("schools.csv", "w") as stream:
        stream.truncate(0)
    drop.destroy()
    display_choice_label.config(text="Please select a program: ")
    display_col_label.config(text = "Five-year outcome: ")
    display_tuition_label.config(text = "Tuition: ")
    display_salary_label.config(text = "Salary: ")
    display_living_expenses_label.config(text = "Living Expenses: ")


def get_csv_row(program):
    row_data = []
    with open("schools.csv", "r") as stream:
        reader = csv.reader(stream)
        for row in reader:
            if (f"{row[0]}: {row[2]}") == program:
                row_data.append(row)
    row_data = cleanup_data(row_data)
    return row_data

def get_selected_program(): # this function gets the selected program from the drop down menu
    selected_program = clicked.get()
    useful_data = get_csv_row(selected_program)
    update_choice_label(useful_data)
    return useful_data

def calculate_col(list, col_table): # this function matches the city to the cost of living table 
    for i in range(len(col_table)):
        if col_table[i][0] == list[0][1]:
            print(col_table[i])
            return col_table[i]
        

# --- GUI --- #

m = tk.Tk() 
m.title("University Search")
label = tk.Label(m, text="Please enter the website: ")
label.grid(row=1)
input_site = tk.Text(m, height=1, width=20)
input_site.grid(row=1, column=2)
display_choice_label = tk.Label(m, text="Please select a program: ")
display_choice_label.grid(row=2)
scrape_button = tk.Button(m, text="Scrape", command=get_website)
scrape_button.grid(row=1, column=3)
read_button = tk.Button(m, text="Print All to Console", command=read_csv)
read_button.grid(row=1, column=4)
clear_list_button = tk.Button(m, text="Reset Database", command=clear_csv)
clear_list_button.grid(row=1, column=6)
display_duration_label = tk.Label(m, text="Duration: ")
display_duration_label.grid(row=8, columnspan=8, sticky="W")
display_annual_tuition_label = tk.Label(m, text="Annual tuition price: ")
display_annual_tuition_label.grid(row=9, columnspan=8, sticky="W")
display_living_expenses_label = tk.Label(m, text="Net living expenses: ")
display_living_expenses_label.grid(row=11, columnspan=8, sticky="W")
display_salary_label = tk.Label(m, text="Salary: ")
display_salary_label.grid(row=12, columnspan=8, sticky="W")
display_tuition_label = tk.Label(m, text="Net cost for total tuition: ")
display_tuition_label.grid(row=10, columnspan=8, sticky="W")
display_col_label = tk.Label(m, text="Five-year outcome: ")
display_col_label.grid(row=13, columnspan=8, sticky="W")
display_program_info_button = tk.Button(m, text="Calculate program info", command=get_selected_program)
display_program_info_button.grid(row=1, column=8)
exit_button = tk.Button(m, text="Exit", command=m.destroy)
exit_button.grid(row=1, column=9)
label = tk.Label(m, text=get_current_date())
label.grid(row=14, column=9)

if __name__ == "__main__":
    m.mainloop()