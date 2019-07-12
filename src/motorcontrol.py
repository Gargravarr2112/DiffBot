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

speedPercent = 50

def turnLeft():
	GPIO.output(DIG2, GPIO.LOW)
	steeringMotor.start(speedPercent)
	sleep(0.2)
	steeringMotor.stop()

def turnRight():
	GPIO.output(DIG2, GPIO.HIGH)
	steeringMotor.start(speedPercent)
	sleep(0.2)
	steeringMotor.stop()

def creepForward():
	GPIO.output(DIG1, GPIO.HIGH)
	driveMotor.start(speedPercent)
	sleep(1)
	driveMotor.stop()

def creepBackward():
	GPIO.output(DIG1, GPIO.LOW)
	driveMotor.start(speedPercent)
	sleep(1)
	driveMotor.stop()

def driveForward():
	GPIO.output(DIG1, GPIO.HIGH)
	driveMotor.start(speedPercent)

def driveBackward():
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
			driveForward()
		elif command == ord('s'):
			stop()
			driveBackward()
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