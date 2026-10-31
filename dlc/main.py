# Stub example game.

def main():
    Renderer = gamelib.Renderer
    with Renderer(1280, 720, "DLCbase Test") as game:

        player_x = 100
        player_y = 100
        speed_x = 0
        speed_y = 0
        
        while game.running:
            game.poll_events()

            if not game.running:
                break

            player_x += speed_x
            player_y -= speed_y
            speed_x = sum([speed_x * 4, 0]) / 5
            speed_y = sum([speed_y * 4, 0]) / 5

            if game.key_down("LEFT"):
                speed_x = sum([speed_x, -120]) / 9

            elif game.key_down("RIGHT"):
                speed_x = sum([speed_x, 120]) / 9

            if game.key_down("UP"):
                speed_y = sum([speed_y, 120]) / 9

            elif game.key_down("DOWN"):
                speed_y = sum([speed_y, -120]) / 9

            game.clear((25, 25, 35))

            game.draw_rect(
                player_x, player_y,
                64, 64,
                (255, 80, 80)
            )

            game.present()