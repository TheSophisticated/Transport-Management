"""
TODO:
1. Analysis (i.e finding overlapping routes for buses with available spaces)
2. Vehicle Info table (i.e Bus License No. , Driver Name, Conductor Name, Age, Last Service Date)
"""

#Importing Dependencies
import pymysql as connector
from tabulate import tabulate #Tabulate to display data in a table format
import matplotlib.pyplot as plt #Matplotlib to analyse data graphically (Plot Graphs) 

#Defining the cursor object
my_connector = connector.connect(
    host = "localhost",
    user = "root",
    passwd = "root",
    database = 'transport_details'
)

cursor = my_connector.cursor()

print('''

████████╗██████╗░░█████╗░███╗░░██╗░██████╗██████╗░░█████╗░██████╗░████████╗clea
╚══██╔══╝██╔══██╗██╔══██╗████╗░██║██╔════╝██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝
░░░██║░░░██████╔╝███████║██╔██╗██║╚█████╗░██████╔╝██║░░██║██████╔╝░░░██║░░░
░░░██║░░░██╔══██╗██╔══██║██║╚████║░╚═══██╗██╔═══╝░██║░░██║██╔══██╗░░░██║░░░
░░░██║░░░██║░░██║██║░░██║██║░╚███║██████╔╝██║░░░░░╚█████╔╝██║░░██║░░░██║░░░
░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝╚═════╝░╚═╝░░░░░░╚════╝░╚═╝░░╚═╝░░░╚═╝░░░

███╗░░░███╗░█████╗░███╗░░██╗░█████╗░░██████╗░███████╗███╗░░░███╗███████╗███╗░░██╗████████╗
████╗░████║██╔══██╗████╗░██║██╔══██╗██╔════╝░██╔════╝████╗░████║██╔════╝████╗░██║╚══██╔══╝
██╔████╔██║███████║██╔██╗██║███████║██║░░██╗░█████╗░░██╔████╔██║█████╗░░██╔██╗██║░░░██║░░░
██║╚██╔╝██║██╔══██║██║╚████║██╔══██║██║░░╚██╗██╔══╝░░██║╚██╔╝██║██╔══╝░░██║╚████║░░░██║░░░
██║░╚═╝░██║██║░░██║██║░╚███║██║░░██║╚██████╔╝███████╗██║░╚═╝░██║███████╗██║░╚███║░░░██║░░░
╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝╚═╝░░╚═╝░╚═════╝░╚══════╝╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚══╝░░░╚═╝░░░

''')

#Listing all the tables in the database
def show_tables():
    query = "SHOW TABLES"
    cursor.execute(query)
    result = cursor.fetchall()
    for row in result:
        print (row)

#Showing all the data from a particular table
def show_data_from_table(name):
    query = "SELECT * FROM " + name
    cursor.execute(query)
    result = cursor.fetchall()

    cursor.execute("SHOW COLUMNS FROM " + name)
    columns = cursor.fetchall()
    column_names = [col[0] for col in columns] 

    print(tabulate(result, headers=column_names, tablefmt="psql"))

def Update_Record(column, key, value, keyvalue):

    query = f"UPDATE STUDENT SET {column} = %s where {key} = {keyvalue}"
    cursor.execute(query, tuple(value))
    my_connector.commit()
    

#Adding data into the table
def add_data(name, no_of_records):
    col_query = f"SHOW COLUMNS FROM {name}"
    cursor.execute(col_query)
    columns = cursor.fetchall()
    column_names = [col[0] for col in columns] 

    for j in range(no_of_records):
        data = []
        for i in column_names:
            value = input("Enter value for "+ i + ": ")
            data.append(value)

        query = f"INSERT INTO {name} values({'%s,' * len(column_names)})"[:-2]+')'

        try:
            cursor.execute(query, tuple(data))
            my_connector.commit()
            print("\nData was added successfully!\n")
        except:
            print("Unexpected Error!")

#Deleting Data from the table
def delete_data(name, column_name, value):
    query = f"DELETE FROM {name} WHERE {column_name} = %s"
    try:
        cursor.execute(query, (value, )) #Turning Value into a tuple since cursor.execute accepts tuples
        my_connector.commit()
        print("\nData was deleted successfully!\n")
    except:
        print("An Unexpected Error occurred!")

#Plotting graph based on the data
def graph_data(name):
    query = f"SELECT bus_no, no_of_students FROM {name}"
    cursor.execute(query)
    result = cursor.fetchall()

    bus_no = [row[0] for row in result]
    students = [row[1] for row in result]

    #Plotting the graph
    plt.figure(figsize=(10,6))
    plt.bar(bus_no, students, color = "#5975ff")
    plt.axhline(y=60, color='black', linestyle='--', linewidth=2, label=f'Max Capacity (60)')
    plt.xlabel("Bus No.")
    plt.ylabel("No. of Students")
    plt.title("No. of students in each bus")
    plt.xticks(bus_no)
    plt.grid(True, axis = 'y')
    plt.show()

def Sort_Data(name):
    query = "SELECT * FROM " + name
    cursor.execute(query)
    array = list(cursor.fetchall())

    for i in range(0, len(array)):
        for j in range(i+1, len(array)):
            if array[i][0] > array[j][0]:
                array[i], array[j] = array[j], array[i]
    my_connector.commit()
    return array

    


def Search_Data(name):
    target = int(input("Enter the Bus No. you want to Search for: "))
    array = Sort_Data(name)

    low = 0
    high = len(array) - 1
    while low <= high:
        mid = (low + high) // 2 
        if array[mid][0] == target:
            break
        elif array[mid][0] < target:
            low = mid + 1
        else:
            high = mid - 1

    cursor.execute(f"SHOW COLUMNS FROM {name}")
    columns = cursor.fetchall()
    column_names = [col[0] for col in columns] 

    print(tabulate([array[mid]], headers=column_names, tablefmt="psql"))

def find_overlap():
    is_overlap = False
    query = "SELECT * FROM bus_info" 
    cursor.execute(query)
    result = cursor.fetchall()

    array = []
    overlap_list = []

    for i in result:
        if i[2] not in array:
            array.append(i[2])
        elif i[2] in array:
            if i[1] < 60:              
                query = f"SELECT bus_no, area_covered FROM bus_info WHERE area_covered = '{i[2]}'"
                cursor.execute(query)
                result = cursor.fetchall() 
                overlap_list.extend([i for i in result])
                is_overlap = True
    if is_overlap:
        print("Potential Overlap Determined!")
        column_names = ['Bus_No', 'Area_Covered'] 
        print(tabulate(overlap_list, headers=column_names, tablefmt="psql"))
    else:
        print("No Overlap Found. The routes are optimised!")


#Main Program Loop
while True:
    #Main Menu
    print('''\nMenu - (Type the no. adjacent to the action you want to perform)\n
    1 - Show All Tables
    2 - Show Data
    3 - Add Data
    4 - Delete Data
    5 - Analyse Data - Bus Info Table
    6 - Sort Data
    7 - Search for Data using Bus No.
    8 - Exit
    ''')
    choice = input("\nEnter your option no. : ")
    if choice == "1":
        show_tables()

    elif choice == "2":
        table_name = input("Enter the name of the table you wish to see: ")
        show_data_from_table(table_name)
            
    elif choice == "3":
        table_name = input("Enter the name of the table: ")
        entries = int(input("No. of entries you want to add: "))
        add_data(table_name, entries)     

    elif choice == '4':
        table_name = input("Enter the name of the table: ")
        column_name = input("Enter the column name for the condition: ")
        value = input("Enter a value from the column to identify the record you wish to delete: ")
        delete_data(table_name, column_name, value)        

    elif choice == "5":   
        while True:
            print ("""
            Graph - View a Capacity Vs Bus_no Graph for all the buses
            Overlap - Analyse the table to find potential overlaps between area covered by buses
            Exit - Go Back to Main Menu
            """)
            subchoice = input("Enter Your Choice Here: ")
            if subchoice == 'Graph':
                 graph_data('bus_info')
            elif subchoice == 'Overlap':
                find_overlap()
            elif subchoice == 'Exit':
                break
            else:
                print("Please Enter a Valdid Choice")


    elif choice == '6':
        name = input("Enter Table name: ")
        array = Sort_Data(name)
        
        cursor.execute("SHOW COLUMNS FROM " + name)
        columns = cursor.fetchall()
        column_names = [col[0] for col in columns] 

        print(tabulate(array, headers=column_names, tablefmt="psql"))

    elif choice == '7':
        name = input("Enter table Name: ")
        Search_Data(name)

    elif choice == "8":
        print("Thank You for using our Transport Management System!")
        cursor.close()
        my_connector.close()
        break
    else:
        print("Invalid Input! Please chose an action from the one's listed above")