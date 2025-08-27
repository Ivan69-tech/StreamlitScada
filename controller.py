from modbus import ModbusClient
from collections import deque
from db.manage_database import PostgresDB
import time
import os
import os.path


class SMT:
    def __init__(self, context, host=None, port=5502):
        # Determine host: env var overrides; else detect Docker; fallback to localhost
        default_host = "python-client-modbus" if os.path.exists("/.dockerenv") else "localhost"
        resolved_host = os.getenv("MODBUS_HOST", host if host is not None else default_host)

        # historiques des mesures
        self.P_kW = deque(maxlen=10)
        self.Q_kVar = deque(maxlen=10)
        self.state = deque(maxlen=10)
        self.watchdog = deque(maxlen=10)
        self.soc = deque(maxlen=10)

        self.context = context  # dictionnaire partagé

        self.connected = False
        self.db_connected = False

        # Connexion DB
        self.db = PostgresDB(
            host=os.getenv("DB_HOST"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT")
        )

        print(os.getenv("DB_HOST"))
        
        if self.db_connected :
            self.create_table()

        # Connexion Modbus
        self.mc = ModbusClient(host=resolved_host, port=port)
        

    def check_connection(self):
        """Vérifie et rétablit la connexion Modbus sans bloquer."""
        try:
            self.connected = self.mc.connect()
        except Exception:
            self.connected = False
    
    def check_db_connection(self):
        try:
            self.db_connected = self.db.is_connected()
            if not self.db_connected:
                self.db.connect()
                self.db_connected = self.db.is_connected()
        except Exception:
            self.db_connected = False

    def read(self):
        """Lit les valeurs Modbus et met à jour les deque + contexte"""
        val_state = self.mc.read_input_uint32(0x2502)
        val_P = self.mc.read_input_int32(0x2518)
        val_Q = self.mc.read_input_int32(0x251a)
        val_watchdog = self.mc.read_holding_int32(0xd000)
        val_soc = self.mc.read_input_int32(0x2504)

        if val_state is not None:
            self.state.append(val_state)
            self.context.add("state", val_state)
        if val_P is not None:
            self.P_kW.append(val_P)
            self.context.add("p", val_P)
        if val_Q is not None:
            self.Q_kVar.append(val_Q)
            self.context.add("q", val_Q)
        if val_watchdog is not None:
            self.watchdog.append(val_watchdog)
            self.context.add("watchdog", val_watchdog)
        if val_soc is not None:
            soc_value = val_soc / 100
            self.soc.append(soc_value)
            self.context.add("soc", soc_value)

        if self.db_connected:
            self.save_context()

    def watchdog_cycle(self):
        """Cycle d’écriture automatique sur watchdog"""
        a = 0
        while True:
            try:
                self.mc.write_int32(0xd000, a)
                a += 1
                if a > 10:
                    a = 0
            except Exception:
                pass
            time.sleep(1)

    def start_bess(self):
        self.mc.write_uint32(0xd002, 4)

    def shutdown_bess(self):
        self.mc.write_uint32(0xd002, 1)

    def set_P(self, P):
        print(f"Set P = {P}")
        self.mc.write_int32(0xd004, P)

    def set_Q(self, Q):
        print(f"Set Q = {Q}")
        self.mc.write_int32(0xd006, Q)

    def clear_faults(self):
        self.mc.write_int32(0xd00a, 0xFF)

    def create_table(self):
        """Crée la table context si elle n’existe pas déjà"""
        self.db.execute_write(
            """
            CREATE TABLE IF NOT EXISTS context (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMPTZ DEFAULT NOW()
            )
            """
        )

    def save_context(self):
        """Insère les valeurs du contexte, crée les colonnes si besoin"""
        try:
            # Vérifier et ajouter les colonnes manquantes
            for key in self.context.context.keys():
                self.db.execute_write(
                    f"""
                    ALTER TABLE context
                    ADD COLUMN IF NOT EXISTS {key} DOUBLE PRECISION
                    """
                )

            # Construire la requête d’INSERT dynamiquement
            columns = ", ".join(self.context.context.keys())
            placeholders = ", ".join(["%s"] * len(self.context.context))
            values = list(self.context.context.values())

            query = f"""
                INSERT INTO context ({columns})
                VALUES ({placeholders})
            """

            self.db.execute_write(query, values)

        except Exception as e:
            print("Erreur lors de la sauvegarde du contexte :", e)

