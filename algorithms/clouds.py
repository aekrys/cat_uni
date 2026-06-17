import random
from images import load_image


class Cloud:
    def __init__(self, x, y, speed, size, path):
        self.image = load_image(path, (size, size))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


def create_clouds(screen_width, cloud_images):
    clouds = []
    for _ in range(7):
        x = random.randint(0, screen_width)
        y = random.randint(50, 450)
        speed = random.uniform(0.5, 2)
        size = random.randint(80, 200)
        image = random.choice(cloud_images)
        clouds.append(Cloud(x, y, speed, size, image))
    return clouds


def update_clouds(clouds, screen_width, cloud_images):
    for cloud in clouds:
        cloud.update()

        if cloud.rect.right < 0:
            x  = screen_width + random.randint(0, 200)
            y = random.randint(50, 450)
            speed = random.uniform(0.5, 2)
            size = random.randint(80, 200)
            image = random.choice(cloud_images)

            cloud.image = load_image(image, (size, size))
            cloud.size = size
            cloud.rect.x = x
            cloud.rect.y = y

            cloud.speed = speed
