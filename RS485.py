from pymodbus.client import ModbusSerialClient as ModbusClient 
serial = 223025 
cliente = ModbusClient(method="rtu", 
                       port="/dev/ttyUSB0", 
                       stopbits=1, 
                       bytesize=8, 
                       parity='N', 
                       baudrate=9600, 
                       timeout=1)
conexion = cliente.connect()
if conexion:
    print("Conectado")
else:
    print("Error en la conexión")
#result = cliente.read_coils(1)
result = cliente.read_input_registers(address=258,count=1,slave=1)
valor = (result.registers)
print (valor)

result = cliente.read_input_registers(address=20480,count=1,slave=1)
valor = (result.registers)
print (valor)
#result = cliente.read_holding_registers(address=11,count=1,slave=1)
#result = cliente.read_holding_registers(address=20480,count=6,slave=1)
#print(result.registers[0], result.registers[1])
#print (result)
cliente.close()
