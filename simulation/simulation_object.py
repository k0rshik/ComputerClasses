from abc import ABC, abstractmethod


class SimulationObject(ABC):
    @abstractmethod
    def tick(self) -> None:
        pass
