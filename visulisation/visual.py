from simulation.sim import Simulation
from visulisation.visualization_objects import SeverVisualization, RoomVisualization, StationVisualization, Connection
from tkinter import *
from tkinter import ttk
from visulisation.config import *


class Visualization:
    __simulation: Simulation
    __window: Tk
    __canvas: Canvas

    def __init__(self, simulation: Simulation, width: int, height: int):
        self.__simulation = simulation

        self.__window = Tk()
        self.__window.geometry(f"{width}x{height}")
        self.__window.geometry(
            f"+{self.__window.winfo_screenwidth() // 2 - width // 2}+{self.__window.winfo_screenheight() // 2 - height // 2}")
        self.__window.title("Computer classes")
        self.__window.update()

        self.__canvas = Canvas(bg=canvas_color)
        self.__rectangle = self.__canvas.create_rectangle(0, 0, 0, 0, width=0)

        self.__canvas.tag_bind(self.__rectangle, "<Button-1>", self.on_canvas_click)
        self.__configure_canvas()
        self.__window.bind("<Configure>", self.__on_change_size)

        # self.__canvas.grid(row=0, column=0)
        self.__canvas.pack(side=LEFT)
        mspt_frame = Frame()
        mspt_frame.pack(side=BOTTOM, anchor=S)

        self.__mspt = IntVar(value=10)
        Label(mspt_frame, text="MSTP").pack(anchor=SE, side=RIGHT, pady=3)
        ttk.Entry(mspt_frame, width=6, textvariable=self.__mspt, validate="key",
                  validatecommand=(self.__window.register(lambda x: x.isdigit() and 10 <= int(x) <= 1000), "%P")).pack(
            anchor=SE, side=RIGHT, pady=3)
        ttk.Scale(mspt_frame, from_=10, to=1000, variable=self.__mspt,
                  command=lambda s: self.__mspt.set(int(float(s)))).pack(anchor=SE, side=RIGHT, padx=5)
        self.__pause = False
        self.__button = ttk.Button(mspt_frame, text="Stop", command=self.__on_button_click)
        self.__button.pack(anchor=SE, side=RIGHT, padx=5, pady=3)

        self.__widgets = []
        self.__widgets.append(Label(text="Simulation"))
        self.__widgets.append(Label(text=f"Servers: {len(simulation.servers)}"))
        self.__widgets.append(Label(text=f"Stations: {len(simulation.stations)}"))

        self.__users_text = StringVar(value=f"Users: {len(simulation.users)}")
        self.__widgets.append(Label(textvariable=self.__users_text))

        self.__success_users_text = StringVar(
            value=f"All/Success users: {simulation.users_count}/{simulation.success_users_count}")
        self.__widgets.append(Label(textvariable=self.__success_users_text))

        self.__servers = []
        for i in range(len(self.__simulation.servers)):
            self.__servers.append(SeverVisualization(self, self.__simulation.servers[i], *self.__get_server_pos(i)))

        self.__rooms = []
        for i in range(len(self.__simulation.computer_rooms)):
            self.__rooms.append(RoomVisualization(self, self.__simulation.computer_rooms[i], *self.__get_room_pos(i)))

        self.__stations = []
        for i in range(len(self.__simulation.stations)):
            self.__stations.append(StationVisualization(self, self.__simulation.stations[i], 0, 0, 0, 0))

        self.__connections = []
        for room in self.__rooms:
            for server in self.__servers:
                self.__connections.append(Connection(self, room, server))

        self.pack()
        self.__ticks = 0
        self.update()
        self.__window.mainloop()

    def __on_button_click(self):
        self.__pause = not self.__pause
        if self.__pause:
            self.__button.configure(text="Start")
        else:
            self.__button.configure(text="Stop")

    @property
    def canvas(self):
        return self.__canvas

    @property
    def rectangle(self):
        return self.__rectangle

    def update_widgets(self):
        self.__users_text.set(f"Users: {len(self.__simulation.users)}")
        self.__success_users_text.set(
            f"All/Success users: {self.__simulation.users_count}/{self.__simulation.success_users_count}")

    def pack(self):
        self.unpack()
        for widget in self.__widgets:
            widget.pack(anchor=NW)

    def unpack(self):
        for obj in self.__servers + self.__stations + self.__rooms + self.__connections:
            obj.unpack()
        for widget in self.__widgets:
            widget.pack_forget()

    def on_canvas_click(self, *args):
        for s in self.__servers:
            s.unselect()
        for r in self.__rooms:
            r.set_mid_all()
        for c in self.__connections:
            c.unselect()

        self.pack()

    def __on_change_size(self, *args):
        self.__configure_canvas()
        for i in range(len(self.__servers)):
            self.__servers[i].change_position(*self.__get_server_pos(i))

        for i in range(len(self.__rooms)):
            self.__rooms[i].change_position(*self.__get_room_pos(i))

        for c in self.__connections:
            c.update_position()

    def __configure_canvas(self):
        self.__canvas_width = int(self.__window.winfo_width() * canvas_size)
        self.__canvas_height = self.__window.winfo_height()
        self.__canvas.configure(width=self.__canvas_width,
                                height=self.__canvas_height)
        self.__canvas.coords(self.__rectangle, 0, 0, self.__canvas_width, self.__canvas_height)

    def __get_server_pos(self, number):
        height = int(self.__canvas_height * 0.9 / 7)
        width = int(self.__canvas_width * 0.9 / len(self.__simulation.servers))
        width_margin = int((self.__canvas_width * 0.1) / (len(self.__simulation.servers) + 1))

        return [width_margin * (number + 1) + width * number, height, width, height]

    def __get_room_pos(self, number):
        height = int(self.__canvas_height * 0.9 / 7)
        width = int(self.__canvas_width * 0.9 / len(self.__simulation.computer_rooms))
        width_margin = int((self.__canvas_width * 0.1) / (len(self.__simulation.computer_rooms) + 1))

        return [width_margin * (number + 1) + width * number, height * 3, width, height * 4]

    def set_low(self):
        for s in self.__servers:
            s.shade()
        for r in self.__rooms:
            r.set_low_all()
        for c in self.__connections:
            c.shade()

    def update(self):
        self.__window.after(self.__mspt.get(), self.update)
        if self.__pause: return

        self.__simulation.tick()
        self.__ticks += 1
        self.__window.title(str(self.__ticks))

        for s in self.__servers:
            s.update()

        for r in self.__rooms:
            r.update()

        for c in self.__connections:
            c.update()

        self.update_widgets()

    @property
    def stations(self):
        return self.__stations
