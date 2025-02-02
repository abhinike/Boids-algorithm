from boid import Boid
import pygame
from tools import *
from random import uniform
import colorsys
from matrix import *
from math import pi, sin, cos
from constants import * 
class AmbulanceBoid(Boid):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.max_speed = 10  # Ambulance moves faster
        self.min_speed = 7   # Minimum speed for ambulance
        self.color = (255, 255, 255)  # Purple color for ambulance
        self.siren_radius = 200  # Radius within which other boids react

    def update(self):
        # Update position and velocity
        self.position = self.position + self.velocity
        self.velocity = self.velocity + self.acceleration
        
        # Ensure minimum speed
        current_speed = self.velocity.magnitude()
        if current_speed < self.min_speed:
            self.velocity.normalize()
            self.velocity = self.velocity * self.min_speed
            
        # Ensure maximum speed
        self.velocity.limit(self.max_speed)
        
        # Ensure primarily horizontal movement
        if self.velocity.x < 0:  # Always move right
            self.velocity.x = abs(self.velocity.x)
            
        # Add slight rightward bias
        self.velocity.x = self.velocity.x * 1.2
        
        # Update angle for rendering
        self.angle = self.velocity.heading() + pi / 2

        # Add flashing effect
        if pygame.time.get_ticks() % 500 < 250:
            self.color = (255, 0, 0)  # Red
        else:
            self.color = (255,255,255)  # white

    def behaviour(self, flock):
        self.acceleration.reset()
        
        # Only apply minimal separation to avoid collisions
        if self.toggles["separation"]:
            avoid = self.separation(flock)
            avoid = avoid * (self.values["separation"] * 0.05)  # Very minimal separation
            self.acceleration.add(avoid)
            
        # No alignment or cohesion - ambulance maintains its own path

    def activate_siren(self, flock):
        for boid in flock:
            if isinstance(boid, AmbulanceBoid):
                continue
            
            dist = getDistance(self.position, boid.position)
            if dist < self.siren_radius:
                # Calculate relative position
                avoidance_vector = SubVectors(boid.position, self.position)
                avoidance_vector.normalize()
                
                # Stronger avoidance force
                avoidance_vector = avoidance_vector * 3
                
                # Apply the avoidance force
                boid.velocity = boid.velocity + avoidance_vector
                
                # Slow down other boids more significantly
                boid.velocity.limit(boid.max_speed * 0.4)