import sqlite3

connection = sqlite3.connect('./data/data.db')
cursor = connection.cursor()
#user table
create_user_table = "CREATE TABLE users(userId INT, username TEXT, password TEXT, email TEXT, briefIntro TEXT)"
cursor.execute(create_user_table)
users = [
    (1, 'jose', 'asdf123', 'jose@ucla.edu', 'hi i am an undergrad at ucla'),
    (2, 'rolf', 'asdf', 'rolf@ucla.edu', 'I am a PHD at ucla'),
    (3, 'anne', 'xyz', 'anne@ucla.edu', 'I am just a master')
]
insert_query = "INSERT INTO users VALUES (?, ?, ?, ?, ?)"
cursor.executemany(insert_query, users)

select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)

connection.commit() 
connection.close()