import arcade
import random

# Configuración de la ventana
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "My Draw with Smoke"

class Smoke:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(5, 15)
        self.alpha = 255  # Opacidad

    def update(self):
        self.x -= random.uniform(2, 5)  # Movimiento horizontal inverso
        self.y += random.uniform(-1, 1)  # Movimiento vertical leve
        self.alpha -= 2  # Desvanece el humo más lentamente

    def draw(self):
        if self.alpha > 0:
            arcade.draw_circle_filled(self.x, self.y, self.size, arcade.color.GRAY + (self.alpha,))

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.AIR_SUPERIORITY_BLUE)
        self.smoke_particles = []
        self.road_lines = [i for i in range(10, 800, 110)]

    def on_draw(self):
        arcade.start_render()

        # Carretera
        arcade.draw_lrtb_rectangle_filled(0, 800, 250, 0, arcade.color.ARSENIC)
        for i in self.road_lines:
            arcade.draw_lrtb_rectangle_filled(i, i+80, 110, 90, arcade.color.BISQUE)

        # Coche
        arcade.draw_lrtb_rectangle_filled(200, 650, 300, 230, arcade.color.BOSTON_UNIVERSITY_RED)
        arcade.draw_lrtb_rectangle_filled(300, 500, 350, 230, arcade.color.BOSTON_UNIVERSITY_RED)
        arcade.draw_triangle_filled(230, 300, 300, 350, 300, 300, arcade.color.BOSTON_UNIVERSITY_RED)
        arcade.draw_triangle_filled(570, 300, 500, 350, 500, 300, arcade.color.BOSTON_UNIVERSITY_RED)

        # Detalles
        arcade.draw_circle_filled(650, 285, 10, arcade.color.DEEP_LEMON)
        arcade.draw_lrtb_rectangle_filled(650, 670, 300, 260, arcade.color.AIR_SUPERIORITY_BLUE)
        arcade.draw_lrtb_rectangle_filled(195, 655, 235, 230, arcade.color.BLACK)

        # Ruedas
        arcade.draw_circle_filled(270, 230, 30, arcade.color.BLACK)
        arcade.draw_circle_filled(270, 230, 20, arcade.color.DIRT)
        arcade.draw_circle_filled(530, 230, 30, arcade.color.BLACK)
        arcade.draw_circle_filled(530, 230, 20, arcade.color.DIRT)

        # Ventanas
        arcade.draw_triangle_filled(250, 300, 305, 340, 305, 300, arcade.color.DIAMOND)
        arcade.draw_triangle_filled(550, 300, 495, 340, 495, 300, arcade.color.DIAMOND)
        arcade.draw_lrtb_rectangle_filled(305, 390, 340, 300, arcade.color.DIAMOND)
        arcade.draw_lrtb_rectangle_filled(410, 495, 340, 300, arcade.color.DIAMOND)

        # Dibujar humo
        for smoke in self.smoke_particles:
            smoke.draw()

    def update(self, delta_time):
        # Generar nuevas partículas de humo desde la base de las ruedas
        if random.random() < 0.3:
            self.smoke_particles.append(Smoke(270, 220))
            self.smoke_particles.append(Smoke(530, 220))

        # Actualizar partículas de humo
        for smoke in self.smoke_particles:
            smoke.update()

        # Eliminar partículas que desaparecen más tarde
        self.smoke_particles = [s for s in self.smoke_particles if s.alpha > 0]

        # Mover líneas de la carretera más lentamente para mayor duración
        self.road_lines = [(i - 3) % 800 for i in self.road_lines]

if __name__ == "__main__":
    game = MyGame()
    arcade.run()