from abc import (ABC, abstractmethod)

class Agent(ABC):
    
    @abstractmethod
    def act(state, reward):
        pass