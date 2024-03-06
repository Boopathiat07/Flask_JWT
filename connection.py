import mysql.connector  

my_db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "password",
    database = "FlaskCrud",
)

my_cursor = my_db.cursor()

# my_cursor.execute("CREATE DATABASE FlaskCrud")
query = f"INSERT INTO user (id, name, email, date_joined) VALUES (35, 'Boopathi', 'abc@gmail.com', '2023-03-23')"
my_cursor.execute(query)

my_cursor.execute("SELECT * FROM user")

for db in my_cursor:
    print(db)

