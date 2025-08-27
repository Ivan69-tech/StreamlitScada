from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ConnectionException
import struct
import time

class ModbusClient:
    def __init__(self, host="localhost", port=5502):
        """
        Initialise le client Modbus TCP.
        """
        self.host = host
        self.port = port
        # Low timeouts to avoid UI blocking
        self.client = ModbusTcpClient(host=host, port=port, timeout=1)

    def connect(self) -> bool:
        try:
            if self.client is None:
                self.client = ModbusTcpClient(host=self.host, port=self.port, timeout=1)
            return bool(self.client.connect())
        except Exception:
            return False

    def ensure_connected(self) -> bool:
        if self.client is None:
            return self.connect()
        try:
            if not self.client.connected:
                return self.connect()
            return True
        except Exception:
            return self.connect()

        
    # --- Lecture ---
    def read_coils(self, address, count=1, device_id=1):
        if self.client is None:
            return None
        try:
            self.ensure_connected()
            result = self.client.read_coils(address, count, device_id=device_id)
            if not result.isError():
                return result.bits
            else:
                print(f"Erreur lecture coils à {address}")
                return None
        except Exception as e:
            print(f"Erreur lecture coils : {e}")
            return None

    def read_discrete_inputs(self, address, count=1, device_id=1):
        if self.client is None:
            return None
        try:
            self.ensure_connected()
            result = self.client.read_discrete_inputs(address, count, device_id=device_id)
            if not result.isError():
                return result.bits
            else:
                print(f"Erreur lecture discrete inputs à {address}")
                return None
        except Exception as e:
            print(f"Erreur lecture discrete inputs : {e}")
            return None

    def read_holding_registers(self, address, count=1, device_id=1):
        if self.client is None:
            return None
        try:
            self.ensure_connected()
            result = self.client.read_holding_registers(address, count, device_id=device_id)
            if not result.isError():
                return result.registers
            else:
                print(f"Erreur lecture holding registers à {address}")
                return None
        except Exception as e:
            print(f"Erreur lecture holding registers : {e}")
            return None

    def read_input_registers(self, address, count=1, device_id=1):
        if self.client is None:
            return None
        try:
            self.ensure_connected()
            result = self.client.read_input_registers(address, count, device_id=device_id)
            if not result.isError():
                return result.registers
            else:
                print(f"Erreur lecture input registers à {address}")
                return None
        except Exception as e:
            print(f"Erreur lecture input registers : {e}")
            return None

    # --- Écriture ---
    def write_coil(self, address, value, device_id=1):
        if self.client is None:
            return False
        try:
            self.ensure_connected()
            result = self.client.write_coil(address, value, device_id=device_id)
            return not result.isError()
        except Exception as e:
            print(f"Erreur écriture coil : {e}")
            return False

    def write_register(self, address, value, device_id=1):
        if self.client is None:
            return False
        try:
            self.ensure_connected()
            result = self.client.write_register(address, value, device_id=device_id)
            return not result.isError()
        except Exception as e:
            print(f"Erreur écriture register : {e}")
            return False

    # --- Cycle d’écriture / lecture ---
    def cycle_holding_registers(self, start=0, stop=10, delay=2, address=0, device_id=1):
        a = start
        while True:
            self.write_register(address, a, device_id)
            print(f"Écrit {a} dans le holding register {address}")
            a += 1
            if a > stop:
                a = start
            time.sleep(delay)

    # --- Int32 / Uint32 ---
    def read_holding_int32(self, address, device_id=1, byteorder='big'):
        if self.client is None:
            return None
        try:
            self.ensure_connected()
            response = self.client.read_holding_registers(address, count=2, device_id=device_id)
            if response.isError():
                return None
            regs = response.registers
            b = struct.pack('>HH' if byteorder=='big' else '<HH', regs[0], regs[1])
            return struct.unpack('>i' if byteorder=='big' else '<i', b)[0]
        except Exception as e:
            print(f"Erreur lecture holding int32 : {e}")
            return None

    def read_holding_uint32(self, address, device_id=1, byteorder='big'):
        if self.client is None:
            return None
        try:
            self.ensure_connected()
            response = self.client.read_holding_registers(address, count=2, device_id=device_id)
            if response.isError():
                return None
            regs = response.registers
            b = struct.pack('>HH' if byteorder=='big' else '<HH', regs[0], regs[1])
            return struct.unpack('>I' if byteorder=='big' else '<I', b)[0]
        except Exception as e:
            print(f"Erreur lecture holding uint32 : {e}")
            return None

    def read_input_int32(self, address, device_id=1, byteorder='big'):
        if self.client is None:
            return None
        try:
            self.ensure_connected()
            response = self.client.read_input_registers(address, count=2, device_id=device_id)
            if response.isError():
                return None
            regs = response.registers
            b = struct.pack('>HH' if byteorder=='big' else '<HH', regs[0], regs[1])
            return struct.unpack('>i' if byteorder=='big' else '<i', b)[0]
        except Exception as e:
            print(f"Erreur lecture input int32 : {e}")
            return None

    def read_input_uint32(self, address, device_id=1, byteorder='big'):
        if self.client is None:
            return None
        try:
            self.ensure_connected()
            response = self.client.read_input_registers(address, count=2, device_id=device_id)
            if response.isError():
                return None
            regs = response.registers
            b = struct.pack('>HH' if byteorder=='big' else '<HH', regs[0], regs[1])
            return struct.unpack('>I' if byteorder=='big' else '<I', b)[0]
        except Exception as e:
            print(f"Erreur lecture input uint32 : {e}")
            return None

    def write_int32(self, address, value, device_id=1):
        if self.client is None:
            return False
        try:
            self.ensure_connected()
            hi, lo = struct.unpack(">HH", struct.pack(">i", value))
            return self.client.write_registers(address, [hi, lo], device_id=device_id)
        except Exception as e:
            print(f"Erreur écriture int32 : {e}")
            return False

    def write_uint32(self, address, value, device_id=1):
        if self.client is None:
            return False
        try:
            self.ensure_connected()
            hi, lo = struct.unpack(">HH", struct.pack(">I", value))
            return self.client.write_registers(address, [hi, lo], device_id=device_id)
        except Exception as e:
            print(f"Erreur écriture uint32 : {e}")
            return False
