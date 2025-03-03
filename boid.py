import pygame
from tools import *
from random import uniform
import colorsys
from matrix import *
from math import pi, sin, cos
from constants import *
from ui import Highway, Highway2 

# def hsvToRGB(h, s, v):
#     return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))

class Boid:
    def __init__(self, x, y):
        self.position = Vector(x, y)
        vec_x = uniform(0.5, 1)
        vec_y = uniform(-0.5, 0.5)
        self.velocity = Vector(vec_x, vec_y)
        self.velocity.normalize()
        # Set a random magnitude
        self.velocity = self.velocity * uniform(1.5, 4)
        self.acceleration = Vector()
        self.color = (255, 255, 255)
        self.temp = self.color
        self.secondaryColor = (70, 70, 70)
        self.max_speed = 5
        self.max_length = 1
        self.size = 2
        self.stroke = 5
        self.angle = 0
        self.hue = 0
        self.toggles = {"separation": True, "alignment": True, "cohesion": True}
        self.values = {"separation": 0.1, "alignment": 0.1, "cohesion": 0.1}
        self.radius = 40

    def behaviour(self, flock):
        self.acceleration.reset()

        if self.toggles["separation"]:
            avoid = self.separation(flock)
            avoid = avoid * self.values["separation"]
            self.acceleration.add(avoid)

        if self.toggles["cohesion"]:
            coh = self.cohesion(flock)
            coh = coh * self.values["cohesion"]
            self.acceleration.add(coh)

        if self.toggles["alignment"]:
            align = self.alignment(flock)
            align = align * self.values["alignment"]
            self.acceleration.add(align)

    def limits(self, screen_width, screen_height, highway : Highway, highway2 : Highway2):
        highway_top = 0
        highway_bottom = highway.bottom_left_coordinate[1] - 50
        

        # Limit x position to screen width
        if self.position.x < 0:
            self.position.x = screen_width
        elif self.position.x > screen_width:
            self.position.x = 0

        # Limit y position to highway boundaries
        if self.position.y < highway_top:
            self.position.y = highway_top
        elif self.position.y > highway_bottom:
            self.position.y = highway_bottom

    def separation(self, flockMates):
        total = 0
        steering = Vector()

        for mate in flockMates:
            dist = getDistance(self.position, mate.position)
            if mate is not self and dist < self.radius:
                temp = SubVectors(self.position, mate.position)
                temp = temp / (dist ** 2)
                steering.add(temp)
                total += 1
        
        # Avoid edges of the highway
        if self.position.y - self.radius < HighwayTop:
            edge_steering = Vector(0, 1)
            steering.add(edge_steering)
            total += 1
        elif self.position.y + self.radius > HighwayBottom:
            edge_steering = Vector(0, -1)
            steering.add(edge_steering)
            total += 1

        if total > 0:
            steering = steering / total
            steering.normalize()
            steering = steering * self.max_speed
            steering = steering - self.velocity
            steering.limit(self.max_length)

        return steering

    def alignment(self, flockMates):
        total = 0
        steering = Vector()

        for mate in flockMates:
            dist = getDistance(self.position, mate.position)
            if mate is not self and dist < self.radius:
                vel = mate.velocity.Normalize()
                steering.add(vel)
                mate.color = hsv_to_rgb(self.hue, 1, 1)
                total += 1

        if total > 0:
            steering = steering / total
            steering.normalize()
            steering = steering * self.max_speed
            steering = steering - self.velocity.Normalize()
            steering.limit(self.max_length)

        return steering

    def cohesion(self, flockMates):
        total = 0
        steering = Vector()

        for mate in flockMates:
            dist = getDistance(self.position, mate.position)
            if mate is not self and dist < self.radius:
                steering.add(mate.position)
                total += 1

        if total > 0:
            steering = steering / total
            steering = steering - self.position
            steering.normalize()
            steering = steering * self.max_speed
            steering = steering - self.velocity
            steering.limit(self.max_length)

        return steering

    def update(self):
        
        # Increase the horizontal component
        self.velocity.x = abs(self.velocity.x) * 1.5  # Ensure positive horizontal direction
        self.velocity.normalize()
        self.position = self.position + self.velocity
        self.velocity = self.velocity + self.acceleration
        self.velocity.limit(self.max_speed)
        self.angle = self.velocity.heading() + pi / 2

    def Draw(self, screen, distance, scale):
        ps = []
        # Change to 4 points for rectangle
        points = [None for _ in range(4)]

        # Define rectangle points
        half_width = self.size // 2
        half_height = self.size // 2
        half_height = 2 * half_height
        points[0] = [[-half_width], [-half_height], [0]]  # Top left
        points[1] = [[half_width], [-half_height], [0]]   # Top right
        points[2] = [[half_width], [half_height], [0]]    # Bottom right
        points[3] = [[-half_width], [half_height], [0]]   # Bottom left

        for point in points:
            rotated = matrix_multiplication(rotationZ(self.angle), point)
            z = 1 / (distance - rotated[2][0])

            projection_matrix = [[z, 0, 0], [0, z, 0]]
            projected_2d = matrix_multiplication(projection_matrix, rotated)

            x = int(projected_2d[0][0] * scale) + self.position.x
            y = int(projected_2d[1][0] * scale) + self.position.y
            ps.append((x, y))

        pygame.draw.polygon(screen, self.secondaryColor, ps)
        pygame.draw.polygon(screen, self.color, ps, self.stroke)
