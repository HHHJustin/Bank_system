import psycopg2

# Update connection string information
host = "localhost"
dbname = "bank-database"
user = "postgres"
password = "zxcv4567"
sslmode = "allow"

# Construct connection string
conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
conn = psycopg2.connect(conn_string)
print("Connection established")

cursor = conn.cursor()
cursor.execute("SELECT account FROM users")
data = cursor.fetchall()
account_list = []
for row in data:
    account_list.append(row[0])

if 'ponz1234' in account_list:
    print(123)
# Clean up
conn.commit()
cursor.close()
conn.close()