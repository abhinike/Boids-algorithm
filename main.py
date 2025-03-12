import pygame
from boid import Boid
from tools import Vector
import math
import random
from matrix import *
from constants import *
from uiParameters import *
import matplotlib.pyplot as plt
import numpy as np
import threading

pygame.init()

window = pygame.display.set_mode(size)
clock = pygame.time.Clock()
fps = 60

scale = 40
Distance = 5
speed = 0.0005

flock = []
obstacles = []
n = 20

for i in range(n):
    flock.append(Boid(random.randint(20, Width - 20), random.randint(10, 400 - 10), highway1))

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

start_time = pygame.time.get_ticks()
plot_update_interval = 500
last_plot_update = 0

def plot_thread():
    plt.ion()
    fig, ax = plt.subplots()
    ax.set_title("Live Loss Plot")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Loss")
    avg_line, = ax.plot([], [], marker="o", linestyle="-", color="r", label="Avg Loss")
    front_line, = ax.plot([], [], marker="x", linestyle="-", color="b", label="Front Loss")
    ax.legend()

    time_values = []
    avg_loss_values = []
    front_loss_values = []

    while run:
        try:
            elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
            if len(flock) > 0:
                # Use getattr with default values to avoid AttributeError
                avg_loss = math.sqrt(sum(getattr(boid, 'loss', 0)**2 for boid in flock) / len(flock))
                avg_front_loss = math.sqrt(sum(getattr(boid, 'front_loss', 0)**2 for boid in flock) / len(flock))
            else:
                avg_loss = 0
                avg_front_loss = 0

            time_values.append(elapsed_time)
            avg_loss_values.append(avg_loss)
            front_loss_values.append(avg_front_loss)

            if len(time_values) > 100:
                time_values = time_values[-100:]
                avg_loss_values = avg_loss_values[-100:]
                front_loss_values = front_loss_values[-100:]

            avg_line.set_xdata(time_values)
            avg_line.set_ydata(avg_loss_values)
            front_line.set_xdata(time_values)
            front_line.set_ydata(front_loss_values)
            ax.relim()
            ax.autoscale_view()
            plt.draw()
            plt.pause(0.5)
        except Exception as e:
            print(f"Plot thread error: {e}")
            plt.pause(0.5)

    plt.ioff()
    plt.show()

plot_thread = threading.Thread(target=plot_thread)
plot_thread.start()

while run:
    clock.tick(fps)
    window.fill((10, 10, 15))

    highway1.render(screen=window)
    highway2.render(screen=window)

    n = numberInput.value
    scale = sliderScale.value

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            clicked = True
        if event.type == pygame.MOUSEBUTTONDOWN:
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

        try:
            if len(flock) > 0:
                avg_loss = math.sqrt(sum(getattr(boid, 'loss', 0)**2 for boid in flock) / len(flock))
                avg_front_loss = math.sqrt(sum(getattr(boid, 'front_loss', 0)**2 for boid in flock) / len(flock))
            else:
                avg_loss = 0
                avg_front_loss = 0

            AverageLossText.text = f"Avg Loss: {avg_loss:.2f} | Front Loss: {avg_front_loss:.2f}"
        except Exception as e:
            AverageLossText.text = f"Error calculating loss: {e}"

    else:
        UItoggle.Render(window)

    backSpace = False
    keyPressed = False
    pygame.display.flip()
    clicked = False

pygame.quit()
