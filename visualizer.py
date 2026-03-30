import tkinter as tk
from tkinter import ttk
from placement.otherAlgorithms.PositionsBLF import *
from geneticAlgorithms import pygadGenetic
import time

from utils import sortInput

import tkinter as tk
from tkinter import ttk

from basicComponents.rectangleContainer import Container
from placement.otherAlgorithms.bottomLeftFill import bottom_left_fill

import tkinter as tk
from tkinter import ttk


class VisualizerApp:
    """
        Zoom in / out
        Pan via keyboard or mouse drag
    """

    def __init__(
        self,
        num_generations: int,
        num_populations: int,
        container_width: float,
        canvas_width: int = 800,
        canvas_height: int = 600,
    ):
        # ######################
        # ------- State ---
        # ######################
        self.num_generations = num_generations
        self.num_populations = num_populations
        self.container_width = container_width

        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

        self.current_generation = 0
        self.current_population = 0

        self.container = Container(container_width)

        # callbacks (set from outside)
        self.on_generation_changed = None
        self.on_population_changed = None

        # view transform
        self.shiftX = 0
        self.shiftY = 0
        self.base_scale = 1.0     # fit-to-width scale
        self.zoom = 1.0           # user zoom multiplier

        # mouse pan state
        self._last_mouse_x = None
        self._last_mouse_y = None

        # ######################
        # ------ UI setup ---
        # ######################
        self.root = tk.Tk()
        self.root.title("Rectangle Packing Visualizer")

        self._build_ui()
        self._update_info_labels()
        self.bindKeys()
        self.draw()

    # ======================================================
    # -------UI construction
    # ======================================================

    def _build_ui(self):
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas
        self.canvas = tk.Canvas(
            self.main_frame,
            width=self.canvas_width,
            height=self.canvas_height,
            bg="white",
        )
        self.canvas.grid(row=0, column=0, rowspan=6, padx=10, pady=10)

        # Controls
        control_frame = ttk.Frame(self.main_frame)
        control_frame.grid(row=0, column=1, sticky="ns", padx=10, pady=10)

        # Generation selector
        ttk.Label(control_frame, text="Generation").pack(anchor="w")
        self.gen_selector = ttk.Spinbox(
            control_frame,
            from_=0,
            to=max(0, self.num_generations - 1),
            width=10,
            command=self._on_generation_change,
        )
        self.gen_selector.set(0)
        self.gen_selector.pack(anchor="w", pady=5)

        # Population selector
        ttk.Label(control_frame, text="Population").pack(anchor="w")
        self.pop_selector = ttk.Spinbox(
            control_frame,
            from_=0,
            to=max(0, self.num_populations - 1),
            width=10,
            command=self._on_population_change,
        )
        self.pop_selector.set(0)
        self.pop_selector.pack(anchor="w", pady=5)

        # Info label
        self.info_label = ttk.Label(control_frame, text="")
        self.info_label.pack(anchor="w", pady=10)

    # ======================================================
    # --------------Navigation callbacks
    # ======================================================

    def _on_generation_change(self):
        try:
            self.current_generation = int(self.gen_selector.get())
            self.current_population = 0
            self.pop_selector.set(0)

            if self.on_generation_changed:
                self.on_generation_changed(self.current_generation)

            self._update_info_labels()
            self.draw()
        except ValueError:
            pass

    def _on_population_change(self):
        try:
            self.current_population = int(self.pop_selector.get())

            if self.on_population_changed:
                self.on_population_changed(
                    self.current_generation,
                    self.current_population,
                )

            self._update_info_labels()
            self.draw()
        except ValueError:
            pass

    # ======================================================
    # External API
    # ======================================================

    def set_container(self, container: Container):
        self.container = container
        self.reset_view()

    def reset_view(self):
        self.shiftX = 0
        self.shiftY = 0
        self.zoom = 1.0
        self.draw()

    def zoom_in(self, factor=1.1):
        self.zoom *= factor
        self.draw()

    def zoom_out(self, factor=1.1):
        self.zoom /= factor
        self.draw()

    # ======================================================
    # Drawing
    # ======================================================

    def _scale_coords(self, x, y, w, h):
        s = self.base_scale * self.zoom

        canvas_x1 = x * s + self.shiftX
        canvas_y1 = self.canvas_height - (y + h) * s + self.shiftY
        canvas_x2 = (x + w) * s + self.shiftX
        canvas_y2 = self.canvas_height - y * s + self.shiftY

        return canvas_x1, canvas_y1, canvas_x2, canvas_y2

    def draw(self):
        self.canvas.delete("all")

        if self.container.width == 0:
            return

        # compute base scale once (fit container width)
        self.base_scale = self.canvas_width / self.container.width

        # Container boundary
        cx1, cy1, cx2, cy2 = self._scale_coords(
            0, 0, self.container.width, self.container.height
        )
        self.canvas.create_rectangle(cx1, cy1, cx2, cy2, outline="red", width=2)

        # Rectangles
        for rect in self.container.rectangles:
            x1, y1, x2, y2 = self._scale_coords(
                rect.x, rect.y, rect.width, rect.height
            )
            self.canvas.create_rectangle(
                x1, y1, x2, y2, fill=rect.color, outline="black"
            )

        # Height label
        self.canvas.create_text(
            (cx1 + cx2) / 2,
            cy1 - 15,
            text=f"Height: {self.container.height:.2f}",
            font=("Arial", 12, "bold"),
        )

    # ======================================================
    # Info + input
    # ======================================================

    def _update_info_labels(self):
        current_height = getattr(self.container, "height", 0)
        current_width = getattr(self.container, "width", 0)

        self.info_label.config(
            text=(
                f"Generation: {self.current_generation + 1}/{self.num_generations}\n"
                f"Population: {self.current_population + 1}/{self.num_populations}\n"
                f"Height: {current_height:.2f}\n"
                f"Width: {current_width:.2f}"
            )
    )

    def addShift(self, x, y):
        self.shiftX += x
        self.shiftY += y
        self.draw()

    def bindKeys(self):
        def on_key(event):
            k = event.keysym.lower()

            # pan
            if k in ("w", "up"):
                self.addShift(0, 20)
            elif k in ("s", "down"):
                self.addShift(0, -20)
            elif k in ("a", "left"):
                self.addShift(20, 0)
            elif k in ("d", "right"):
                self.addShift(-20, 0)

            # zoom
            elif k in ("plus", "equal"):
                self.zoom_in()
            elif k in ("minus", "underscore"):
                self.zoom_out()

            return "break"

        # keyboard
        self.canvas.bind("<Key>", on_key)

        # mouse wheel zoom
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)      # Windows
        self.canvas.bind("<Button-4>", self._on_mousewheel)        # Linux
        self.canvas.bind("<Button-5>", self._on_mousewheel)

        # mouse drag pan
        self.canvas.bind("<ButtonPress-2>", self._start_pan)
        self.canvas.bind("<B2-Motion>", self._do_pan)

        self.canvas.bind("<Button-1>", lambda e: self.canvas.focus_set())

    # ======================================================
    # Mouse handlers
    # ======================================================

    def _on_mousewheel(self, event):
        if event.delta > 0 or event.num == 4:
            self.zoom_in()
        else:
            self.zoom_out()

    def _start_pan(self, event):
        self._last_mouse_x = event.x
        self._last_mouse_y = event.y

    def _do_pan(self, event):
        dx = event.x - self._last_mouse_x
        dy = event.y - self._last_mouse_y

        self.shiftX += dx
        self.shiftY += dy

        self._last_mouse_x = event.x
        self._last_mouse_y = event.y

        self.draw()

    ##====================================================
    # Run
    ####======================================================

    def run(self):
        self.root.mainloop()

