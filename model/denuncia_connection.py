import psycopg2

class DenunciaConnection():
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
            SELECT * FROM "denuncia" WHERE resuelta=false
            """)
            return cur.fetchall()
        
    def read_one(self, id):
        with self.conn.cursor() as cur:
            cur.execute("""
            SELECT * FROM "denuncia" WHERE id = %s
            """, (id,))
            return cur.fetchone()

    def write(self, data):
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO "denuncia"(motivo,id_recipe,resuelta) VALUES(%(motivo)s, %(id_recipe)s,%(resuelta)s)
                        """,data)
        self.conn.commit()
        

    def update(self, data):
        with self.conn.cursor() as cur:
            cur.execute("""
            UPDATE "denuncia" SET motivo=%(motivo)s, id_recipe=%(id_recipe)s, resuelta=%(resuelta)s WHERE id=%(id)s
            """, data)
        self.conn.commit()

    def resuelta(self, id):
        with self.conn.cursor() as cur:
            cur.execute("""
            UPDATE "denuncia" SET resuelta=true WHERE id=%s
            """, (id,))
        self.conn.commit()

    def delete(self,id):
        with self.conn.cursor() as cur:
            cur.execute("""
            DELETE FROM "denuncia" WHERE id =%s
            """, (id,))
        self.conn.commit()

    def __def__(self):
        self.conn.close()