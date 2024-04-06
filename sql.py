import mysql.connector

connector = mysql.connector.connect(host='localhost',user='root',password = 'aashoksai306@',database='student_marks')

db = connector.get_server_info()
print(db)

cursor = connector.cursor()

cursor.execute("CREATE TABLE  student (name VARCHAR(255),class varchar(255),section varchar(255), marks INT)")

# Insert values into the table
sql = "INSERT INTO student (name, class, section, marks) VALUES (%s, %s, %s, %s)"
values = [
    ('John', 'Data Science', 'A', 65),
    ('Alice', 'DevOps', 'B', 89),
    ('Bob', 'Front End', 'A', 95),
    ('Emma', 'Data Science', 'B', 78),
    ('Michael', 'DevOps', 'A', 82)
]

cursor.executemany(sql, values)

# Commit changes
connector.commit()

# Close cursor and connection
cursor.close()
connector.close()

