import evdev
from evdev import ecodes
from motorcontrol import driveForward, driveBackward, turnLeft, turnRight, stop

#gamepadBTAddress = '98:58:8A:02:39:81'
gamepadName = 'Samsung Game Pad EI-GP20'

#Find the device

gamepad = [device for device in [evdev.InputDevice(path) for path in evdev.list_devices()] if device.name == gamepadName]

gamepadCodes = { 0: 'ANALOG_L_X', 1: 'ANALOG_L_Y', 3: 'ANALOG_R_X', 4: 'ANALOG_R_Y', 16: 'DPAD_X', 17: 'DPAD_Y', 304: 'BUTTON_ONE', 305: 'BUTTON_TWO', 307: 'BUTTON_THREE', 308: 'BUTTON_FOUR', 310: 'BUTTON_SHOULDERL', 311: 'BUTTON_SHOULDERR', 314: 'BUTTON_SELECT', 315: 'BUTTON_START', 319: 'BUTTON_PLAY' }

stickMin = 0
stickMax = 255
stickZero = 128

if len(gamepad) == 0:
	print("Could not find gamepad in input device list, is bluetooth connected?")
	exit()
else:
	gamepad = gamepad[0]

#Linux EvDev interface:
#-code == which subdevice generated the event
#-type == what kind of input event - EV_SYN is a delimiter
#-value == analog or digital value
def debug():
	for event in gamepad.read_loop():
		eCode = event.code
		eType = event.type
		eValue = event.value
		print("Code: {0}\t\tType: {1}\t\tValue: {2}".format(gamepadCodes[eCode], evdev.ecodes.EV[eType], eValue))

#Formula contributed by Owen
def calculateDrivePercent(analogValue):
	if analogValue == 128: #Stop, shouldn't happen
		return 0
	elif analogValue < 128: #Forward
		return int(100 * (128 - analogValue) / 128)
	else: #Backward
		return int(100 * (analogValue - 128) / 127)

def driveByGamepad():
	for event in gamepad.read_loop():
		eType = event.type
		eCode = event.code
		eValue = event.value
		if eType == ecodes.EV_ABS: #Analog stick
			print("Analog stick")
			if eCode == 1: #L Y-axis, throttle
				print("Left-Y")
				if eValue == 128: #Centred stick
					print("Stop")
					stop()
				elif eValue < 128: #Forward
					speedPercent = calculateDrivePercent(eValue)
					print("Forward {0}%".format(speedPercent))
					driveForward(speedPercent)
				elif eValue > 128: #Backward
					speedPercent = calculateDrivePercent(eValue)
					print("Backward {0}%".format(speedPercent))
					driveBackward(speedPercent)
		elif eType == ecodes.EV_KEY: #Button
			print("Button")
			if eCode == 304: #Button 1, stop
				print("Stop")
				stop()
			elif eCode == 310: #ShoulderL, turn left
				print("Left")
				turnLeft()
			elif eCode == 311: #ShoulderR, turn right
				print("Right")
				turnRight()