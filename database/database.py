import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
db = psycopg2.connect(
    user="postgres",
    password="root",
    host="localhost",
    port='5432'
)

db.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT);

cursor = db.cursor();

print("Connection database successfully.")

name_Database   = "chefencasa";

db = psycopg2.connect(
    user="postgres",
    password="root",
    host="localhost",
    port='5432',
    database = name_Database
)
db.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT);

cursor = db.cursor();

cursor.execute("CREATE TABLE IF NOT EXISTS moderador (id SERIAL PRIMARY KEY, name VARCHAR(255) NOT NULL, last_name VARCHAR(255) NOT NULL, email VARCHAR(255) UNIQUE NOT NULL, username VARCHAR(50) UNIQUE NOT NULL, password VARCHAR(255) NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")
cursor.execute("CREATE TABLE IF NOT EXISTS denuncia (id SERIAL PRIMARY KEY, motivo VARCHAR(255) NOT NULL, id_recipe INT NOT NULL, resuelta BOOLEAN, FOREIGN KEY (id_recipe) REFERENCES recipes(id));")
cursor.execute("CREATE TABLE IF NOT EXISTS mensajes (id SERIAL PRIMARY KEY, emisor_id INT NOT NULL, destinatario_id INT NOT NULL, asunto VARCHAR(255) NOT NULL, mensaje TEXT NOT NULL, respuesta TEXT,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (emisor_id) REFERENCES users(id), FOREIGN KEY (destinatario_id) REFERENCES users(id));")
print("The chefencasa database schema was created succesfully.")