import pg8000 as pg

# Connect to the database
# Will need to be on Mines VPN for this to work
user = input("Enter username:")
password = input("Enter password:")
db_conn = pg.connect(user=user, password=password, host='codd.mines.edu', port=5433, database='csci403')

# Establsih the database cursor
cursor = db_conn.cursor()

# Move into correct schema
schema_correction = "SET search_path TO iradley, "+user+", public"
cursor.execute(schema_correction)

# Example code of simple query
'''
cursor.execute("SELECT * FROM tax_revenue")

results = cursor.fetchall()
for row in results:
    print(row)
'''

