import mysql.connector

#Main Database
#
db_login = "Database Login"
db_password = "Database Password"
db_address = "Database Adress"
db_database = "Database Name"
#
#
#Users table name
db_users = "users"
#
#
mydb = mysql.connector.connect(
  host=db_address,
  user=db_login,
  passwd=db_password
)

mydb_u = mysql.connector.connect(
  host=db_address,
  user=db_login,
  passwd=db_password,
  database=db_database
)
#mycursor = mydb.cursor()
