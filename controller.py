from modbus import ModbusClient
from collections import deque
import time

class SMT:
    def __init__(self, host="localhost", port=5502):
        self.P_kW = deque(maxlen=10)
        self.Q_kVar = deque(maxlen=10)
        self.state = deque(maxlen=10)
        self.watchdog = deque(maxlen=10)
        
        self.mc = ModbusClient(host=host, port=port)
    
    def Read(self):
        self.state.append(self.mc.read_input_uint32(0x2502))
        self.P_kW.append(self.mc.read_input_int32(0x2518))
        self.Q_kVar.append(self.mc.read_input_int32(0x251a))
        self.watchdog.append(self.mc.read_holding_int32(0xd000))
    
    def Watchdog(self):
        a = 0
        while True :
            self.mc.write_int32(0xd000,a)
            a += 1
            if a > 10 :
                a = 0
            time.sleep(1)
        
