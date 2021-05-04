import pg8000.native

con = pg8000.native.Connection(user='maxgawason', password='', host='codd.mines.edu', port=5433, database='csci403')
print(con.run("SELECT * FROM patents"))
