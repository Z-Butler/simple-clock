"""Simple clock application."""
from modules import tkinter_closet as tkc
import tkinter as tk
import datetime as dt
from multiprocessing import Process, Pipe

menu_text = ("'ESC' to quit | "
             "right/left arrows to change time format | "
             "up/down arrows to change date format | "
             "'w' for weather | "
             "'h' to hide this text")


class Application(tk.Tk):
    """Initialize tkinter."""

    zip_code = None

    def __init__(
            self, x_pixel: int = 2560, y_pixel: int = 1440) -> None:
        super().__init__()
        self._clock_job_id = None

        # Main App configuration
        self.geometry(f"{x_pixel}x{y_pixel}+488+-1440")  # janky fullscreen effect.
        self.configure(background="black")
        self.overrideredirect(True)  # True = No border

        # Format trackers.
        self.time_format = True
        self.show_controls = True
        self.date_format = 0

        # Create center frame
        self.main_frame = tk.Frame(self, background="black")
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.control_label = tk.Label(
            self.main_frame,
            font=("times new roman", 25),
            foreground="red",
            background="black",
            anchor="center",
            text=menu_text
        )
        self.control_label.grid(column=0, row=0)

        # Create and configure time.
        self.time_label = tk.Label(
            self.main_frame,
            font=("times new roman", 220),
            foreground="purple",
            background="black",
            anchor="center",
        )
        self.time_label.grid(column=0, row=1)

        # Create and configure date
        self.date_label = tk.Label(
            self.main_frame,
            font=("times new roman", 45),
            foreground="purple",
            background="black",
            anchor="center",
        )
        self.date_label.grid(column=0, row=2)

        self.zipcode_input = tkc.InputForm(
            self,
            label_text="Enter zip code:",
            preview=True,
            font_config=("times new roman", 20),
            limit_state=True,
            limit_max=5,
            limit_min=5,
        )
        self.zipcode_input.grid(column=0, row=0)

        # Keybinds and update feature.
        self.update_clock()
        self.bind("<Escape>", self.on_escape)
        self.bind("<Right>", self.time_12)
        self.bind("<Left>", self.time_24)
        self.bind("<Up>", self.change_date_up)
        self.bind("<Down>", self.change_date_down)
        self.bind("<h>", self.app_controls)
        self.bind("<w>", self.weather)


    def update_clock(self) -> None:
        """Track and update date and time. Switches between 12/24-hour format."""
        time = dt.datetime.now()
        date = dt.date.today()

        if self.time_format:  # Set to 24-hour format.
            self.time_label.configure(text=f"{time.strftime('%H:%M')}")
        else:  # Set to 12-hour format
            self.time_label.configure(text=f"{time.strftime('%I:%M %p')}")

        if self.date_format == 0:
            self.date_label.configure(text=f"{date.strftime('%A - %B %d')}")
        elif self.date_format == 1:
            self.date_label.configure(text=f"{date.strftime('%Y-%m-%d')}")
        elif self.date_format == 2:
            self.date_label.configure(text=f"{date.strftime('%m/%d/%Y')}")
        elif self.date_format == 3:
            self.date_label.configure(text=f"{date.strftime('%d/%m/%Y')}")
        elif self.date_format == 4:
            self.date_label.configure(text=f"{date.strftime('%B %d, %Y')}")
        elif self.date_format == 5:
            self.date_label.configure(text=f"{date.strftime('%A, %B %d, %Y')}")

        self._clock_job_id = self.after(ms=1000, func=self.update_clock)

    def on_escape(self, event: tk.Event | None = None) -> None:
        """Cancel pending clock update and close application."""
        self.after_cancel(self._clock_job_id)
        self.destroy()

    def time_12(self, event: tk.Event | None = None) -> None:
        """Change clock to 12-hour format."""
        self.time_format = False

    def time_24(self, event: tk.Event | None = None) -> None:
        """Change clock to 24-hour format."""
        self.time_format = True

    def change_date_up(self, event: tk.Event | None = None) -> None:
        """Change date format."""
        if self.date_format < 5:
            self.date_format += 1
        else:
            self.date_format = 0

    def change_date_down(self, event: tk.Event | None = None) -> None:
        """Change date format."""
        if self.date_format > 0:
            self.date_format -= 1
        else:
            self.date_format = 5

    def weather(self, event: tk.Event | None = None) -> None:
        """Show weather conditions."""
        pass

    def app_controls(self, event: tk.Event | None = None) -> None:
        """Show/Hide app controls."""
        if self.show_controls:
            self.show_controls = False
            self.control_label.configure(text="")
            self.zipcode_input.grid_forget()
        else:
            self.show_controls = True
            self.control_label.configure(text=menu_text)
            self.zipcode_input.grid()


def main() -> None:
    app = Application()
    app.mainloop()


if __name__ == "__main__":
    main()
