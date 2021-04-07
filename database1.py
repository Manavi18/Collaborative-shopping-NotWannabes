import sqlite3

conn = sqlite3.connect('database1.db')
c = conn.cursor() 

#create table for users
c.execute('''CREATE TABLE users 
		(userId INTEGER PRIMARY KEY, 
		password TEXT,
		email TEXT,
		username TEXT,
		phone TEXT
		)''')

# table to store product name and its image url
c.execute('''CREATE TABLE products
		(productId INTEGER PRIMARY KEY,
		name TEXT,
		img TEXT
		)''')

# table to store user section name, user's product and the corresponding image
c.execute('''CREATE TABLE kart
		(name TEXT,
		prod_name TEXT,
		prod_img TEXT,
		FOREIGN KEY(prod_name) REFERENCES products(name)
		FOREIGN KEY(prod_img) REFERENCES products(img),
		)''')

c.close()