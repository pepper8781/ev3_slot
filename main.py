#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                
                                InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import random
import time  # Add this line to import the 'time' module
from pybricks.media.ev3dev import Font

# Create your objects here.
ev3 = EV3Brick()

# Write your program here.
ev3.speaker.beep()

big_font = Font(size=120)
ev3.screen.set_font(big_font)

class Slot():
    def __init__(self, max_number, button, x, y):
        self.max_number = max_number
        self.count = random.randint(0, self.max_number - 1)
        self.numbers = [i for i in range(1, self.max_number + 1)]
        self.presentNumber = self.numbers[self.count % self.max_number]
        self.isMoving = True
        self.button = button
        self.x = x
        self.y = y
        
    def turn(self):
        if self.isMoving:
            self.count += 1
            self.presentNumber = self.numbers[self.count % self.max_number]
    
    def button_pressed(self):
        if self.button in ev3.buttons.pressed():
            while self.button in ev3.buttons.pressed():
                pass
            if self.isMoving:
                self.isMoving = False
    
    def show(self):
        ev3.screen.draw_text(self.x, self.y, str(self.presentNumber))

class Game():
    def __init__(self):
        self.max_number = 7
        self.left = Slot(self.max_number, Button.LEFT, 58, 68)
        self.center = Slot(self.max_number, Button.CENTER, 174, 68)
        self.right = Slot(self.max_number, Button.RIGHT, 290, 68)
        self.game_over = False
        self.refresh_rate = 100

    def turn(self):
        self.left.turn()
        self.center.turn()
        self.right.turn()

    def button_pressed(self):
        self.left.button_pressed()
        self.center.button_pressed()
        self.right.button_pressed()

    def show(self):
        self.left.show()
        self.center.show()
        self.right.show()
    
    def check_game_over(self):
        if self.left.isMoving == False and self.center.isMoving == False and self.right.isMoving == False:
            if self.left.presentNumber == self.center.presentNumber and self.center.presentNumber == self.right.presentNumber:
                self.game_over = True
        else:
            self.game_over = False
    
    def game_over_show(self):
        ev3.screen.clear()
        ev3.speaker.beep()
        ev3.screen.draw_text(58,68,"clear!")
        wait(3000)
    
    def process(self):
        self.turn()
        self.button_pressed()
        self.show()
        self.check_game_over()
        wait(self.refresh_rate)

game = Game()

while not game.game_over:
    game.process()
game.game_over_show()