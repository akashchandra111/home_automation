from House.house import House
from serial_comm.serial_comm import Bserial as Bluetooth

h = House()
msg_handler = Bluetooth("98:D3:35:00:C9:F8")
