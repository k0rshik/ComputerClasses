from tkinter import *
from abc import ABC, abstractmethod
from math import sqrt, ceil
from visulisation.config import *
from enum import Enum


class Color(Enum):
    Shaded = 0
    Unselected = 1
    Selected = 2


class VisualizationObject(ABC):
    _canvas: Canvas

    def __init__(self, visualization, obj):
        self._visualisation = visualization
        self._canvas = visualization.canvas
        self._obj = obj
        self._canvas.tag_bind(self._obj, "<Button-1>", self._onclick)
        self._widgets = []
        self._current_color = Color.Unselected

    def remove(self):
        self._canvas.delete(self._obj)
        self._obj = None

    def update(self):
        self.update_color()

    def update_color(self):
        match self._current_color:
            case Color.Shaded:
                self._canvas.itemconfig(self._obj, fill=shaded_bg, outline=shaded_fg)
            case Color.Unselected:
                self._canvas.itemconfig(self._obj, fill=unselected_bg, outline=unselected_fg)
            case Color.Selected:
                self._canvas.itemconfig(self._obj, fill=selected_bg, outline=selected_fg)

    def _onclick(self, *args):
        self._visualisation.set_low()
        self.select()
        self.pack()

    def select(self):
        self._current_color = Color.Selected
        self.update_color()

    def unselect(self):
        self._current_color = Color.Unselected
        self.update_color()

    def shade(self):
        self._current_color = Color.Shaded
        self.update_color()

    def change_position(self, x, y, width, height):
        self._canvas.coords(self._obj, x, y, x + width, y + height)

    @property
    def center(self):
        cords = self._canvas.coords(self._obj)
        return (cords[0] + cords[2]) / 2, (cords[1] + cords[3]) / 2

    def pack(self):
        self._visualisation.unpack()
        for w in self._widgets:
            w.pack(anchor=NW)

    def unpack(self):
        for w in self._widgets:
            w.pack_forget()


class SeverVisualization(VisualizationObject):
    def __init__(self, visualization, server, x=0, y=0, width=0, height=0):
        super().__init__(visualization,
                         visualization.canvas.create_rectangle(x, y, x + width, y + height, width=2))
        self.__server = server

        # Widgets setup
        self._widgets.append(Label(text=f"Server: {id(server)}"))
        self._widgets.append(Label(text=f"Have GIS: {server.have_gis}"))
        self._widgets.append(Label(text=f"Have DBMS: {server.have_dbms}"))
        self._widgets.append(Label(text=f"Crush probability: {server.chash_probability}"))
        self._widgets.append(Label(text=""))

        text_crush_protect = f"Have crush protect: {server.have_crush_protect}"
        if server.have_crush_protect:
            if server.crush_protect_used:
                text_crush_protect += " | Used"
            else:
                text_crush_protect += " | Not used"

        self._text_crush_protect = StringVar(value=text_crush_protect)
        self._widgets.append(Label(textvariable=self._text_crush_protect))

        self._text_broken = StringVar(value=f"Broken: {server.is_broken}")
        self._widgets.append(Label(textvariable=self._text_broken))

    def update_color(self):
        if self.__server.is_broken:
            match self._current_color:
                case Color.Shaded:
                    self._canvas.itemconfig(self._obj, fill=broken_shaded_bg, outline=shaded_fg)
                case Color.Unselected:
                    self._canvas.itemconfig(self._obj, fill=broken_unselected_bg, outline=unselected_fg)
                case Color.Selected:
                    self._canvas.itemconfig(self._obj, fill=broken_selected_bg, outline=selected_fg)
        else:
            super().update_color()

    @property
    def server(self):
        return self.__server

    @property
    def center(self):
        cords = self._canvas.coords(self._obj)
        return (cords[0] + cords[2]) / 2, cords[3]

    def update(self):
        super().update()
        self.widgets_update()

    def widgets_update(self):
        self._text_broken.set(f"Broken: {self.__server.is_broken}")

        text_crush_protect = f"Have crush protect: {self.__server.have_crush_protect}"
        if self.__server.have_crush_protect:
            if self.__server.crush_protect_used:
                text_crush_protect += " | Used"
            else:
                text_crush_protect += " | Not used"
        self._text_crush_protect.set(text_crush_protect)

    def _onclick(self, *args):
        self._visualisation.unpack()
        self.pack()
        super()._onclick(*args)


class StationVisualization(VisualizationObject):
    def __init__(self, visualization, station, x=0, y=0, width=0, height=0):
        super().__init__(visualization,
                         visualization.canvas.create_rectangle(x, y, x + width, y + height, width=2))
        self.__station = station

        # Widgets setup
        self._widgets.append(Label(text=f"Station: {id(station)}"))
        self._widgets.append(Label(text=f"Have GIS: {station.have_gis}"))
        self._widgets.append(Label(text=f"Have DBMS: {station.have_dbms}"))
        self._widgets.append(Label(text=f"Crush probability: {station.chash_probability}"))
        self._widgets.append(Label(text=f"Resolution: {station.display_resolution}"))
        self._widgets.append(Label(text=""))

        self._text_broken = StringVar(value=f"Broken: {station.is_broken}")
        self._widgets.append(Label(textvariable=self._text_broken))

        self._text_occupied = StringVar(value=f"Occupied: {station.occupied}")
        self._widgets.append(Label(textvariable=self._text_occupied))

    def update_color(self):
        if self.__station.is_broken:
            match self._current_color:
                case Color.Shaded:
                    self._canvas.itemconfig(self._obj, fill=broken_shaded_bg, outline=shaded_fg)
                case Color.Unselected:
                    self._canvas.itemconfig(self._obj, fill=broken_unselected_bg, outline=unselected_fg)
                case Color.Selected:
                    self._canvas.itemconfig(self._obj, fill=broken_selected_bg, outline=selected_fg)
        elif self.__station.occupied:
            match self._current_color:
                case Color.Shaded:
                    self._canvas.itemconfig(self._obj, fill=occupied_shaded_bg, outline=shaded_fg)
                case Color.Unselected:
                    self._canvas.itemconfig(self._obj, fill=occupied_unselected_bg, outline=unselected_fg)
                case Color.Selected:
                    self._canvas.itemconfig(self._obj, fill=occupied_selected_bg, outline=selected_fg)
        else:
            super().update_color()

    @property
    def station(self):
        return self.__station

    def set_station(self, station):
        self.__station = station

    def update(self):
        super().update()
        self.widgets_update()

    def widgets_update(self):
        self._text_broken.set(f"Broken: {self.__station.is_broken}")
        self._text_occupied.set(f"Occupied: {self.__station.occupied}")


class RoomVisualization(VisualizationObject):
    def __init__(self, visualization, room, x=0, y=0, width=0, height=0):
        super().__init__(visualization,
                         visualization.canvas.create_rectangle(x, y, x + width, y + height, width=2))
        self.__room = room
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height

        self._widgets.append(Label(text=f"Room: {id(self.__room)}"))
        self.__servers_text = StringVar(value=f"Servers: {len(room.servers)}")
        self._widgets.append(Label(textvariable=self.__servers_text))
        self.__stations_text = StringVar(value=f"Stations: {len(room.stations)}")
        self._widgets.append(Label(textvariable=self.__stations_text))
        self.__users_text = StringVar(value=f"Users: {len(room.users)}")
        self._widgets.append(Label(textvariable=self.__users_text))


    def update_widgets(self):
        self.__servers_text.set(f"Servers: {len(self.__room.servers)}")
        self.__stations_text.set(f"Stations: {len(self.__room.stations)}")
        self.__users_text.set(f"Users: {len(self.__room.users)}")


    def change_position(self, x, y, width, height):
        super().change_position(x, y, width, height)
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.update_stations()

    def set_low_all(self):
        super().shade()
        for station in self._visualisation.stations:
            if station.station in self.__room.stations:
                station.shade()

    def set_mid_all(self):
        super().unselect()
        for station in self._visualisation.stations:
            if station.station in self.__room.stations:
                station.unselect()

    def set_high_all(self):
        super().select()
        for station in self._visualisation.stations:
            if station.station in self.__room.stations:
                station.select()

    def update_stations(self):
        n = 0
        for station in self._visualisation.stations:
            if station.station in self.__room.stations:
                station.update()
                station.change_position(*self.__get_station_pos(n))
                n += 1

    def __get_station_pos(self, number):
        size = ceil(sqrt(len(self.__room.stations)))
        height = int(self.__height * 0.9 / size)
        height_margin = int((self.__height * 0.1) / (size + 1))

        width = int(self.__width * 0.9 / size)
        width_margin = int((self.__width * 0.1) / (size + 1))

        return [self.__x + (width_margin + width) * (number % size) + width_margin,
                self.__y + (height_margin + height) * (number // size) + height_margin,
                width,
                height]

    def update(self):
        super().update()
        self.update_stations()
        self.update_widgets()

    def _onclick(self, *args):
        super()._onclick(*args)

    @property
    def center(self):
        cords = self._canvas.coords(self._obj)
        return (cords[0] + cords[2]) / 2, cords[1]

    def connected_to(self, server: SeverVisualization):
        return server.server in self.__room.servers


class Connection(VisualizationObject):
    def __init__(self, visualization, room: RoomVisualization, server: SeverVisualization):
        super().__init__(visualization,
                         visualization.canvas.create_line(*room.center, *server.center, width=2))
        self.__room = room
        self.__server = server

        self._widgets.append(Label(text=f"Connection: {id(self)}"))

    def select(self):
        super().select()
        self._canvas.tag_raise(self._obj)

    def update_color(self):
        if self.__room.connected_to(self.__server):
            match self._current_color:
                case Color.Shaded:
                    self._canvas.itemconfig(self._obj, fill=shaded_fg)
                case Color.Unselected:
                    self._canvas.itemconfig(self._obj, fill=unselected_fg)
                case Color.Selected:
                    self._canvas.itemconfig(self._obj, fill=selected_fg)
        else:
            self._canvas.itemconfig(self._obj, fill=canvas_color)
            self._canvas.tag_lower(self._obj)
            self._canvas.tag_lower(self._visualisation.rectangle)

    def change_position(self, x1, y1, x2, y2):
        self._canvas.coords(self._obj, x1, y1, x2, y2)

    def update_position(self):
        self.change_position(*self.__server.center, *self.__room.center)

    def _onclick(self, *args):
        self._visualisation.on_canvas_click()
