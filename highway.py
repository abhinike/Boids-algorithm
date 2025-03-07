from codecs import strict_errors

import pygame
from constants import *
from tools import *
from abc import ABC, abstractmethod
from tools import Vector
from random import uniform
from math import pi


class Highway(ABC):  # Abstract base class
    def __init__(self, lanes, lane_width, dash_length, dash_gap):
        self.lanes = lanes
        self.lane_width = lane_width
        self.dash_length = dash_length
        self.dash_gap = dash_gap

    @abstractmethod
    def render(self, screen):
        """Abstract method to render the highway"""
        pass
    
    @abstractmethod
    def limits(self, boid ):
        """Abstract method to keep boids within highway boundaries"""
        pass

    @abstractmethod
    def avoid_boundary(self, boid ):
        """Abstract method to avoid boundary of highway"""
        pass

    def draw_dashed_line(self, screen, color, start_pos, end_pos, width=1):
        """Utility method to draw dashed lines"""
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


class Highway1(Highway):  # Horizontal Highway
    def __init__(self, lanes=4, lane_width=100, dash_length=20, dash_gap=20):
        super().__init__(lanes, lane_width, dash_length, dash_gap)
        self.width = lanes * lane_width
        self.length = Width
        self.top_left_coordinate = (0, 0)
        self.bottom_left_coordinate = (0, self.width)
        self.top_right_coordinate = (Width, 0)
        self.bottom_right_coordinate = (Width, self.width)
        self.direction = Vector(1, 0)
        self.boids = []  # Store boids within this highway

    def add_boid(self, boid):
        """Add a boid to the highway"""
        self.boids.append(boid)

    def render(self, screen):
        highway_rect = pygame.Rect(self.top_left_coordinate[0], self.top_left_coordinate[1], self.length, self.width)
        pygame.draw.rect(screen, (50, 50, 50), highway_rect)

        for i in range(1, self.lanes):
            lane_y = highway_rect.top + i * self.lane_width
            self.draw_dashed_line(screen, (255, 255, 255), (0, lane_y), (self.length, lane_y), 2)



    def limits(self, boid):
        """Keep boids within highway boundaries"""
        if boid.position.x < 0:
            boid.position.x = self.length
        elif boid.position.x > self.length:
            boid.position.x = 0

        highway_top = 0
        highway_bottom = self.bottom_left_coordinate[1] - 50

        if boid.position.y < highway_top:
            boid.position.y = highway_top
        elif boid.position.y > highway_bottom:
            boid.position.y = highway_bottom

    def avoid_boundary(self, boid):
        total = 0
        steering = Vector(0, 0)


        # Avoid edges of the highway
        if boid.position.y - boid.radius < HighwayTop:
            edge_steering = Vector(0, 1)
            steering.add(edge_steering)
            total += 1
        elif boid.position.y + boid.radius > HighwayBottom:
            edge_steering = Vector(0, -1)
            steering.add(edge_steering)
            total += 1

        return total, steering




    


class Highway2(Highway):  # Angled Highway
    def __init__(self, screen_width, lanes=2, lane_width=100, dash_length=20, dash_gap=20):
        super().__init__(lanes, lane_width, dash_length, dash_gap)
        self.width = lanes * lane_width
        self.length = screen_width
        self.top_left_coordinate = (500, 400)
        self.top_right_coordinate = (700, 400)
        self.bottom_left_coordinate = (0, Height)
        self.bottom_right_coordinate = (200, Height)
        self.direction = Vector(self.top_left_coordinate[0] - self.bottom_left_coordinate[0], self.top_left_coordinate[1] - self.bottom_left_coordinate[1])

    def render(self, screen):
        highway_2_polygon = [
            self.top_left_coordinate,
            self.bottom_left_coordinate,
            self.bottom_right_coordinate,
            self.top_right_coordinate
        ]
        pygame.draw.polygon(screen, (50, 50, 50), highway_2_polygon)
        
        
    def limits(self, boid):
        return super().limits(boid)


    def avoid_boundary(self, boid):
        total = 0
        steering = Vector(0, 0)


        # Avoid edges of the highway
        if boid.position.y - boid.radius < HighwayTop:
            edge_steering = Vector(0, 1)
            steering.add(edge_steering)
            total += 1
        elif boid.position.y + boid.radius > HighwayBottom:
            edge_steering = Vector(0, -1)
            steering.add(edge_steering)
            total += 1

        return total, steering



