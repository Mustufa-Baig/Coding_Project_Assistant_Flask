
import pygame
import random
import math

WIDTH = 800
HEIGHT = 600
NUM_PARTICLES = 50
MIN_RADIUS = 5
MAX_RADIUS = 20

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class Particle:
    def __init__(self):
        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(0, HEIGHT)
        self.vx = random.uniform(-5, 5)
        self.vy = random.uniform(-5, 5)
        self.radius = random.randint(MIN_RADIUS, MAX_RADIUS)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

    def check_boundary(self):
        if self.x - self.radius < 0:
            self.x = self.radius
            self.vx *= -1
        if self.x + self.radius > WIDTH:
            self.x = WIDTH - self.radius
            self.vx *= -1
        if self.y - self.radius < 0:
            self.y = self.radius
            self.vy *= -1
        if self.y + self.radius > HEIGHT:
            self.y = HEIGHT - self.radius
            self.vy *= -1

particles = [Particle() for _ in range(NUM_PARTICLES)]
running = True

while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for p in particles:
        p.update(dt)

    for p in particles:
        p.check_boundary()

    for i in range(len(particles)):
        for j in range(i + 1, len(particles)):
            p1 = particles[i]
            p2 = particles[j]
            dx = p2.x - p1.x
            dy = p2.y - p1.y
            dist_sq = dx * dx + dy * dy
            min_dist = p1.radius + p2.radius
            if dist_sq < min_dist * min_dist:
                if dist_sq == 0:
                    # Avoid division by zero by separating particles
                    p1.x -= 1.0
                    p2.x += 1.0
                    continue
                distance = math.sqrt(dist_sq)
                overlap = min_dist - distance
                dx_normalized = dx / distance
                dy_normalized = dy / distance
                p1.x -= dx_normalized * (overlap / 2)
                p1.y -= dy_normalized * (overlap / 2)
                p2.x += dx_normalized * (overlap / 2)
                p2.y += dy_normalized * (overlap / 2)
                p1.vx, p2.vx = p2.vx, p1.vx
                p1.vy, p2.vy = p2.vy, p1.vy

    screen.fill((0, 0, 0))
    for p in particles:
        pygame.draw.circle(screen, p.color, (int(p.x), int(p.y)), p.radius)
    pygame.display.flip()

pygame.quit()
exit()

