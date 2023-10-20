import psycopg2

class RecipesConnection():
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

    def delete(self,id):
        with self.conn.cursor() as cur:
            cur.execute("""
            DELETE FROM "recipes" WHERE id =%s
            """, (id,))
        self.conn.commit()

    def __def__(self):
        self.conn.close()