import sqlite3
import pandas as pd

# Create table

# c.execute("CREATE TABLE userlog (id text,name text,date text,time text)")
# c.execute("CREATE TABLE userinfo (id text,name text)")


# Create a database or connect to one
conn = sqlite3.connect('database.db')

# Create cursor
c = conn.cursor()

#c.execute("CREATE TABLE userlog (id text,name text,date text,time text)")
#c.execute("CREATE TABLE userinfo (id text,name text)")
#c.execute("CREATE TABLE Images (id text,photo BLOB,status text)")


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData


def insertImage(ids, photo, status):
    try:
        conn = sqlite3.connect('database.db')
        # Create cursor
        c = conn.cursor()

        sqlite_insert_blob_query = """ INSERT INTO Images
                                  (id,  photo , status) VALUES (?, ?, ?)"""

        empPhoto = convertToBinaryData(photo)
        # resume = convertToBinaryData(resumeFile)
        # Convert data into tuple format
        data_tuple = (ids, empPhoto, status)
        c.execute(sqlite_insert_blob_query, data_tuple)
        conn.commit()
        print("Image and file inserted successfully as a BLOB into a table")
        c.close()
    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
    finally:
        if (conn):
            conn.close()
            print("the sqlite connection is closed")

# insertBLOB(1, "Smith", "E:\pynative\Python\photos\smith.jpg", "E:\pynative\Python\photos\smith_resume.txt")
# insertBLOB(2, "David", "E:\pynative\Python\photos\david.jpg", "E:\pynative\Python\photos\david_resume.txt")


def insertUserLog(ids, name, date, time):
    # Create a database or connect to one
    conn = sqlite3.connect('database.db')
    # Create cursor
    c = conn.cursor()

    # Insert Into Table
    c.execute("INSERT INTO userlog VALUES (:id, :name, :date, :time)",
              {
                  'id': ids,
                  'name': name,
                  'date': date,
                  'time': time,
              })
    selectUserLog()

    # Commit Changes
    conn.commit()

    # Close Connection
    conn.close()


def insertUserInfo(ids, name):
    # Create a database or connect to one
    conn = sqlite3.connect('database.db')
    # Create cursor
    c = conn.cursor()

    # Insert Into Table
    c.execute("INSERT INTO userinfo VALUES (:id, :name)",
              {
                  'id': ids,
                  'name': name,
              })
    selectUserInfo()

    # Commit Changes
    conn.commit()

    # Close Connection
    conn.close()


def selectUserLog():
    # Create a database or connect to one
    conn = sqlite3.connect('database.db')
    # Create cursor
    c = conn.cursor()

    # Insert Into Table
    c.execute("SELECT * from  userlog")
    records = c.fetchall()

    col_names = ['Id', 'Name', 'Date', 'Time']
    attendance = pd.DataFrame(columns=col_names)
    print_records = ''
    for record in records:
        attendance.loc[len(attendance)] = [record[0],
                                           record[1], record[2], record[3]]

        # query_label = Label(root, text=print_records)
        # query_label.grid(row=12, column=0, columnspan=2)
    print(attendance)
    # Commit Changes
    conn.commit()

    # Close Connection
    conn.close()


def selectUserInfo():
    # Create a database or connect to one
    conn = sqlite3.connect('database.db')
    # Create cursor
    c = conn.cursor()

    # Insert Into Table
    c.execute("SELECT * FROM userinfo")
    records = c.fetchall()
    print(records)

    col_names = ['Id', 'Name']
    attendance = pd.DataFrame(columns=col_names)
    print_records = ''
    for record in records:
        attendance.loc[len(attendance)] = [record[0], record[1]]

        # query_label = Label(root, text=print_records)
        # query_label.grid(row=12, column=0, columnspan=2)

    # Commit Changes
    conn.commit()


    # Close Connection
    conn.close()
    return (attendance)


# Commit Changes
conn.commit()

# Close Connection
conn.close()
