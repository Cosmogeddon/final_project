from classes import University, Country
import tkinter as tk
from bs4 import BeautifulSoup
import csv

def check_data(list):
    for item in list:
        print(str(item))

def write_csv(school):
    with open("schools.csv", "w", newline='') as stream:
        writer = csv.writer(stream)
        writer.writerows(iter(school))

def read_csv():
    with open("schools.csv", "r") as stream:
        reader = csv.reader(stream)
        for row in reader:
            print(row)


def create_list(list1, list2, list3, list4, list5):
    global uni_lists
    uni_lists = []
    for i in range(len(list1)):
        school = University(list1[i].text, list2[i].text, list3[i].text, list4[i].text, list5[i].text)
        uni_lists.append(school)
    return uni_lists

def scrape_data(website):
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


def get_website():
    global website
    website = input_site.get("1.0", "end-1c")
    scrape_data(website)

def get_list_options():
    list_options = []
    with open("schools.csv", "r") as stream:
        reader = csv.reader(stream)
        for row in reader:
            list_options.append(row[2])
    return list_options

m = tk.Tk()
m.title("University Search")
label = tk.Label(m, text="Please enter the website: ")
label.grid(row=12)
input_site = tk.Text(m, height=1, width=20)
input_site.grid(row=12, column=1)
scrape_button = tk.Button(m, text="Scrape", command=get_website)
scrape_button.grid(row=12, column=3)
read_button = tk.Button(m, text="Read", command=read_csv)
read_button.grid(row=12, column=4)
exit_button = tk.Button(m, text="Exit", command=m.destroy)
exit_button.grid(row=12, column=5)

if __name__ == "__main__":
    m.mainloop()