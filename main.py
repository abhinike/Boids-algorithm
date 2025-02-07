import pygame
from boid import Boid
from tools import Vector
import math
import random
from matrix import *
from constants import *
from uiParameters import *
from ambulance import AmbulanceBoid

pygame.init()
window = pygame.display.set_mode((400, 900), pygame.FULLSCREEN)

# size = (800, 600)  # Example dimensions for a smaller window

window = pygame.display.set_mode(size)  # No FULLSCREEN flag

clock = pygame.time.Clock()
fps = 60

scale = 40
Distance = 5
speed = 0.0005

flock = []
#number of boids
n = 20
#radius of perception of each boid

# Calculate lane positions
highway_height = 400
lane_height = highway_height / 3
highway_top = (Height - highway_height) // 2
# middle_lane_y = highway_top + lane_height + (lane_height / 2)  # Starting y position of highway

# Calculate the center y-coordinate for each lane
lane_1_y = highway_top + (lane_height / 2)  # Top lane center
lane_2_y = lane_1_y + lane_height  - 120        # Middle lane center
lane_3_y = lane_2_y + lane_height          # Bottom lane center

lanes = [lane_1_y, lane_2_y, lane_3_y]  # Fixed lane options

for i in range(n):
    lane_y = lanes[i % 3]  # Assign lanes in a repeating pattern (1 → 2 → 3 → 1 ...)
    lane_variation = random.randint(-5, 5)  # Small variation within lane (optional)
    
    flock.append(Boid(
        x=random.randint(50, Width - 50),  # Random X, but always in a lane
        y=lane_y + lane_variation
    ))

# Place the ambulance in the middle lane
ambulance = AmbulanceBoid(
    x=random.randint(50, Width - 50),
    y=lane_2_y
)
flock.append(ambulance)
 

textI = "10"
reset = False
SpaceButtonPressed = False
backSpace = False
keyPressed = False
showUI = False
clicked = False
run = True
while run:
	clock.tick(fps)
	window.fill((10, 10, 15))
 
	#render highway
	highway.render(screen=window)
	

	n = numberInput.value
	scale = sliderScale.value

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONUP:
			clicked = True
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				run = False
			if event.key == pygame.K_r:
				reset = True
			if event.key == pygame.K_SPACE:
				SpaceButtonPressed = True

			textI = pygame.key.name(event.key)
			keyPressed = True

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_BACKSPACE:
				backSpace = True
			if event.key == pygame.K_u:
				showUI = not showUI

	if reset == True or resetButton.state == True:
		flock = []
		for i in range(n):
			flock.append(Boid(random.randint(20, Width-20), random.randint(20, Height-20)))
		reset = False

	
	for boid in flock:
		if isinstance(boid, AmbulanceBoid):
			boid.activate_siren(flock)  # Activate siren effect for ambulance boid

		# Update boid properties and behavior
		boid.toggles = {
			"separation": toggleSeparation.state,
			"alignment": toggleAlignment.state,
			"cohesion": toggleCohesion.state
		}
		boid.values = {
			"separation": separationInput.value / 100,
			"alignment": alignmentInput.value / 100,
			"cohesion": cohesionInput.value / 100
		}
		boid.radius = scale
		boid.limits(Width, Height, 400)
		boid.behaviour(flock)
		boid.update()
		boid.hue += speed
		boid.Draw(window, Distance, scale)




	if showUI == True:
		panel.Render(window)

		resetButton.Render(window)
		Behaviours.Render(window)
		Separation.Render(window)
		Alignment.Render(window)
		Cohesion.Render(window)
		SeparationValue.Render(window)
		AlignmentValue.Render(window)
		CohesionValue.Render(window)
		NumberOfBoids.Render(window)
		ScaleText.Render(window)
		toggleSeparation.Render(window, clicked)
		toggleAlignment.Render(window, clicked)
		toggleCohesion.Render(window, clicked)
		separationInput.Render(window, textI, backSpace, keyPressed)
		alignmentInput.Render(window, textI, backSpace, keyPressed)
		cohesionInput.Render(window, textI, backSpace, keyPressed)
		numberInput.Render(window, textI, backSpace, keyPressed)

		sliderScale.Render(window)

	else:
		UItoggle.Render(window)
	backSpace = False
	keyPressed = False
	pygame.display.flip()
	clicked = False
pygame.quit()
