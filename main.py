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
highway_height = 400  # Total height of highway
lane_height = highway_height / 3  # Height of each lane
highway_top = (Height - highway_height) // 2  # Starting y position of highway

# Calculate the center y-coordinate for each lane
lane_1_y = highway_top + (lane_height / 2)  # Top lane center
lane_2_y = lane_1_y + lane_height          # Middle lane center
lane_3_y = lane_2_y + lane_height          # Bottom lane center

# Create boids in lanes
for i in range(n):
    # Randomly select a lane
    lane_y = random.choice([lane_1_y, lane_2_y, lane_3_y])
    
    # Add small random variation within the lane (optional)
    lane_variation = random.randint(-10, 10)  # ±10 pixels variation
    
    # Create boid with random x position but fixed lane y position
    flock.append(Boid(
        x=random.randint(20, Width-20),
        y=lane_y + lane_variation
    ))
 
ambulance = AmbulanceBoid(random.randint(20, Width - 20), random.randint(20, Height - 20))
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
