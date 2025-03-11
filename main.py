import pygame
from boid import Boid
from tools import Vector
import math
import random
from matrix import *
from constants import *
from uiParameters import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation

pygame.init()
window = pygame.display.set_mode((400, 900), pygame.FULLSCREEN)

# size = (800, 600)  # Example dimensions for a smaller window
window = pygame.display.set_mode(size)

clock = pygame.time.Clock()
fps = 60

scale = 40
Distance = 5
speed = 0.0005

flock = []
obstacles = []
# Number of cars
n = 20

# Radius of perception of each boid
for i in range(n):
    flock.append(Boid(random.randint(20, Width - 20), random.randint(10, 400 - 10), highway1))

# Testing highway2
flock.append(Boid(100, Height, highway2))
flock.append(Boid(220, Height - 100, highway2))

textI = "10"
reset = False
SpaceButtonPressed = False
backSpace = False
keyPressed = False
showUI = False
clicked = False
run = True

# Matplotlib setup
loss_values = []
time_values = []
fig, ax = plt.subplots()
ax.set_title("Live Loss Plot")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Average Loss")

def update_graph(i):
    """Update the Matplotlib plot with new loss values."""
    ax.clear()
    ax.set_title("Live Loss Plot")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Average Loss")
    if time_values:
        ax.plot(time_values, loss_values, marker="o", linestyle="-", color="r")

ani = animation.FuncAnimation(fig, update_graph, interval=500, cache_frame_data=False)
plt.ion()  # Interactive mode ON
plt.show()

start_time = pygame.time.get_ticks()  # Track simulation time

while run:
    clock.tick(fps)
    window.fill((10, 10, 15))

    # Render highway
    highway1.render(screen=window)
    highway2.render(screen=window)

    n = numberInput.value
    scale = sliderScale.value

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            clicked = True
        if event.type == pygame.MOUSEBUTTONDOWN:  # Detect tap
            x, y = event.pos
            if highway1.on_road((x, y)):
                flock.append(Boid(x, y, highway1))
            if highway2.on_road((x, y)):
                flock.append(Boid(x, y, highway2))

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

    if reset or resetButton.state:
        flock = [Boid(random.randint(20, Width - 20), random.randint(20, Height - 20), highway1) for _ in range(n)]
        reset = False

    for boid in flock:
        boid.toggles = {"separation": toggleSeparation.state, "alignment": toggleAlignment.state, "cohesion": toggleCohesion.state}
        boid.values = {"separation": separationInput.value / 100, "alignment": alignmentInput.value / 100, "cohesion": cohesionInput.value / 100}
        boid.radius = scale
        boid.limits()
        boid.behaviour(flock)
        boid.update(flock, obstacles)
        boid.hue += speed
        boid.Draw(window, Distance, scale)

    if showUI:
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

        AverageLossText.Render(window)
        # Calculate average loss
        if len(flock) > 0:
            avg_loss = math.sqrt(sum(boid.loss**2 for boid in flock) / len(flock))
        else:
            avg_loss = 0

        # Update loss text
        AverageLossText.text = f"Avg Loss: {avg_loss:.2f}"

        # Update Matplotlib data
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # Convert to seconds
        time_values.append(elapsed_time)
        loss_values.append(avg_loss)

    else:
        UItoggle.Render(window)

    backSpace = False
    keyPressed = False
    pygame.display.flip()
    clicked = False

pygame.quit()
plt.ioff()
plt.show()
