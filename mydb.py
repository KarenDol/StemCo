import mysql.connector

dataBase = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "banana228",
    auth_plugin='mysql_native_password'
)

cursorObject = dataBase.cursor()

cursorObject.execute("CREATE DATABASE problems")

print("All Done!")