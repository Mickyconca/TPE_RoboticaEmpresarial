import tkinter as tk
from tkinter import simpledialog
import os


class PomodoroApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600")
        self.root.title("Pomodoro Timer")

        self.pomodoro_time = 25 * 60
        self.break_time = 5 * 60
        self.is_paused = False
        self.automatic_mode = False

        self.timer_label = tk.Label(self.root, font=('Helvetica', 48), bg='green')
        self.timer_label.pack(pady=100)

        self.start_button = tk.Button(self.root, text="Iniciar", command=self.start_pomodoro)

        self.pause_button = tk.Button(self.root, text="Pausar", command=self.pause_timer)
        self.pause_button.pack(pady=20)

        self.automatic_button = tk.Button(self.root, text="Iniciar Pomodoro", command=self.toggle_automatic_mode)
        self.automatic_button.pack(pady=20)

        self.config_button = tk.Button(self.root, text="Configurar Tiempos", command=self.configure_times)
        self.config_button.pack(pady=20)

        self.remaining_time = 0
        self.mode = None

    def play_sound(self):
        os.system("afplay alert.mp3")

    def toggle_automatic_mode(self):
        self.automatic_mode = not self.automatic_mode
        if self.automatic_mode:
            self.automatic_button.config(text="Detener Pomodoro")
            self.start_pomodoro()
        else:
            self.automatic_button.config(text="Iniciar Pomodoro")
            self.stop_timer()

    def pause_timer(self):
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.pause_button.config(text="Reanudar")
        else:
            self.pause_button.config(text="Pausar")
            self.update_timer()

    def start_pomodoro(self):
        self.mode = "pomodoro"
        self.remaining_time = self.pomodoro_time
        self.timer_label.config(bg="green")
        self.start_button.config(text="Detener", command=self.stop_timer)
        self.update_timer()

    def start_break(self):
        self.mode = "break"
        self.remaining_time = self.break_time
        self.set_background_color("red")
        self.timer_label.config(bg="red")
        self.start_button.config(text="Detener", command=self.stop_timer)
        self.update_timer()

    def stop_timer(self):
        self.remaining_time = 0
        self.start_button.config(text="Iniciar Pomodoro", command=self.start_pomodoro)

    def update_display(self):
        minutes, seconds = divmod(self.remaining_time, 60)
        self.timer_label.config(text=f"{minutes:02}:{seconds:02}")

    def update_timer(self):
        if self.is_paused:
            return

        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.update_display()
            self.root.after(1000, self.update_timer)
        else:
            if self.automatic_mode:
                self.play_sound()
            if self.mode == "pomodoro":
                self.start_button.config(text="Iniciar Recreo", command=self.start_break)
                if self.automatic_mode:
                    self.start_break()
            elif self.mode == "break":
                self.start_button.config(text="Iniciar Pomodoro", command=self.start_pomodoro)
                if self.automatic_mode:
                    self.start_pomodoro()

    def set_background_color(self, color):
        self.root.configure(bg=color)

    def configure_times(self):
        self.pomodoro_time = simpledialog.askinteger("Configurar", "Tiempo del Pomodoro (en minutos)", minvalue=1) * 60
        self.break_time = simpledialog.askinteger("Configurar", "Tiempo de recreo (en minutos)",
                                                        minvalue=1) * 60


if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()
