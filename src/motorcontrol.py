#!/usr/bin/env python3

import RPi.GPIO as GPIO
from time import sleep
import curses

GPIO.setmode(GPIO.BCM)

AN2 = 13# set pwm2 pin on MD10-Hat
AN1 = 12# set pwm1 pin on MD10-hat
DIG2 = 24# set dir2 pin on MD10-Hat
DIG1 = 26# set dir1 pin on MD10-Hat
GPIO.setup(AN2, GPIO.OUT)           # set pin as output
GPIO.setup(AN1, GPIO.OUT)           # set pin as output
GPIO.setup(DIG2, GPIO.OUT)          # set pin as output
GPIO.setup(DIG1, GPIO.OUT)          # set pin as output
p1 = GPIO.PWM(AN1, 100)                     # set pwm for M1, 100Hz
p2 = GPIO.PWM(AN2, 100)                     # set pwm for M2, 100Hz

speedPercent = 50

def turnLeft():
	GPIO.output(DIG2, GPIO.LOW)
	p2.start(speedPercent)
	sleep(0.5)
	p2.start(0) #stop

def turnRight():
	GPIO.output(DIG2, GPIO.HIGH)
	p2.start(speedPercent)
	sleep(0.5)
	p2.start(0)

def creepForward():
	GPIO.output(DIG1, GPIO.HIGH)
	p1.start(speedPercent)
	sleep(1)
	p1.start(0)

def creepBackward():
	GPIO.output(DIG1, GPIO.LOW)
	p1.start(speedPercent)
	sleep(1)
	p1.start(0)

def driveForward():
	GPIO.output(DIG1, GPIO.HIGH)
	p1.start(speedPercent)

def driveBackward():
	GPIO.output(DIG1, GPIO.LOW)
	p1.start(speedPercent)

def stop():
	p1.start(0)
	p2.start(0)

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