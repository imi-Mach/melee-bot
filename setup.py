from args import melee_parser

import melee

import signal
import sys


if __name__ == "__main__":
    args = melee_parser()

    log = None
    if args.debug:
        log = melee.Logger()
    
    console = melee.Console(path=args.dolphin_executable_path,
                        slippi_address=args.address,
                        logger=log)
    
    controller = melee.Controller(console=console,
                              port=args.port,
                              type=melee.ControllerType.STANDARD)
    
    controller_opponent = melee.Controller(console=console,
                                       port=args.opponent,
                                       type=melee.ControllerType.GCN_ADAPTER)
    
    def signal_handler(sig, frame):
        console.stop()
        if args.debug:
            log.writelog()
            print("") #because the ^C will be on the terminal
            print("Log file created: " + log.filename)
        print("Shutting down cleanly...")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    console.run(iso_path=args.iso)

    print("Connecting to console...")
    if not console.connect():
        print("ERROR: Failed to connect to the console.")
        sys.exit(-1)
    print("Console connected")

    print("Connecting controller to console...")
    if not controller.connect():
        print("ERROR: Failed to connect the controller.")
        sys.exit(-1)
    print("Controller connected")

    

    while True:
        gamestate = console.step()
        if gamestate is None:
            continue

        if console.processingtime * 1000 > 12:
            print("WARNING: Last frame took " + str(console.processingtime*1000) + "ms to process.")

        if gamestate.menu_state in [melee.Menu.IN_GAME, melee.Menu.SUDDEN_DEATH]:
            
            if gamestate.distance < 4:
                pass
                #controller.press_button(melee.Button.BUTTON_A)
                # controller.empty_input()
                # melee.techskill.multishine(ai_state=gamestate.players[args.port], controller=controller)
            else:
                onleft = gamestate.player[args.opponent].x > gamestate.players[args.port].x
                controller.tilt_analog(melee.Button.BUTTON_MAIN, int(onleft), 0.5)
                controller.release_button(melee.Button.BUTTON_A)

                if gamestate.player[args.opponent].y > gamestate.players[args.port].y:
                    controller.press_button(melee.Button.BUTTON_X)
                else:
                    controller.release_button(melee.Button.BUTTON_X)

            if log:
                log.logframe(gamestate)
                log.writeframe()
        else:
            melee.MenuHelper.menu_helper_simple(gamestate,
                                                controller,
                                                melee.Character.FOX,
                                                melee.Stage.YOSHIS_STORY,
                                                args.connect_code,
                                                autostart=True,
                                                swag=False)
            if log:
                log.skipframe()