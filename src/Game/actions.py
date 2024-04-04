# should align closely to specific characters

# while I can make 1 class to read character 
# data file (for frame data), looks like bots 
# will need some harcode specific logic for stategies off stage.

class actions():
    def __init__(self) -> None:
        # create object for queue (when actions require several frames)
        self.move_buffer = []
        pass

    # here is where we check additional logic
    # e.g. if the agent is off screen, clear move buffer and hard code recovery.
    def _strategy(self) -> None:
        pass
