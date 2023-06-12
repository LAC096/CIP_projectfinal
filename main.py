# Design: I took inspiration from the search engine assignment, but I decided to create a different version based on what I liked. I wanted to make it more dynamic but I need more time.
# Aim was: given specific characteristics of the users find out the best AI software available to help them from a list of softwares.
# Disclaimer: I tried to develop a simple search engine: google and chatGTP was used to solve some conceptual problems: such as how to conceptually create a search query with filters and how to display results.

# Milestone 1: data loading: I used  the pandas library, the excel is not real although I scraped some software and I could used a real one.
# Milestone 2: input:  search query, select an MBTI type, and choose a techsavvy
# Milestone 3: filtering data: filter data based on user-specified criteria. MBTI type, and techsavvy level which are specific for the user
# Milestone 4: sorting data: sorting data to add order and priorities
# Milestone 5: display results: separate window  to display the search results in a tabular format: results will include all the column in the excel

# Import packages needed
import pandas as pd
import tkinter as tk
from tkinter import ttk


# #Milestone 1
aisoftware_sheet = pd.read_excel('software_list.xlsx', sheet_name='software_list')

def search_engine():
# create a search engine software function

    query = search_entry.get().lower()
    mbti_type = mbti_combobox.get().lower()
    techsavvy_level = techsavvy_combobox.get()

    # Milestone 3: filtering data based on search query, MBTI and techsevvy
    filtered_software = aisoftware_sheet[
        (aisoftware_sheet['Task'].str.lower().str.contains(query)) |
        (aisoftware_sheet['MBTI'].str.lower().str.contains(query)) |
        (aisoftware_sheet['Description'].str.lower().str.contains(query)) |
        (aisoftware_sheet['Area'].str.lower().str.contains(query))]

    if mbti_type:
        filtered_software = filtered_software[filtered_software['MBTI'].str.lower() == mbti_type]

    if techsavvy_level:
        filtered_software = filtered_software[filtered_software['Techsavvy'] == int(techsavvy_level)]

    # Milestone 4: Sort software based on task
    sorted_software = filtered_software.sort_values('Task')

    # Milestone 5: display results
    result_user_interface = tk.Toplevel(user_interface)
    result_user_interface.title("Search")

    # Mil 5: Display results (after some tries treeview was chosen because it is ordered in a tabular fashion)
    result_display_treeview = ttk.Treeview(result_user_interface)
    result_display_treeview['columns'] = tuple(aisoftware_sheet.columns)
    for col in aisoftware_sheet.columns:
        result_display_treeview.heading(col, text=col)
    result_display_treeview.pack()

    # Mil 5: Display search results
    if sorted_software.empty:
        result_display_treeview.insert('', 'end', values=('No software matches the given query.', '', '', '', '', '', '', '', ''))
    else:
        for _, row in sorted_software.iterrows():
            result_display_treeview.insert('', 'end', values=row.values)

# Create user interface
user_interface = tk.Tk()
user_interface.title("AI Software Search Engine")

# Milestone 2 and Milestone 3 completion entry and filtering

search_label = tk.Label(user_interface, text="What do you want to do?")
search_label.pack()
search_entry = tk.Entry(user_interface)
search_entry.pack()

mbti_label = tk.Label(user_interface, text="your_MBTI_type:")
mbti_label.pack()
mbti_values = sorted(aisoftware_sheet['MBTI'].unique())
mbti_combobox = ttk.Combobox(user_interface, values=mbti_values)
mbti_combobox.pack()

techsavvy_label = tk.Label(user_interface, text="Techsavvy_level:")
techsavvy_label.pack()
techsavvy_values = sorted(aisoftware_sheet['Techsavvy'].astype(str).unique())
techsavvy_combobox = ttk.Combobox(user_interface, values=techsavvy_values)
techsavvy_combobox.pack()

# create search button
search_button = tk.Button(user_interface, text="MagicSearchClick", command=search_engine)
search_button.pack()

# Start
user_interface.mainloop()
