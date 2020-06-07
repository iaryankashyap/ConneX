import mysql.connector as sq
sqcon = sq.connect(host='connex.mysql.pythonanywhere-services.com', database='connex$users',
                   user='connex', password='rootrootroot')
cursor = sqcon.cursor()
cursor.execute("SELECT * FROM users")
for i in cursor:
    print(i)
    cursor.close()
