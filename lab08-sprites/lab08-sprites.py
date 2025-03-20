import arcade
import random

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Personalized Sprite Game"

PLAYER_SCALING = 0.3
GOOD_SCALING = 0.1
BAD_SCALING = 0.2

GOOD_SPRITE_COUNT = 10
BAD_SPRITE_COUNT = 10

MOVEMENT_SPEED = 5


class MyGame(arcade.Window):
    """Main game class."""

    def __init__(self):
        """Initializes the game window."""
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Sprite lists
        self.player_list = None
        self.good_sprite_list = None
        self.bad_sprite_list = None

        # Player
        self.player_sprite = None

        # Background texture
        self.background = None

        # Sound effects
        self.collect_good_sound = None
        self.collect_bad_sound = None

        # Score
        self.score = 0

        # Movement keys
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # Set background color (fallback)
        arcade.set_background_color(arcade.color.SKY_BLUE)

    def setup(self):
        """Set up the game and initialize variables."""

        # Load background image
        self.background = arcade.load_texture("images/background.png")

        # Initialize score
        self.score = 0

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.good_sprite_list = arcade.SpriteList()
        self.bad_sprite_list = arcade.SpriteList()

        # Set up player sprite
        self.player_sprite = arcade.Sprite("images/player.png", PLAYER_SCALING)
        self.player_sprite.center_x = SCREEN_WIDTH / 2
        self.player_sprite.center_y = SCREEN_HEIGHT / 2
        self.player_list.append(self.player_sprite)

        # Create good sprites
        for _ in range(GOOD_SPRITE_COUNT):
            good_sprite = arcade.Sprite("images/good_item.png", GOOD_SCALING)
            good_sprite.center_x = random.randint(20, SCREEN_WIDTH - 20)
            good_sprite.center_y = random.randint(20, SCREEN_HEIGHT - 20)
            # Give them random speed
            good_sprite.change_x = random.choice([-2, 2])
            good_sprite.change_y = random.choice([-2, 2])
            self.good_sprite_list.append(good_sprite)

        # Create bad sprites
        for _ in range(BAD_SPRITE_COUNT):
            bad_sprite = arcade.Sprite("images/bad_item.png", BAD_SCALING)
            bad_sprite.center_x = random.randint(20, SCREEN_WIDTH - 20)
            bad_sprite.center_y = random.randint(20, SCREEN_HEIGHT - 20)
            # Different random speed
            bad_sprite.change_x = random.choice([-3, 3])
            bad_sprite.change_y = random.choice([-3, 3])
            self.bad_sprite_list.append(bad_sprite)

    def on_draw(self):
        """Render the screen."""
        self.clear()

        # Draw background first
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        # Draw sprites
        self.good_sprite_list.draw()
        self.bad_sprite_list.draw()
        self.player_list.draw()

        # Draw score
        arcade.draw_text(f"Score: {self.score}", 10, 20, arcade.color.WHITE, 20)

    def on_update(self, delta_time):
        """Movement and game logic."""

        # Freeze the game if there are no more good sprites
        if len(self.good_sprite_list) == 0:
            return  # Skip updating if no good sprites are left

        # Move the player
        self.update_player_position()

        # Move the good sprites
        for good_sprite in self.good_sprite_list:
            good_sprite.center_x += good_sprite.change_x
            good_sprite.center_y += good_sprite.change_y

            # Bounce off the edges
            if good_sprite.left < 0 or good_sprite.right > SCREEN_WIDTH:
                good_sprite.change_x *= -1
            if good_sprite.bottom < 0 or good_sprite.top > SCREEN_HEIGHT:
                good_sprite.change_y *= -1

        # Move the bad sprites (different pattern - bounce faster)
        for bad_sprite in self.bad_sprite_list:
            bad_sprite.center_x += bad_sprite.change_x
            bad_sprite.center_y += bad_sprite.change_y

            if bad_sprite.left < 0 or bad_sprite.right > SCREEN_WIDTH:
                bad_sprite.change_x *= -1
            if bad_sprite.bottom < 0 or bad_sprite.top > SCREEN_HEIGHT:
                bad_sprite.change_y *= -1

        # Check for collisions with good sprites
        good_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.good_sprite_list)
        for good in good_hit_list:
            good.remove_from_sprite_lists()
            self.score += 1
            arcade.play_sound(self.collect_good_sound)

        # Check for collisions with bad sprites
        bad_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.bad_sprite_list)
        for bad in bad_hit_list:
            bad.remove_from_sprite_lists()
            self.score -= 1
            arcade.play_sound(self.collect_bad_sound)

    def update_player_position(self):
        """Update the player position based on keys pressed."""
        if self.up_pressed and not self.down_pressed:
            self.player_sprite.center_y += MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.center_y -= MOVEMENT_SPEED

        if self.left_pressed and not self.right_pressed:
            self.player_sprite.center_x -= MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.center_x += MOVEMENT_SPEED

        # Keep player inside screen bounds
        if self.player_sprite.left < 0:
            self.player_sprite.left = 0
        if self.player_sprite.right > SCREEN_WIDTH:
            self.player_sprite.right = SCREEN_WIDTH
        if self.player_sprite.bottom < 0:
            self.player_sprite.bottom = 0
        if self.player_sprite.top > SCREEN_HEIGHT:
            self.player_sprite.top = SCREEN_HEIGHT

    def on_key_press(self, key, modifiers):
        """Handle key presses."""
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        """Handle key releases."""
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

def main():
    """Main function"""
    game = MyGame()
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()