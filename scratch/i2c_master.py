from smbus import SMBus
addr = 0x8
bus = SMBus(1)

numb = 1

print("Enter 1 to turn ON and 0 to turn OFF")
while numb == 1:
	ledState = input(">>> ")
	if ledState == "1":
		bus.write_byte(addr, 0x1) # turn ON
	elif ledState == "0":
		bus.write_byte(addr, 0x0) # turn OFF
	else:
		numb = 0
