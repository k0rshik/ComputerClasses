import random

from simulation.computer_room import ComputerRoom
from simulation.computers import Server, Station, Resolution
from simulation.user import User


def chance(probability=0.5):
    return random.random() < probability


class Simulation:
    __users: list[User]
    __servers: list[Server]
    __stations: list[Station]
    __rooms: list[ComputerRoom]

    # simulation settings
    # user
    user_spawn_prob: float = 1 / 20
    user_need_gis_prob: float = 1 / 5
    user_need_dbms_prob: float = 1 / 5
    user_min_worktime: int = 20
    user_max_worktime: int = 200
    # computer
    comp_min_fix_time = 10
    comp_max_fix_time = 60
    station_replace_prob = 1 / 200
    server_replace_prob = 1 / 2000

    def __init__(self):
        self.__users = []
        self.__servers = []
        self.__stations = []
        self.__rooms = []

        self.__all_time_users = 0
        self.__successful_users = 0

    @property
    def users_count(self):
        return self.__all_time_users

    @property
    def success_users_count(self):
        return self.__successful_users

    def add_server(self, server: Server) -> None:
        if server not in self.__servers:
            self.__servers.append(server)

    def create_room(self, servers: list[Server] = None) -> ComputerRoom:
        room = ComputerRoom(servers.copy())
        self.__rooms.append(room)
        return room

    def add_station(self, station: Station) -> None:
        if station not in self.__stations:
            self.__stations.append(station)

    def add_user(self, user: User):
        if user not in self.__users:
            self.__users.append(user)

    @property
    def computer_rooms(self) -> list[ComputerRoom]:
        return self.__rooms

    def remove_user(self, user: User, successful=False):
        if successful:
            self.__successful_users += 1
        self.__users.remove(user)

    @property
    def broken_stations(self) -> list[Station]:
        return list(filter(lambda s: s.is_broken, self.__stations))

    @property
    def broken_servers(self) -> list[Server]:
        return list(filter(lambda s: s.is_broken, self.__servers))

    @property
    def free_stations(self) -> list[Station]:
        return list(filter(lambda s: not s.occupied, self.__stations))

    @property
    def users(self) -> list[User]:
        return self.__users

    @property
    def working_users(self) -> list[User]:
        return list(filter(lambda u: u.have_station, self.__users))

    @property
    def servers(self) -> list[Server]:
        return self.__servers

    @property
    def stations(self) -> list[Station]:
        return self.__stations

    @property
    def have_gis(self) -> bool:
        for s in self.__servers:
            if s.have_gis:
                return True
        return False

    @property
    def have_dbms(self) -> bool:
        for s in self.__servers:
            if s.have_dbms:
                return True
        return False

    def tick(self) -> None:
        for server in self.__servers:
            server.tick()
        for station in self.__stations:
            station.tick()
        for user in self.__users:
            user.tick()

        if chance(self.user_spawn_prob):
            self.__all_time_users += 1
            self.add_user(User(self,
                               random.choice([Resolution.HD, Resolution.FullHD, Resolution.UltraHD]),
                               chance(self.user_need_gis_prob),
                               chance(self.user_need_dbms_prob),
                               random.randint(self.user_min_worktime, self.user_max_worktime)))

        broken_computers = self.broken_stations + self.broken_servers
        if len(broken_computers) > 0:
            random.choice(broken_computers).fix(random.randint(self.comp_min_fix_time, self.comp_max_fix_time))

        if chance(self.station_replace_prob) and len(self.free_stations) > 0:
            random.choice(self.free_stations).set_computer_room(random.choice(self.__rooms))

        if chance(self.server_replace_prob):
            rooms = list(filter(lambda r: len(r.servers) > 1, self.__rooms))
            if len(rooms) > 0:
                room = random.choice(rooms)
                room.remove_server(random.choice(room.servers))

        if chance(self.server_replace_prob):
            server = random.choice(self.__servers)
            rooms = list(filter(lambda r: server not in r.servers, self.__rooms))
            if len(rooms) > 0:
                random.choice(rooms).add_server(server)
