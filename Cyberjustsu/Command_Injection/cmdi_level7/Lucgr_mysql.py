#hostname: cyberjutsu-prod-cmdi08.cvn0lbsf7yym.ap-southeast-1.rds.amazonaws.com:3306
#database: cmdi08
#user: cmdi08user
#password: eku.YUE9bwc4ezt1vap
from sqlite3 import connect
import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(host='cyberjutsu-prod-cmdi08.cvn0lbsf7yym.ap-southeast-1.rds.amazonaws.com',
                                         database='cmdi08',
                                         user='cmdi08user',
                                         password='eku.YUE9bwc4ezt1vap')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL database... MySQL Server version on ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("Your connected to - ", record)
except Error as e:
    print("Error while connecting to MySQL", e)
    
    