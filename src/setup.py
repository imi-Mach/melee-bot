from args import melee_parser

import Game.play

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
        
        if args.debug:
            log.writelog()
            print("") #because the ^C will be on the terminal
            print("Log file created: " + log.filename)
        print("Shutting down cleanly...")
        console.stop()
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

    
    Game.play.entry(console,controller,args.port, args.opponent, log)