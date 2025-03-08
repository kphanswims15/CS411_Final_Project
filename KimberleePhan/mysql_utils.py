# mysql
import mysql.connector
from mysql.connector import errorcode

# connects to the sql database
def db_connect():
    try:
        cnx = mysql.connector.connect(user='root', 
                                password='Jerrybob1234!', 
                                database='academicworld')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        print("Database Connection Successful!")
        return cnx

def select(db, query):
    data_cursor = db.cursor()
    sql_query = query
    data_cursor.execute(sql_query)
    data = data_cursor.fetchall()
    return data

# fills in university drop down
def university_dropdown():
    db = db_connect()
    data_cursor = db.cursor()
    sql_query = 'SELECT id, name FROM university;'
    data_cursor.execute(sql_query)
    data = data_cursor.fetchall()
    process_data = [{'label': name, 'value': id} for id, name in data]
    db.close()
    return process_data

# fills in faculty dropdown from university id
def faculty_dropdown(uni_id):
    db = db_connect()
    data_cursor = db.cursor()
    sql_query = "SELECT id, name FROM faculty WHERE university_id = " + str(uni_id) + " ORDER BY name;"
    data_cursor.execute(sql_query)
    data = data_cursor.fetchall()
    process_data = [{'label': name, 'value': name} for id, name in data]
    db.close()
    return process_data

# counts the number of faculty numbers based on university id
def faculty_count(uni_id):
    db = db_connect()
    data_cursor = db.cursor()
    sql_query = "SELECT COUNT(university_id) FROM faculty WHERE university_id =" + str(uni_id) + ";"
    data_cursor.execute(sql_query)
    data = data_cursor.fetchall()
    process_data = [faculty_count[0] for faculty_count in data]
    db.close()
    return process_data

# gets data to populate the faculty table
def faculty_table(uni_id):
    db = db_connect()
    data_cursor = db.cursor()
    sql_query = "SELECT name, position, email, phone FROM faculty WHERE university_id = " + str(uni_id) + " ORDER BY name;"
    data_cursor.execute(sql_query)
    data = data_cursor.fetchall()
    process_data = [{'Name': row[0], 'Position': row[1], 'Email': row[2], 'Phone': row[3]} for row in data]
    db.close()
    return process_data

# inserts new faculty into the database based off of input from the user
def insert_faculty(name, position, email, phone, uni_affiliation): 
    print(str(name) + " - " + str(position) + " - " + str(email) + " - " + str(phone) + " - " + str(uni_affiliation))
    db = db_connect()
    data_cursor = db.cursor()
    sql_query = "INSERT INTO faculty (id, name, position, email, phone, university_id) values (%s, %s , %s , %s, %s, %s);"
    values = (generate_faculty_id(), name, position, email, phone, uni_affiliation)
    data_cursor.execute(sql_query, values)
    db.commit()
    db.close()

# generates a new id for the new faculty added
def generate_faculty_id():
    db = db_connect()
    data_cursor = db.cursor()
    sql_query = "SELECT MAX(id) FROM faculty;"
    data_cursor.execute(sql_query)
    data = data_cursor.fetchone()
    new_id = data[0] if data[0] else 0
    db.close()
    return new_id + 1

# gets data for the bar chart
def keyword_bar_chart(uni_id):
    db = db_connect()
    data_cursor = db.cursor()
    sql_query = "SELECT keyword.name, COUNT(faculty_keyword.faculty_id) FROM keyword, faculty_keyword, faculty WHERE keyword.id = faculty_keyword.keyword_id AND faculty.id = faculty_keyword.faculty_id AND faculty.university_id ="  + str(uni_id) +  " GROUP BY faculty_keyword.keyword_id ORDER BY COUNT(faculty_keyword.faculty_id) DESC LIMIT 10;"
    data_cursor.execute(sql_query)
    data = data_cursor.fetchall()
    db.close()
    return data

# gets data for the faculty profile widget
def get_faculty_profile(name):
    db = db_connect()
    data_cursor = db.cursor()
    sql_query = "SELECT name, position, email, phone, photo_url FROM faculty WHERE name='" + str(name) + "';"
    data_cursor.execute(sql_query)
    data = data_cursor.fetchall()
    process_data = [{'Name': row[0], 'Position': row[1], 'Email': row[2], 'Phone': row[3], 'Photo': row[4]} for row in data]

    db.close()
    return process_data