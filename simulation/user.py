import random
from simulation.simulation_object import SimulationObject


class User(SimulationObject):
    __work_time: int
    __need_gis: bool
    __need_dbms: bool

    __station_attempts: int = 0
    __room_attempts: int = 0

    def __init__(self, simulation, minimal_resolution, need_gis: bool,
                 need_dbms: bool,
                 work_time: int):
        self.__simulation = simulation
        self.__need_dbms = need_dbms
        self.__need_gis = need_gis
        self.__minimal_resolution = minimal_resolution
        self.__work_time = work_time

        self.__current_room = None
        self.__current_station = None

    def __check_station(self) -> bool:
        if self.__current_station is None:
            return False
        return (not self.__current_station.is_broken and
                (not self.__need_gis or self.__current_station.have_gis) and
                (not self.__need_dbms or self.__current_station.have_dbms))

    def tick(self) -> None:
        if self.__work_time <= 0:
            self.remove(True)
            return
        if self.__room_attempts > 3:
            self.remove()
            return

        if self.__current_room is None:
            if len(self.__simulation.computer_rooms) > 0:
                self.__current_room = random.choice(self.__simulation.computer_rooms)
                self.__station_attempts = 0
            self.__room_attempts += 1
            return

        if self.__current_station is None:

            stations = list(filter(lambda
                                       s: s.display_resolution.value >= self.__minimal_resolution.value and not s.occupied and not s.is_broken,
                                   self.__current_room.stations))

            if len(stations) > 0:
                self.set_station(random.choice(stations))

            self.__station_attempts += 1
            if self.__station_attempts > 3:
                self.__station_attempts = 0
                self.__current_room = None

            return

        if not self.__check_station():
            self.remove_station(self.__current_station)
            return

        self.__work_time -= 1

    @property
    def work_time(self) -> int:
        return self.__work_time

    @property
    def need_gis(self) -> bool:
        return self.__need_gis

    @property
    def need_dbms(self) -> bool:
        return self.__need_dbms

    @property
    def have_station(self) -> bool:
        return self.__current_station is not None

    @property
    def have_room(self) -> bool:
        return self.__current_room is not None

    def remove(self, successful=False) -> None:
        if self.__current_station is not None:
            self.__current_station.remove_user(self)
        self.__simulation.remove_user(self, successful)

    # User -- Station
    def set_station(self, station) -> None:
        if self.__current_station is station:
            return
        if self.__current_station is not None:
            self.remove_station(self.__current_station)

        self.__current_station = station
        self.__current_station.set_user(self)

    def remove_station(self, station) -> None:
        if self.__current_station is station:
            self.__current_station = None
            station.remove_user(self)
