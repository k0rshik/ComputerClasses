from abc import ABC, abstractmethod
from simulation.simulation_object import SimulationObject
import random
import enum


class Resolution(enum.Enum):
    HD = "1280x720"
    FullHD = "1920x1080"
    UltraHD = "3840x2160"


class Computer(SimulationObject, ABC):
    _fix_time: int
    __crash_probability: float
    __broken: bool

    @abstractmethod
    def __init__(self, crash_probability: float):
        self.__crash_probability = crash_probability
        self.__broken = False
        self._fix_time = 0

    @abstractmethod
    def tick(self) -> None:
        if self.__broken:
            if self._fix_time >= 0:
                self._fix_time -= 1

            if self._fix_time == 0:
                self.__broken = False
        elif not self.__broken and random.random() < self.__crash_probability:
            self.__broken = True

    def fix(self, time: int = 0) -> None:
        if time <= 0:
            self.__broken = False
            self._fix_time = -1
        else:
            self._fix_time = time

    @property
    def is_broken(self) -> bool:
        return self.__broken

    @property
    def chash_probability(self) -> float:
        return self.__crash_probability


class Server(Computer):
    __crush_protect_used: bool
    __have_crush_protect: bool
    __have_dbms: bool
    __have_gis: bool

    def __init__(self, __crash_probability: float, have_gis: bool, have_dbms: bool, have_crush_protect: bool):
        super().__init__(__crash_probability)
        self.__have_gis = have_gis
        self.__have_dbms = have_dbms
        self.__have_crush_protect = have_crush_protect
        self.__crush_protect_used = False

    def tick(self) -> None:
        super().tick()
        if self.is_broken and self.__have_crush_protect and not self.__crush_protect_used:
            super().fix()
            self.__crush_protect_used = True



    @property
    def have_gis(self) -> bool:
        return self.__have_gis

    @property
    def have_dbms(self) -> bool:
        return self.__have_dbms

    @property
    def have_crush_protect(self) -> bool:
        return self.__have_crush_protect

    @property
    def crush_protect_used(self) -> bool:
        return self.__crush_protect_used

class Station(Computer):
    __display_resolution: Resolution

    def __init__(self, crash_probability: float, display_resolution: Resolution,
                 computer_room):
        super().__init__(crash_probability)
        self.__display_resolution = display_resolution
        self.__computer_room = computer_room
        computer_room.add_station(self)

        self.__user = None

    def tick(self) -> None:
        super().tick()

    @property
    def occupied(self) -> bool:
        return self.__user is not None

    @property
    def display_resolution(self) -> Resolution:
        return self.__display_resolution

    @property
    def have_gis(self) -> bool:
        return self.__computer_room.have_gis

    @property
    def have_dbms(self) -> bool:
        return self.__computer_room.have_dbms

    @property
    def user(self):
        return self.__user

    # Station -- ComputerRoom
    def set_computer_room(self, room) -> None:
        if self.__computer_room is room:
            return
        if self.__computer_room is not None:
            self.__computer_room.remove_station(self)

        self.__computer_room = room
        self.__computer_room.add_station(self)

    def remove_computer_room(self, room) -> None:
        if room is self.__computer_room:
            self.__computer_room.remove_station(self)
            self.__computer_room = None

    # Station -- User
    def set_user(self, user):
        if self.__user is user:
            return
        if self.__user is not None:
            user.remove_station(self)

        self.__user = user
        self.__user.set_station(self)

    def remove_user(self, user):
        if self.__user is user:
            self.__user = None
            user.remove_station(self)

