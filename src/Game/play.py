import melee
from melee import enums


def multishine(ai_state, controller):
    """ Frame-perfect Multishines as Fox """
    #If standing, shine
    if ai_state.action == enums.Action.STANDING:
        controller.press_button(enums.Button.BUTTON_B)
        controller.tilt_analog(enums.Button.BUTTON_MAIN, .5, 0)
        return

    #Shine on frame 3 of knee bend, else nothing
    if ai_state.action == enums.Action.KNEE_BEND:
        if ai_state.action_frame == 1:
            controller.press_button(enums.Button.BUTTON_B)
            controller.tilt_analog(enums.Button.BUTTON_MAIN, .5, 0)
            return
        controller.release_all()
        return

    shine_start = (ai_state.action == enums.Action.DOWN_B_STUN or
                   ai_state.action == enums.Action.DOWN_B_GROUND_START)

    #Jump out of shine
    if shine_start and ai_state.action_frame >= 4 and ai_state.on_ground:
        controller.press_button(enums.Button.BUTTON_Y)
        return

    if ai_state.action == enums.Action.DOWN_B_GROUND:
        controller.press_button(enums.Button.BUTTON_Y)
        return

    controller.release_all()

def entry(console: melee.Console, controller: melee.Controller, ai_port, opponent_port, log: melee.Logger=None):
    while True:
        gamestate = console.step()
        if gamestate is None:
            continue

        # if console.processingtime * 1000 > 12:
        #     print("WARNING: Last frame took " + str(console.processingtime*1000) + "ms to process.")

        if gamestate.menu_state in [melee.Menu.IN_GAME, melee.Menu.SUDDEN_DEATH]:
            
            # in game
            multishine(gamestate.players[ai_port], controller)

            if log:
                log.logframe(gamestate)
                log.writeframe()
        else:
            melee.MenuHelper.menu_helper_simple(gamestate,
                                                controller,
                                                melee.Character.FOX,
                                                melee.Stage.YOSHIS_STORY,
                                                "", # connect code
                                                autostart=True,
                                                swag=False)
            if log:
                log.skipframe()