import pygame
import engine
import input
import title
import level
import os


def run():
    window = engine.Engine("Oasis")
    ihandler = input.Input(["LEFT CLICK", "PLAYER LEFT", "PLAYER RIGHT", "PLAYER UP", "PLAYER DOWN", "SPELLCAST"])
    ihandler.map_key("M1", "LEFT CLICK")
    ihandler.map_key(pygame.K_w, "PLAYER UP")
    ihandler.map_key(pygame.K_a, "PLAYER LEFT")
    ihandler.map_key(pygame.K_s, "PLAYER DOWN")
    ihandler.map_key(pygame.K_d, "PLAYER RIGHT")
    ihandler.map_key(pygame.K_SPACE, "SPELLCAST")
    state_objects = [title.Title(), level.Level()]
    gamestate = 0
    running = True

    while running:
        window.tick()
        ihandler.clear_input_queue()
        ihandler.plug_events()
        gamestate = state_objects[gamestate].input_output(ihandler.queue, ihandler.states, ihandler.mouse_x, ihandler.mouse_y)
        running = (not ihandler.user_exits) and gamestate != -1
        if not running:
            break
        update(window.delta, state_objects[gamestate])
        render(window, state_objects[gamestate])

    window.quit()


def update(delta, state_object):
    state_object.update(delta)


def render(window, state_object):
    window.clear_screen()

    state_object.render(window)

    window.render_fps()
    window.flip_buffer()


os.environ['SDL_VIDEO_CENTERED'] = '1'
run()
