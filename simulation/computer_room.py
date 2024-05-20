class ComputerRoom:

    def __init__(self, servers=None):
        if servers is None:
            self.__servers = []
        else:
            self.__servers = servers.copy()

        self.__stations = []

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

    @property
    def stations(self):
        return self.__stations

    @property
    def servers(self):
        return self.__servers

    @property
    def broken_stations(self):
        return list(filter(lambda s: s.is_broken, self.__stations))

    @property
    def broken_servers(self):
        return list(filter(lambda s: s.is_broken, self.__servers))

    @property
    def users(self):
        result = []
        for station in self.__stations:
            if station.occupied:
                result.append(station.user)
        return result

    # Room -- Station
    def add_station(self, station) -> None:
        if station not in self.__stations:
            self.__stations.append(station)
            station.set_computer_room(self)

    def remove_station(self, station) -> None:
        if station in self.__stations:
            self.__stations.remove(station)
            station.remove_computer_room(self)

    # Room -> Server
    def add_server(self, server) -> None:
        if server not in self.__servers:
            self.__servers.append(server)

    def remove_server(self, server) -> None:
        if server in self.__servers:
            self.__servers.remove(server)
