import sqlite3

#Open database
conn = sqlite3.connect('database.db')

#Create table
conn.execute('''CREATE TABLE usuarios 
		(idUsuario INTEGER PRIMARY KEY, 
		contraseña TEXT,
		correo TEXT,
		nombres TEXT,
		apellidos TEXT,
		direccion TEXT, 
		telefono TEXT
		)''')

conn.execute('''CREATE TABLE productos
		(idProducto INTEGER PRIMARY KEY,
		nombre TEXT,
		precio REAL,
		descripcion TEXT,
		imagen TEXT,
		stock INTEGER,
		idCategoria INTEGER,
		FOREIGN KEY(idCategoria) REFERENCES categorias(idCategoria)
		)''')

conn.execute('''CREATE TABLE carro
		(idUsuario INTEGER,
		idProducto INTEGER,
        correo Text,
		FOREIGN KEY(idUsuario) REFERENCES usuarios(idUsuario),
		FOREIGN KEY(idProducto) REFERENCES productos(idProducto)
		)''')

conn.execute('''CREATE TABLE categorias
		(idCategoria INTEGER PRIMARY KEY,
		nombre TEXT
		)''')



conn.close()