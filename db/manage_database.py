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
        """Établit la connexion à la base de données avec timeout et keepalive"""
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                port=self.port,
                connect_timeout=3,
                keepalives=1,
                keepalives_idle=30,
                keepalives_interval=10,
                keepalives_count=3,
            )
            self.cursor = self.conn.cursor(cursor_factory=extras.RealDictCursor)
            print("Connexion réussie à PostgreSQL")
        except Exception as e:
            print("Erreur de connexion :", e)

    def ensure_connection(self):
        """Reconnecte si nécessaire."""
        try:
            if self.conn is None or self.conn.closed:
                self.connect()
                return
            # ping
            with self.conn.cursor() as cur:
                cur.execute("SELECT 1")
        except Exception:
            # reconnect
            self.connect()

    def execute_query(self, query, params=None):
        """Exécute une requête SELECT et retourne les résultats"""
        try:
            self.ensure_connection()
            self.cursor.execute(query, params)
            result = self.cursor.fetchall()
            print("requete ok")
            return result
        except Exception as e:
            print("Erreur lors de l’exécution de la requête :", e)
            return None

    def execute_write(self, query, params=None):
        """Exécute une requête INSERT/UPDATE/DELETE et commit"""
        try:
            self.ensure_connection()
            self.cursor.execute(query, params)
            self.conn.commit()
        except Exception as e:
            try:
                if self.conn:
                    self.conn.rollback()
            except Exception:
                pass
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
            if self.conn is None or self.conn.closed:
                return False
            with self.conn.cursor() as cur:
                cur.execute("SELECT 1")
            return True
        except Exception:
            return False
