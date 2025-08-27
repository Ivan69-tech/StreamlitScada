import psycopg2
from psycopg2 import sql, extras

class PostgresDB:
    def __init__(self, host, dbname, user, password, port=5432):
        self.host = host
        self.dbname = dbname
        self.user = user
        self.password = password
        self.port = port
        self.conn = None
        self.cursor = None

    def connect(self):
        """Établit la connexion à la base de données"""
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                port=self.port
            )
            self.cursor = self.conn.cursor(cursor_factory=extras.RealDictCursor)
            print("Connexion réussie à PostgreSQL")
        except Exception as e:
            print("Erreur de connexion :", e)

    def execute_query(self, query, params=None):
        """Exécute une requête SELECT et retourne les résultats"""
        try:
            self.cursor.execute(query, params)
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            print("Erreur lors de l’exécution de la requête :", e)
            return None

    def execute_write(self, query, params=None):
        """Exécute une requête INSERT/UPDATE/DELETE et commit"""
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print("Erreur lors de l’écriture :", e)

    def close(self):
        """Ferme la connexion"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("Connexion fermée")
    
    def is_connected(self):
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT 1")
            return True
        except Exception:
            return False
