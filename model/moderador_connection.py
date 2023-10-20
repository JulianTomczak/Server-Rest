import psycopg2

class ModeradorConnection():
    conn = None
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                user="postgres",
                password="root",
                host="localhost",
                port='5432',
                database = "chefencasa")
        except psycopg2.OperationalError as err:
            print(err)
            self.conn.close()

    def read_all(self):
        with self.conn.cursor() as cur:
            cur.execute("""
            SELECT * FROM "moderador"
            """)
            return cur.fetchall()
        
    def read_one(self, id):
        with self.conn.cursor() as cur:
            cur.execute("""
            SELECT * FROM "moderador" WHERE id = %s
            """, (id,))
            return cur.fetchone()

    def write(self, data):
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO "moderador"(name,last_name,email,username,password) VALUES(%(name)s, %(last_name)s,%(email)s,%(username)s,%(password)s)
                        """,data)
        self.conn.commit()
        

    def update(self, data):
        with self.conn.cursor() as cur:
            cur.execute("""
            UPDATE "moderador" SET name=%(name)s, last_name=%(last_name)s, email=%(email)s, username=%(username)s, password=%(password)s WHERE id=%(id)s
            """, data)
        self.conn.commit()

    def delete(self,id):
        with self.conn.cursor() as cur:
            cur.execute("""
            DELETE FROM "moderador" WHERE id =%s
            """, (id,))
        self.conn.commit()

    def __def__(self):
        self.conn.close()
