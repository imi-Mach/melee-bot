import melee

def entry(console: melee.Console, controller: melee.Controller, ai_port, opponent_port, log: melee.Logger=None):
    while True:
        gamestate = console.step()
        if gamestate is None:
            continue

        if console.processingtime * 1000 > 12:
            print("WARNING: Last frame took " + str(console.processingtime*1000) + "ms to process.")

        if gamestate.menu_state in [melee.Menu.IN_GAME, melee.Menu.SUDDEN_DEATH]:
            
            # in game

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