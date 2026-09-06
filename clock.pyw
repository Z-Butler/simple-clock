"""Simple clock application."""

import tkinter as tk
import datetime as dt


class Application(tk.Tk):
    """Initialize tkinter."""

    def __init__(
            self, x_pixel: int=2560, y_pixel: int=1440) -> None:
        super().__init__()

        # Main App configuration
        self.geometry(f"{x_pixel}x{y_pixel}+488+-1440")  # janky fullscreen effect.
        self.configure(background="black")
        self.overrideredirect(True)

        # Format trackers.
        self.time_format = True
        self.show_controls = True

        # Create center frame
        self.main_frame = tk.Frame(self, background="black")
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.control_label = tk.Label(self.main_frame,
                                      font=("times new roman", 25),
                                      foreground="red",
                                      background="black",
                                      anchor="center",
                                      text="'ESC' to quit | right/left arrows to "
                                           "change time format | 'h' to hide this "
                                           "text"
                                      )
        self.control_label.grid(column=0, row=0)

        # Create and configure time.
        self.time_label = tk.Label(self.main_frame,
                                   font=("times new roman", 220),
                                   foreground="purple",
                                   background="black",
                                   anchor="center",
                                   )
        self.time_label.grid(column=0, row=1)

        # Create and configure date
        self.date_label = tk.Label(self.main_frame,
                                   font=("times new roman", 45),
                                   foreground="purple",
                                   background="black",
                                   anchor="center",
                                   )
        self.date_label.grid(column=0, row=2)

        # Keybinds and update feature.
        self.update_clock()
        self.bind("<Escape>", self.on_escape)
        self.bind("<Right>", self.time_12)
        self.bind("<Left>", self.time_24)
        self.bind("<h>", self.app_controls)

    def update_clock(self) -> None:
        """Track and update date and time. Switches between 12/24-hour format."""
        self.time = dt.datetime.now()
        self.date = dt.date.today()

        if self.time_format:  # Set to 24-hour format.
            self.time_label.configure(text=f"{self.time.strftime('%H:%M')}")
        else:  # Set to 12-hour format
            self.time_label.configure(text=f"{self.time.strftime('%I:%M %p')}")

        self._clock_job_id = self.after(ms=1000, func=self.update_clock)
        self.date_label.configure(text=f"{self.date.strftime('%A - %B %d')}")

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

    def app_controls(self, event: tk.Event | None = None) -> None:
        """Show/Hide app controls."""
        if self.show_controls:
            self.show_controls = False
            self.control_label.configure(text="")
        else:
            self.show_controls = True
            self.control_label.configure(text="'ESC' to quit | right/left arrows to "
                                              "change time format | 'h' to hide this "
                                              "text")

def main() -> None:
    app = Application()
    app.mainloop()


if __name__ == "__main__":
    main()
