import sqlite3
import datetime

# STEP 7: BUILD APPLICATION

# Connect to the SQLite database
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

def find_item_by_title(title):
    # Function to find an item in the library based on the title
    cursor.execute("SELECT * FROM Item WHERE title LIKE ?", ('%' + title + '%',))
    items = cursor.fetchall()
    return items

def borrow_item():
    # Function to borrow an item from the library
    user_id = int(input("Enter your user ID: "))
    item_id = int(input("Enter the item ID you want to borrow: "))
    due_date = input("Enter the due date (YYYY-MM-DD): ")

    cursor.execute("SELECT availabilityStatus FROM Item WHERE itemID = ?", (item_id,))
    availability = cursor.fetchone()
    if availability[0] != 'Available':
        return "Item is not available for borrowing."

    borrowing_date = datetime.date.today()
    cursor.execute("INSERT INTO Borrowing (userID, itemID, borrowingDate, dueDate) VALUES (?, ?, ?, ?)",
                   (user_id, item_id, borrowing_date, due_date))

    cursor.execute("UPDATE Item SET availabilityStatus = ? WHERE itemID = ?", ('Borrowed', item_id))
    conn.commit()
    return "Item successfully borrowed."

def return_item():
    # Function to return a borrowed item
    borrowing_id = int(input("Enter the borrowing ID: "))

    cursor.execute("SELECT itemID, returnDate FROM Borrowing WHERE borrowingID = ?", (borrowing_id,))
    result = cursor.fetchone()
    if result is None:
        return "Invalid borrowing ID."

    item_id, return_date = result
    if return_date is not None:
        return "Item has already been returned."

    return_date = datetime.date.today()
    cursor.execute("UPDATE Borrowing SET returnDate = ? WHERE borrowingID = ?", (return_date, borrowing_id))

    cursor.execute("SELECT dueDate FROM Borrowing WHERE borrowingID = ?", (borrowing_id,))
    due_date = cursor.fetchone()[0]
    if return_date > due_date:
        fine_days = (return_date - due_date).days
        fine = fine_days * 0.50  # Assuming a fine of $0.50 per day late
        cursor.execute("UPDATE Borrowing SET fines = ? WHERE borrowingID = ?", (fine, borrowing_id))

    cursor.execute("UPDATE Item SET availabilityStatus = ? WHERE itemID = ?", ('Available', item_id))
    conn.commit()
    return "Item successfully returned."

def donate_item():
    # Function to donate an item to the library
    title = input("Enter the item title: ")
    author = input("Enter the item author: ")
    genre = input("Enter the item genre: ")
    format = input("Enter the item format: ")

    cursor.execute("INSERT INTO Item (title, author, genre, format, availabilityStatus) VALUES (?, ?, ?, ?, ?)",
                   (title, author, genre, format, 'Available'))
    conn.commit()
    return "Item successfully donated."

def find_event_by_name(event_name):
    # Function to find an event in the library based on the event name
    cursor.execute("SELECT * FROM Event WHERE eventName LIKE ?", ('%' + event_name + '%',))
    events = cursor.fetchall()
    return events

def register_for_event():
    # Function to register for an event in the library
    try:
        user_id = int(input("Enter your user ID: "))
        event_name = input("Enter the event name you want to register for: ")

        cursor.execute("SELECT * FROM Event WHERE eventName = ?", (event_name,))
        event = cursor.fetchone()
        if event is None:
            return "Invalid event name. Please check the event name and try again."

        event_id = event[0]  # Assuming the eventID is in the first column of the Event table.

        cursor.execute("INSERT INTO Invited (userID, eventID) VALUES (?, ?)", (user_id, event_id))
        conn.commit()
        return "Successfully registered for the event."
    except ValueError:
        return "Invalid input. Please enter a valid user ID."

def volunteer():
    try:
        # Function to volunteer for the library
        user_id = int(input("Enter your user ID: "))

        # Fetch user details from the User table using userID
        cursor.execute("SELECT * FROM User WHERE userID = ?", (user_id,))
        user = cursor.fetchone()
        if user is None:
            return "Invalid user ID."

        # Extract user details
        user_first_name = user[1]  # Assuming firstName is in the second column (index 1)
        user_last_name = user[2]   # Assuming lastName is in the third column (index 2)
        user_contact_details = user[3]  # Assuming contactDetails is in the fourth column (index 3)

        task = input("Enter the job you want to volunteer for: ")

        # Insert user details into the Personnel table
        cursor.execute("INSERT INTO Personnel (personnelID, firstName, lastName, jobTitle, contactDetails) VALUES (?, ?, ?, ?, ?)",
                       (user_id, user_first_name, user_last_name, task, user_contact_details))
        conn.commit()

        return "Successfully volunteered for the library. You are now library personnel."
    except ValueError:
        return "Invalid input. Please enter a valid user ID (integer)."
    except Exception as e:
        return f"An error occurred: {e}"


def ask_for_help():
    try:
        # Function to ask for help from a librarian
        user_id = int(input("Enter your user ID: "))
        message = input("Enter your message for the librarian: ")

        cursor.execute("SELECT * FROM User WHERE userID = ?", (user_id,))
        user = cursor.fetchone()
        if user is None:
            return "Invalid user ID."

        return "Help request sent to the librarian."
    except ValueError:
        return "Invalid input. Please enter a valid user ID (integer)."
    except Exception as e:
        return f"An error occurred: {e}"

def print_menu():
    print("\nWelcome To our Library Database! \n")
    print("Please select an option from the following menu: \n")
    print("1. Find an item in the library")
    print("2. Borrow an item from the library")
    print("3. Return a borrowed item")
    print("4. Donate an item to the library")
    print("5. Find an event in the library")
    print("6. Register for an event in the library")
    print("7. Volunteer for the library")
    print("8. Ask for help from a librarian")
    print("9. Exit\n")

while True:
    print_menu()
    choice = int(input("Enter your choice: \n"))

    if choice == 1:
        title = input("Enter the item title: \n")
        items = find_item_by_title(title)
        if items:
            print("Found items:\n")
            for item in items:
                print(item)
        else:
            print("No items found.\n")
    elif choice == 2:
        print(borrow_item())
    elif choice == 3:
        borrowing_id = int(input("Enter the borrowing ID: \n"))
        print(return_item())
    elif choice == 4:
        print(donate_item())
    elif choice == 5:
        event_name = input("Enter the event name: \n")
        events = find_event_by_name(event_name)
        if events:
            print("Found events:")
            for event in events:
                print(event)
        else:
            print("No events found.\n")
    elif choice == 6:
        print(register_for_event())
    elif choice == 7:
        print(volunteer())
    elif choice == 8:
        print(ask_for_help())
    elif choice == 9:
        break
    else:
        print("Invalid choice. Please try again.\n")

# Close the database connection
conn.close()