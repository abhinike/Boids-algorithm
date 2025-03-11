import pygame
from highway import Highway
from tools import *
from random import uniform
import colorsys
from matrix import *
from math import pi, sin, cos
from constants import *

import math

# def hsvToRGB(h, s, v):
#     return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))

class Boid:
    def __init__(self, x, y, highway: Highway):
        self.position = Vector(x, y)
        vec_x = uniform(0.5, 1)
        vec_y = uniform(0, 0.5)
        self.velocity = Vector(vec_x, vec_y)
        # self.velocity.normalize()
        # Set a random magnitude
        self.velocity = self.velocity * uniform(1.5, 4)
        self.acceleration = Vector()
        self.color = (255, 255, 255)
        self.temp = self.color
        self.secondaryColor = (70, 70, 70)
        self.max_speed = 3
        self.max_length = 1
        self.size = 2
        self.stroke = 5
        self.angle = 0
        self.hue = 0
        self.toggles = {"separation": True, "alignment": True, "cohesion": True}
        self.values = {"separation": 0.1, "alignment": 0.1, "cohesion": 0.1}
        self.radius = 500
        self.desired_speed = self.max_speed # Initialize desired speed
        self.highway = highway
        self.speed = uniform(1.5 , 4)

    def behaviour(self, flock):
        # self.acceleration.reset()
        # self.acceleration.add(self.separation(flock) * 0.05)  # Reduced from 0.1 to 0.05
        # self.acceleration.add(self.cohesion(flock) * 0.05)  # Reduced from 0.1 to 0.05
        # self.acceleration.add(self.alignment(self) * 0.05)  # Reduced from 0.1 to 0.05

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

    def limits(self):
       


        self.highway.limits(self)

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

        total_from_highway_boundary , steering_from_highway_boundary  = self.highway.avoid_boundary(self)
        total+=total_from_highway_boundary
        steering.add(steering_from_highway_boundary)

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

    def adjust_speed(self, flock, look_ahead_distance=150, slow_factor=0.8):
        """Adjust speed based on nearby boids in front."""
        boids_ahead = 0
        closest_boid_distance = look_ahead_distance  # Initialize to max look ahead distance

        for mate in flock:
            if mate is not self:
                to_mate = SubVectors(mate.position, self.position)
                distance_to_mate = to_mate.magnitude()

                # Check if mate is within look ahead distance
                if distance_to_mate < look_ahead_distance:
                    forward_direction = self.velocity.Normalize()
                    angle_to_mate = angle_between_vectors(forward_direction, to_mate)

                    # Consider "ahead" if angle is small (e.g., within 45 degrees on either side)
                    if angle_to_mate < pi / 4 : # 45 degrees in radians
                        boids_ahead += 1
                        closest_boid_distance = min(closest_boid_distance, distance_to_mate)

        if boids_ahead > 0:
            # Reduce desired speed if boids ahead, more reduction if closer
            # Example: Reduce speed proportionally to how much of look_ahead_distance is remaining
            speed_reduction_factor = (closest_boid_distance / look_ahead_distance)
            self.desired_speed = self.max_speed * speed_reduction_factor * slow_factor # slow_factor to control intensity
            self.desired_speed = max(1, self.desired_speed) # Minimum speed to avoid complete stop
        else:
            # Speed up to max speed if no boids ahead
            self.desired_speed = self.max_speed


    def update(self, flock, obstacles):
        self.loss = self.calculate_loss(flock, obstacles)  # Store loss for display

        
        self.highway.update_velocity(self)

        self.adjust_speed(flock) # Adjust speed based on surroundings

        # Move towards desired speed
        speed_difference = self.desired_speed - self.velocity.magnitude()
        speed_adjust_accel = self.velocity.Normalize() * speed_difference * 0.1 # 0.1 is dampening factor for speed change
        self.acceleration.add(speed_adjust_accel)


        self.position = self.position + self.velocity
        self.velocity += self.acceleration * 0.5  # Reduce impact of acceleration
        self.velocity.limit(self.max_speed) # Still limit by max_speed for overall control
        self.angle = self.velocity.heading() + pi / 2
        self.acceleration.reset() # Reset acceleration after applying it


    def calculate_loss(self, flock, obstacles, alpha=1, beta=1, gamma=5, delta=1, d_safe=10):
        loss = 0
        penalty = 0
        epsilon = 1e-6  # Small value to prevent log(0)
        scale_factor = 1000  # Scaling before log



        for mate in flock:
            if mate is not self:
                dij = getDistance(self.position, mate.position)
                if dij > 0:
                    # Exponential inverse distance penalty
                    loss += alpha * math.exp(-dij / d_safe)

                    # Stronger penalty when too close
                    if dij < d_safe:
                        penalty += gamma * math.exp(-dij / d_safe)

        nearest_obstacle_dist = min(
            [getDistance(self.position, obs.position) for obs in obstacles] or [float('inf')]
        )
        if nearest_obstacle_dist > 0:
            loss += beta * math.exp(-nearest_obstacle_dist / d_safe)

        # Add penalties
        loss += penalty

        # Apply log scaling for visibility
        scaled_loss = math.log1p(loss * scale_factor) * 10  # log(1 + x) avoids log(0)

        return max(0, min(scaled_loss, 100))  # Clamp between 0-100

    def calculate_loss_front(self, flock, obstacles, alpha=1, beta=1, gamma=5, delta=1, d_safe=10):
        loss = 0
        penalty = 0
        epsilon = 1e-6  # Small value to prevent log(0)
        scale_factor = 1000  # Scaling before log

        # filterflock for boids that are ahead only
        flock_ahead = [mate for mate in flock if mate is not self and mate.position[0] > self.position[0]]


        for mate in flock_ahead:
            if mate is not self:
                dij = getDistance(self.position, mate.position)
                if dij > 0:
                    # Exponential inverse distance penalty
                    loss += alpha * math.exp(-dij / d_safe)

                    # Stronger penalty when too close
                    if dij < d_safe:
                        penalty += gamma * math.exp(-dij / d_safe)

        nearest_obstacle_dist = min(
            [getDistance(self.position, obs.position) for obs in obstacles] or [float('inf')]
        )
        if nearest_obstacle_dist > 0:
            loss += beta * math.exp(-nearest_obstacle_dist / d_safe)

        # Add penalties
        loss += penalty

        # Apply log scaling for visibility
        scaled_loss = math.log1p(loss * scale_factor) * 10  # log(1 + x) avoids log(0)

        return max(0, min(scaled_loss, 100))  # Clamp between 0-100


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

        # Display loss value
        font = pygame.font.Font(None, 20)
        loss_text = font.render(f"{self.loss:.2f}", True, (255, 0, 0))
        screen.blit(loss_text, (self.position.x + 5, self.position.y - 10))