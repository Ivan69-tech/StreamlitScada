from modbus import ModbusClient
from collections import deque
import time

class SMT:
    def __init__(self, host="localhost", port=5502):
        self.P_kW = deque(maxlen=10)
        self.Q_kVar = deque(maxlen=10)
        self.state = deque(maxlen=10)
        self.watchdog = deque(maxlen=10)
        self.soc = 0
        
        self.mc = ModbusClient(host=host, port=port)
        self.connected = False

    def checkConnection(self) :
        self.connected = self.mc.client.connect()
        
    
    def Read(self):
        """Lit les valeurs Modbus et met à jour les deque, ignore les None"""
        val_state = self.mc.read_input_uint32(0x2502)
        val_P = self.mc.read_input_int32(0x2518)
        val_Q = self.mc.read_input_int32(0x251a)
        val_watchdog = self.mc.read_holding_int32(0xd000)
        val_soc = self.mc.read_input_int32(0x2504)
        
        if val_state is not None:
            self.state.append(val_state)
        if val_P is not None:
            self.P_kW.append(val_P)
        if val_Q is not None:
            self.Q_kVar.append(val_Q)
        if val_watchdog is not None:
            self.watchdog.append(val_watchdog)
        if val_soc is not None:
            self.soc = val_soc / 100
        
    
    def Watchdog(self):
        """Cycle d’écriture automatique sur watchdog"""
        a = 0
        while True:
            self.mc.write_int32(0xd000, a)
            a += 1
            if a > 10:
                a = 0
            time.sleep(1)
    
    def StartBess(self):
        self.mc.write_uint32(0xd002, 4)
    
    def ShutDownBess(self):
        self.mc.write_uint32(0xd002, 1)
    
    def SetP(self, P):
        print(f"Set P = {P}")
        self.mc.write_int32(0xd004, P)
    
    def SetQ(self, Q):
        print(f"Set Q = {Q}")
        self.mc.write_int32(0xd006, Q)

    def ClearFaults(self):
        self.mc.write_int32(0xd00a, 0xFF)
