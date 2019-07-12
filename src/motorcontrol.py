#!/usr/bin/env python3

import RPi.GPIO as GPIO
from time import sleep
import curses

GPIO.setmode(GPIO.BCM)

#Uses Cytron HAT-MDD10 2-way motor driver board
#2x PWM outputs (pins 12 and 13) for motor speed control
#2x digital outputs (24 and 26) to control motor direction

AN2 = 13        # set pwm2 pin on MD10-Hat
AN1 = 12        # set pwm1 pin on MD10-hat
DIG2 = 24       # set dir2 pin on MD10-Hat
DIG1 = 26       # set dir1 pin on MD10-Hat
PWM_FREQUENCY = 100
GPIO.setup(AN2, GPIO.OUT)     # set pin as output
GPIO.setup(AN1, GPIO.OUT)     # set pin as output
GPIO.setup(DIG2, GPIO.OUT)    # set pin as output
GPIO.setup(DIG1, GPIO.OUT)    # set pin as output
driveMotor = GPIO.PWM(AN1, PWM_FREQUENCY)       # set pwm for M1, 100Hz
steeringMotor = GPIO.PWM(AN2, PWM_FREQUENCY)       # set pwm for M2, 100Hz

defaultSpeedPercent = 50
steeringSpeedPercent = 75

def turnLeft():
	GPIO.output(DIG2, GPIO.LOW)
	steeringMotor.start(steeringSpeedPercent)
	sleep(0.1)
	steeringMotor.stop()

def turnRight():
	GPIO.output(DIG2, GPIO.HIGH)
	steeringMotor.start(steeringSpeedPercent)
	sleep(0.1)
	steeringMotor.stop()

def inchForward():
	GPIO.output(DIG1, GPIO.HIGH)
	driveMotor.start(defaultSpeedPercent)
	sleep(1)
	driveMotor.stop()

def inchBackward():
	GPIO.output(DIG1, GPIO.LOW)
	driveMotor.start(defaultSpeedPercent)
	sleep(1)
	driveMotor.stop()

def driveForward(speedPercent):
	GPIO.output(DIG1, GPIO.HIGH)
	driveMotor.start(speedPercent)

def driveBackward(speedPercent):
	GPIO.output(DIG1, GPIO.LOW)
	driveMotor.start(speedPercent)

def stop():
	driveMotor.stop()
	steeringMotor.stop()

def driveWASD():
	screen = curses.initscr()
	curses.noecho()
	curses.cbreak()
	screen.keypad(True)
	screen.insstr("W-A-S-D to drive")
	while (True):
		command = screen.getch()
		if command == ord('w'):
			stop()
			driveForward(defaultSpeedPercent)
		elif command == ord('s'):
			stop()
			driveBackward(defaultSpeedPercent)
		elif command == ord('a'):
			turnLeft()
		elif command == ord('d'):
			turnRight()
		elif command == ord('e'):
			stop()
		elif command == ord('q'):
			stop()
			break
	curses.echo()
	curses.nocbreak()
	screen.keypad(0)
	curses.endwin()

if __name__ == "__main__":
	driveWASD()