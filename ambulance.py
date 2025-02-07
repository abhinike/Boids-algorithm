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
        self.max_speed = 5
        self.min_speed = 7
        self.color = (143, 85, 172)
        self.siren_radius = 150  # Increased radius to detect boids earlier
        self.warning_radius = 200  # Radius within which other boids react

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

    def find_best_lane(self, boid, flock, highway_height, screen_height):
        lane_height = highway_height / 3
        highway_top = (screen_height - highway_height) // 2
        
        lane_1_y = highway_top + (lane_height / 2)  
        lane_2_y = lane_1_y + lane_height          
        lane_3_y = lane_2_y + lane_height          
        
        lanes = [lane_1_y, lane_2_y, lane_3_y]
        
        # Check current lane
        current_lane = min(lanes, key=lambda lane: abs(lane - boid.position.y))
        
        # Check occupied lanes
        occupied_lanes = set()
        safety_radius = 50  # Space check for occupied lanes
        
        for other_boid in flock:
            if other_boid != boid and not isinstance(other_boid, AmbulanceBoid):
                for lane_y in lanes:
                    if abs(other_boid.position.y - lane_y) < safety_radius:
                        occupied_lanes.add(lane_y)
        
        # Filter only unoccupied lanes
        available_lanes = [lane for lane in lanes if lane not in occupied_lanes]

        if available_lanes:
            return min(available_lanes, key=lambda lane: abs(lane - current_lane))
        else:
            return current_lane  # Stay in current lane if no open lane found


    def activate_siren(self, flock):
        highway_height = 400  # Total height of highway
        
        for boid in flock:
            if isinstance(boid, AmbulanceBoid):
                continue  # Ignore itself
            
            dist = getDistance(self.position, boid.position)
            
            # If within warning radius, start lane switching preparation
            if dist < self.warning_radius:
                target_lane_y = self.find_best_lane(boid, flock, highway_height, Height)

                # Smooth movement to new lane
                if abs(boid.position.y - target_lane_y) > 1:
                    move_direction = 1 if target_lane_y > boid.position.y else -1
                    move_speed = min(2.0, 5.0 * (self.warning_radius - dist) / self.warning_radius)
                    boid.position.y += move_direction * move_speed
                
                # Slow down slightly while changing lanes
                if dist < self.siren_radius:
                    slow_factor = 0.4 + (0.3 * (dist / self.siren_radius))
                    boid.velocity.limit(boid.max_speed * slow_factor)

                    # Additional horizontal avoidance if very close
                    if dist < self.siren_radius * 0.5:
                        avoidance_vector = SubVectors(boid.position, self.position)
                        avoidance_vector.normalize()
                        avoidance_vector = avoidance_vector * 2
                        boid.velocity = boid.velocity + avoidance_vector 
                        
                        
