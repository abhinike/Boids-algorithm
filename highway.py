import random
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

    @abstractmethod
    def update_velocity(self, boid):
        """Abstract method to update velocity of highway"""
        pass

    @abstractmethod
    def on_road(self, point : tuple[float, float]) -> bool:
        """Abstract method to check whether the given point is within the boundary
            input -> point (x, y)
            output -> boolean
        """
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
            # boid.position.y = random.randint(0, 400)

        highway_top = 0
        highway_bottom = self.bottom_left_coordinate[1]

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

    def update_velocity(self, boid):
        # Increase the horizontal component
        boid.velocity.x = abs(boid.velocity.x) * 1.3 # Ensure positive horizontal direction
        boid.velocity*=boid.desired_speed
        # boid.velocity.normalize()

    def on_road(self, point: tuple[float, float]) -> bool:
        """Check if a point is within the rectangular boundary of the highway"""
        x, y = point
        return 0 <= x <= self.length and 0 <= y <= self.width







    


class Highway2(Highway):  # Angled Highway


    def __init__(self, screen_width, lanes=2, lane_width=100, dash_length=20, dash_gap=20):
        super().__init__(lanes, lane_width, dash_length, dash_gap)
        self.width = lanes * lane_width
        self.length = screen_width
        self.top_left_coordinate = (400, 400)
        self.top_right_coordinate = (600, 400)
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
        # if boid.y > self.top_left_coordinate[1]:
            #move the boid from highway2 to highway1
            # boid.highway = highway1



        """Keep boids within angled highway boundaries"""


        x, y = boid.position.x, boid.position.y

        # Calculate the y-values of the boundary lines for the given x
        left_boundary_y = self.get_boundary_y(self.bottom_left_coordinate, self.top_left_coordinate, x)
        right_boundary_y = self.get_boundary_y(self.bottom_right_coordinate, self.top_right_coordinate, x)

        # If the boid is outside the boundary, reposition it
        if y < left_boundary_y:
            boid.position.y = left_boundary_y
        elif y > right_boundary_y:
            boid.position.y = right_boundary_y

    def avoid_boundary(self, boid):
        # If the boid reaches the top of the angled highway (highway2), shift to highway1
        if boid.position.y < 400:
            highway1 = Highway1()
            boid.highway = highway1

        """Steer boids away from the angled highway boundaries"""
        x, y = boid.position.x, boid.position.y
        steering = Vector(0, 0)
        total = 0

        # Calculate the y-values of the boundaries at the boid's x-position
        left_boundary_y = self.get_boundary_y(self.bottom_left_coordinate, self.top_left_coordinate, x)
        right_boundary_y = self.get_boundary_y(self.bottom_right_coordinate, self.top_right_coordinate, x)

        # Get the perpendicular direction to the highway (normalized)
        road_direction = self.direction.Normalize()  # Assuming you store highway direction
        perpendicular = Vector(-road_direction.y, road_direction.x)  # Perpendicular vector

        # If the boid is too close to the left boundary, steer away
        if y - boid.radius < left_boundary_y:
            steering += perpendicular  # Push outward
            total += 1

        # If the boid is too close to the right boundary, steer away
        elif y + boid.radius > right_boundary_y:
            steering -= perpendicular  # Push inward
            total += 1

        return total, steering

    @staticmethod
    def get_boundary_y(point1, point2, x):
        """Helper function to get y-value of a boundary line for a given x"""
        x1, y1 = point1
        x2, y2 = point2
        if x1 == x2:  # Vertical line (shouldn't happen in a 45-degree highway)
            return y1
        slope = (y2 - y1) / (x2 - x1)
        intercept = y1 - slope * x1
        return slope * x + intercept

    def update_velocity(self, boid):
        # Ensure velocity is aligned with the highway direction
        highway_direction = self.direction.Normalize()  # Normalize highway direction vector

        # Project the boid's velocity onto the highway direction
        velocity_magnitude = boid.velocity.magnitude()  # Get current speed
        boid.velocity = highway_direction * velocity_magnitude * 1.5  # Increase speed along highway direction

        # boid.velocity.normalize()  # Normalize velocity to prevent excessive acceleration

    def on_road(self, point: tuple[float, float]) -> bool:
        """Check if a point is within the quadrilateral highway using area method"""
        x, y = point

        def triangle_area(p1, p2, p3):
            """Calculate the area of a triangle given three points"""
            x1, y1 = p1
            x2, y2 = p2
            x3, y3 = p3
            return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)

        # Compute the total quadrilateral area
        quad_area = (
                triangle_area(self.top_left_coordinate, self.bottom_left_coordinate, self.bottom_right_coordinate) +
                triangle_area(self.top_left_coordinate, self.bottom_right_coordinate, self.top_right_coordinate)
        )

        # Compute sum of areas of triangles formed by (point, three quadrilateral vertices)
        area1 = triangle_area(point, self.top_left_coordinate, self.bottom_left_coordinate)
        area2 = triangle_area(point, self.bottom_left_coordinate, self.bottom_right_coordinate)
        area3 = triangle_area(point, self.bottom_right_coordinate, self.top_right_coordinate)
        area4 = triangle_area(point, self.top_right_coordinate, self.top_left_coordinate)

        # If sum of small triangle areas equals quadrilateral area, point is inside
        return abs((area1 + area2 + area3 + area4) - quad_area) < 1e-5  # Tolerance for floating-point errors







