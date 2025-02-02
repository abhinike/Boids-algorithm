import math
import pygame
from constants import *
from tools import *
class Button:
    def __init__(self, text, position = (Width-230, 600) , w = 100, h= 50, border=10, color = (0, 0, 0), borderColor = (64, 123, 158)):
        self.text = text
        self.position = position
        self.w = w
        self.h = h
        self.border = border
        self.temp = color
        self.color = color
        self.borderColor = borderColor
        self.font = 'freesansbold.ttf'
        self.fontSize = 25
        self.textColor = (255, 255, 255)
        self.state = False
        self.action = None

    def HandleMouse(self, HoverColor = (100, 100, 100)):
        m = pygame.mouse.get_pos()
        self.state = False
        if m[0] >= self.position[0] and m[0] <= self.position[0] + self.w:
            if m[1] >= self.position[1] and m[1] <= self.position[1] + self.h:
                self.color = HoverColor
                if pygame.mouse.get_pressed()[0]:
                    self.color = (200, 200, 200)
                    if self.action == None:
                        self.state = True
            else:
                self.color = self.temp
        else:
            self.color = self.temp


    def Render(self, screen):
        self.HandleMouse()
        font = pygame.font.Font(self.font, self.fontSize)
        text = font.render(self.text, True, self.textColor)
        textRect = text.get_rect()
        textRect.center = (self.position[0]+self.w//2, self.position[1]+self.h//2)
        if self.border > 0:
            pygame.draw.rect(screen, self.borderColor, pygame.Rect(self.position[0] - self.border//2, self.position[1] - self.border//2, self.w + self.border, self.h + self.border))
        pygame.draw.rect(screen, self.color, pygame.Rect(self.position[0], self.position[1], self.w, self.h))

        screen.blit(text, textRect)

class Panel:
    def __init__(self, position = (Width-350, 100), w= 345, h= 500, color=(8, 3, 12), alpha=128):
        self.position = position
        self.w = w
        self.h = h
        self.color = color
        self.alpha = alpha

    def Render(self, screen):
        s = pygame.Surface((self.w, self.h))
        s.set_alpha(self.alpha)
        s.fill(self.color)
        screen.blit(s, (self.position[0], self.position[1]))
        # pygame.draw.rect(screen, self.color, pygame.Rect(self.position[0], self.position[1], self.w, self.h))
     
     
class Highway:
    def __init__(self, lanes=4, lane_width=100, dash_length=20, dash_gap=20):
        self.width = 400
        self.length = Width
        self.lanes = lanes
        self.lane_width = lane_width
        self.dash_length = dash_length
        self.dash_gap = dash_gap
        # highway coordinates
        self.top_left_coordinate = (0, 0)
        self.bottom_left_coordinate = (0, 400)
        self.top_right_coordinate = (Width, 0)
        self.bottom_right_coordinate = (Width,400)

    def draw_dashed_line(self, screen, color, start_pos, end_pos, width=1):
        x1, y1 = start_pos
        x2, y2 = end_pos
        dl = self.dash_length
        dg = self.dash_gap
        if x1 == x2:  # Vertical dashed line
            for y in range(y1, y2, dl + dg):
                pygame.draw.line(screen, color, (x1, y), (x1, min(y + dl, y2)), width)
        elif y1 == y2:  # Horizontal dashed line
            for x in range(x1, x2, dl + dg):
                pygame.draw.line(screen, color, (x, y1), (min(x + dl, x2), y1), width)

    def render(self, screen):
        highway_rect = pygame.Rect(self.top_left_coordinate[0], self.top_left_coordinate[1], self.length, self.width)
        pygame.draw.rect(screen, (50, 50, 50), highway_rect)

        for i in range(1, self.lanes):
            lane_y = highway_rect.top + i * self.lane_width
            self.draw_dashed_line(screen, (255, 255, 255), (0, lane_y), (self.length, lane_y), 2)

class Highway2:
    def __init__(self, screen_width, lanes=2, lane_width=100, dash_length=20, dash_gap=20):
        self.width = 400
        self.length = screen_width
        self.lanes = lanes
        self.lane_width = lane_width
        self.dash_length = dash_length
        self.dash_gap = dash_gap
        # highway2 coordinates
        self.top_left_coordinate = (500, 400)
        self.bottom_left_coordinate = (700, 400)
        self.top_right_coordinate = (0, Height)
        self.bottom_right_coordinate = (200, Height)

    def draw_dashed_line(self, screen, color, start_pos, end_pos, width=1):
        x1, y1 = start_pos
        x2, y2 = end_pos
        dl = self.dash_length
        dg = self.dash_gap
        angle = math.atan2(y2 - y1, x2 - x1)
        dx = dl * math.cos(angle)
        dy = dl * math.sin(angle)
        gap_dx = dg * math.cos(angle)
        gap_dy = dg * math.sin(angle)
        while math.hypot(x2 - x1, y2 - y1) > dl:
            pygame.draw.line(screen, color, (x1, y1), (x1 + dx, y1 + dy), width)
            x1 += dx + gap_dx
            y1 += dy + gap_dy

    def render(self, screen):
        # Define the polygon points for the highway at a 30-degree angle
        highway_2_polygon = [
            self.top_left_coordinate,
            self.bottom_left_coordinate,
            self.bottom_right_coordinate,
            self.top_right_coordinate
        ]
        pygame.draw.polygon(screen, (50, 50, 50), highway_2_polygon)

        # Draw dashed lines for the lanes
        for i in range(1, self.lanes):
            offset = i * self.lane_width
            start_pos = (self.top_left_coordinate[0] + offset, self.top_left_coordinate[1])
            end_pos = (self.bottom_left_coordinate[0] + offset, self.bottom_left_coordinate[1])
            self.draw_dashed_line(screen, (255, 255, 255), start_pos, end_pos, 2)


class ToggleButton:
    def __init__(self, position= ((Width-200, 400)), w = 30, h=30, state=False, color=(40, 40, 10), activeColor=(240, 140, 60)):
        self.position = position
        self.w = w
        self.h = h
        self.clicked = False
        self.state = state
        self.temp = (activeColor, color)
        self.activeColor = activeColor
        self.color = color

    def HandleMouse(self, HoverColor = (150, 120, 40)):
        m = pygame.mouse.get_pos()

        if m[0] >= self.position[0] and m[0] <= self.position[0] + self.w:
            if m[1] >= self.position[1] and m[1] <= self.position[1] + self.h:
                self.color = HoverColor
                self.activeColor = HoverColor
                if self.clicked:
                    self.state = not self.state
                    self.color = (255, 255, 255)
            else:
                self.color = self.temp[1]
                self.activeColor =self.temp[0]
        else:
            self.color = self.temp[1]
            self.activeColor =self.temp[0]

    def Render(self, screen, clicked):
        self.HandleMouse()
        self.clicked = clicked
        if self.state == True:
            pygame.draw.rect(screen, self.activeColor, pygame.Rect(self.position[0], self.position[1], self.w, self.h))
        else:
            pygame.draw.rect(screen, self.color, pygame.Rect(self.position[0], self.position[1], self.w, self.h))
        return self.state
class TextUI:
    def __init__(self,text, position, fontColor):
        self.position = position
        self.text = text
        self.font = 'freesansbold.ttf'
        self.fontSize = 18
        self.fontColor = fontColor
    def Render(self, screen):
        font = pygame.font.Font(self.font, self.fontSize)
        text = font.render(self.text, True, self.fontColor)
        textRect = text.get_rect()
        textRect.center = (self.position[0], self.position[1])
        screen.blit(text, textRect)

class DigitInput:
    def __init__(self,startingValue, position = (Width-320, 100), w= 300, h= 600, color=(8, 3, 12)):
        self.position = position
        self.text = str(startingValue)
        self.fontColor = (255, 255, 255)
        self.fontSize = 18
        self.font = 'freesansbold.ttf'
        self.w = w
        self.h = h
        self.color = color
        self.value  = int(self.text)
        self.hoverEnter = False

    def Check(self, backspace,val):

        if self.hoverEnter == True:
            if backspace == True:

                if len(str(self.value)) <= 0 or len(str(self.value))-1 <= 0:
                    self.value = 0
                else:
                    self.value = int(str(self.value)[:-1])

            else:
                if self.text.isdigit():
                    self.value = int(str(self.value) + str(self.text))
                else:
                    for el in self.text:
                        if el.isdigit() != True:
                            self.text = self.text.replace(el, "")
        backspace == False
        self.text = ""




    def updateText(self, val, pressed):
        m = pygame.mouse.get_pos()
        if m[0] >= self.position[0] and m[0] <= self.position[0] + self.w:
            if m[1] >= self.position[1] and m[1] <= self.position[1] + self.h:
                self.hoverEnter = True
                if pressed == True:
                    self.text += val
            else:
                self.hoverEnter = False
                val = ""
        else:
            self.hoverEnter = False
            val = ""


    def Render(self, screen, val, backspace, pressed):
        self.updateText(val, pressed)
        self.Check(backspace, val)
        font = pygame.font.Font(self.font, self.fontSize)
        text = font.render(str(self.value), True, self.fontColor)
        textRect = text.get_rect()
        textRect.center = (self.position[0]+self.w//2, self.position[1]+self.h//2)
        pygame.draw.rect(screen, self.color, pygame.Rect(self.position[0], self.position[1], self.w, self.h))
        screen.blit(text, textRect)

class Slider:
    def __init__(self,x, y, val, min1, max1, length, h, max=500):
        self.value = val
        self.x = x
        self.y = y
        self.h = h
        self.min1 = min1
        self.max1 = max1
        self.length = length
        self.lineColor = (20, 10, 20)
        self.rectradius = 10
        self.temp_radius = self.rectradius
        self.rectColor = (255, 255, 255)
        self.v = 0.4
        self.temp = self.lineColor
        self.max = max

    def Calculate(self, val):
        self.v = translate(val, 0, self.length, 0, 1)
        self.value = self.v * self.max

    def HandleMouse(self):
        mx, my = pygame.mouse.get_pos()

        if mx >= self.x and mx <= self.x + self.length:
            if my >= self.y and my <= self.y + self.h:
                self.rectradius = 15
                if pygame.mouse.get_pressed()[0]:
                    self.Calculate(mx - self.x)
            else:
                self.lineColor = self.temp
                self.rectradius = self.temp_radius
        else:
            self.lineColor = self.temp
            self.rectradius = self.temp_radius

    def Render(self,screen):
        self.HandleMouse()
        pygame.draw.rect(screen, self.lineColor, pygame.Rect(self.x, self.y, self.length, self.h))
        x = int((self.v * self.length) + self.x)
        pygame.draw.rect(screen, self.rectColor, pygame.Rect(self.x, self.y, int( self.v * self.length), self.h))
        pygame.draw.circle(screen, (130, 213, 151), (x, self.y + (self.rectradius/2)), self.rectradius)
        return self.value
