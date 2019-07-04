#!/usr/bin/env python3

import RPi.GPIO as GPIO
from time import sleep
import curses

GPIO.setmode(GPIO.BCM)

AN2 = 13        # set pwm2 pin on MD10-Hat
AN1 = 12        # set pwm1 pin on MD10-hat
DIG2 = 24       # set dir2 pin on MD10-Hat
DIG1 = 26       # set dir1 pin on MD10-Hat
GPIO.setup(AN2, GPIO.OUT)     # set pin as output
GPIO.setup(AN1, GPIO.OUT)     # set pin as output
GPIO.setup(DIG2, GPIO.OUT)    # set pin as output
GPIO.setup(DIG1, GPIO.OUT)    # set pin as output
p1 = GPIO.PWM(AN1, 100)       # set pwm for M1, 100Hz
p2 = GPIO.PWM(AN2, 100)       # set pwm for M2, 100Hz

turnSpeed = 50

def turnLeft():
	GPIO.output(DIG2, GPIO.LOW)
	p2.start(turnSpeed)
	sleep(0.5)
	p2.start(0) #stop

def turnRight():
	GPIO.output(DIG2, GPIO.HIGH)
	p2.start(turnSpeed)
	sleep(0.5)
	p2.start(0)

def driveWASD():
	currentSpeed = 0
	desiredSpeed = 0
	screen = curses.initscr()
	curses.noecho()
	curses.cbreak()
	screen.keypad(True)
	screen.nodelay(True)
	screen.insstr("W-A-S-D to drive")
	while (True):
		command = screen.getch()
		if command == ord('w'):
			desiredSpeed += 10
			if desiredSpeed > 100:
				desiredSpeed = 100
		elif command == ord('s'):
			desiredSpeed -= 10
			if desiredSpeed < -100:
				desiredSpeed = -100
		elif command == ord('a'):
			turnLeft()
		elif command == ord('d'):
			turnRight()
		elif command == ord('e'):
			desiredSpeed = 0
		elif command == ord('q'):
			p1.start(0)
			break
		if currentSpeed != desiredSpeed:
			currentSpeed += 1 if desiredSpeed > currentSpeed else -1
			GPIO.output(DIG1, GPIO.HIGH if currentSpeed >= 0 else GPIO.LOW)
			p1.start(abs(currentSpeed))
		screen.addstr(5, 2, "Current speed: %d  " % currentSpeed)
		screen.addstr(6, 2, "Desired speed: %d  " % desiredSpeed)
		sleep(0.01)
	curses.echo()
	curses.nocbreak()
	screen.keypad(False)
	screen.nodelay(False)
	curses.endwin()

if __name__ == "__main__":
	driveWASD()