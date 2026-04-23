import tkinter as tk
from tkinter import ttk

from basicComponents.rectangleContainer import Container


class AlgorithmVersion:
    """Holds metadata for a single algorithm version."""

    def __init__(self, name: str, num_generations: int):
        self.name = name
        self.num_generations = num_generations


class VisualizerApp:
    """
    Visualizer for rectangle packing results across algorithm versions and generations.

    Zoom in / out
    Pan via keyboard or mouse drag

    Usage:
    versions = [
        AlgorithmVersion("PSO", num_generations=50),
        AlgorithmVersion("GA",   num_generations=100),
    ]

    app = VisualizerApp(versions)

    def on_gen_changed(version_index: int, generation: int):
        container = ...generate
        app.set_container(container)

    app.on_generation_changed = on_gen_changed
    app.run()
    """

    def __init__(
        self,
        versions: list[AlgorithmVersion],
        canvas_width: int = 800,
        canvas_height: int = 600,
    ):
        if not versions:
            raise ValueError("At least one AlgorithmVersion must be provided.")

        # ######################
        # ------- State --------
        # ######################
        self.versions = versions
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

        self.current_version = 0
        self.current_generation = 0

        self.container: Container | None = None

        # callback (set from outside)
        # signature: on_generation_changed(version_index: int, generation: int)
        self.on_generation_changed = None

        # view transform
        self.shiftX = 0
        self.shiftY = 0
        self.base_scale = 1.0   
        self.zoom = 1.0         

        # mouse pan state
        self._last_mouse_x = None
        self._last_mouse_y = None

        # ######################
        # ------ UI setup ------
        # ######################
        self.root = tk.Tk()
        self.root.title("Rectangle Packing Visualizer")

        self._build_ui()
        self.bindKeys()

      
        self._fire_generation_changed()

    # ======================================================
    # UI construction
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

        # Version selector
        ttk.Label(control_frame, text="Version").pack(anchor="w")
        self.version_selector = ttk.Spinbox(
            control_frame,
            from_=0,
            to=max(0, len(self.versions) - 1),
            width=10,
            command=self._on_version_change,
        )
        self.version_selector.set(0)
        self.version_selector.pack(anchor="w", pady=5)

        # Generation selector
        ttk.Label(control_frame, text="Generation").pack(anchor="w")
        self.gen_selector = ttk.Spinbox(
            control_frame,
            from_=0,
            to=max(0, self.versions[0].num_generations - 1),
            width=10,
            command=self._on_generation_change,
        )
        self.gen_selector.set(0)
        self.gen_selector.pack(anchor="w", pady=5)

        # Info label
        self.info_label = ttk.Label(control_frame, text="")
        self.info_label.pack(anchor="w", pady=10)

        self._update_info_labels()

    # ======================================================
    # Navigation callbacks
    # ======================================================

    def _on_version_change(self):
        try:
            self.current_version = int(self.version_selector.get())
            self.current_generation = 0

            # Update generation spinbox range for the new version
            new_max = max(0, self.versions[self.current_version].num_generations - 1)
            self.gen_selector.config(to=new_max)
            self.gen_selector.set(0)

            self._fire_generation_changed()
        except ValueError:
            pass

    def _on_generation_change(self):
        try:
            self.current_generation = int(self.gen_selector.get())
            self._fire_generation_changed()
        except ValueError:
            pass

    def _fire_generation_changed(self):
        """Call the external callback, then refresh UI."""
        if self.on_generation_changed:
            self.on_generation_changed(self.current_version, self.current_generation)

        self._update_info_labels()
        self.draw()

    # ======================================================
    # External API
    # ======================================================

    def set_container(self, container: Container):
        self.container = container
        self.fit_view()

    def fit_view(self):
        """Scale and center the container to fill the canvas."""
        if self.container is None or self.container.width == 0 or self.container.height == 0:
            self.shiftX = 0
            self.shiftY = 0
            self.zoom = 1.0
            self.draw()
            return

        padding = 20  # pixels of breathing room on each side

        scale_x = (self.canvas_width  - 2 * padding) / self.container.width
        scale_y = (self.canvas_height - 2 * padding) / self.container.height
        fit_scale = min(scale_x, scale_y)

        # base_scale is set in draw() as canvas_width / container.width;
        # zoom is the multiplier on top of that, so derive zoom from fit_scale
        self.base_scale = self.canvas_width / self.container.width
        self.zoom = fit_scale / self.base_scale

        # Center the scaled container in the canvas
        scaled_w = self.container.width  * fit_scale
        scaled_h = self.container.height * fit_scale
        self.shiftX = (self.canvas_width  - scaled_w) / 2
        self.shiftY = (self.canvas_height - scaled_h) / 2

        self.draw()

    def reset_view(self):
        self.fit_view()

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

        if self.container is None or self.container.width == 0:
            return

        # base_scale is set by fit_view(); only initialise here as a fallback
        if self.base_scale == 1.0:
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

        # Height label (above top edge)
        self.canvas.create_text(
            (cx1 + cx2) / 2,
            cy1 - 15,
            text=f"Height: {self.container.height:.2f}",
            font=("Arial", 12, "bold"),
        )

        # Width label (right of right edge)
        self.canvas.create_text(
            cx2 + 5,
            (cy1 + cy2) / 2,
            text=f"Width: {self.container.width:.2f}",
            font=("Arial", 12, "bold"),
            anchor="w",
        )

    # ======================================================
    # Info labels
    # ======================================================

    def _update_info_labels(self):
        version = self.versions[self.current_version]
        current_height = getattr(self.container, "height", 0) if self.container else 0
        current_width = getattr(self.container, "width", 0) if self.container else 0

        self.info_label.config(
            text=(
                f"Version: {self.current_version + 1}/{len(self.versions)}\n"
                f"  {version.name}\n"
                f"Generation: {self.current_generation + 1}/{version.num_generations}\n"
                f"Height: {current_height:.2f}\n"
                f"Width:  {current_width:.2f}"
            )
        )

    # ======================================================
    # Input bindings
    # ======================================================

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

        self.canvas.bind("<Key>", on_key)

        # mouse wheel zoom
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)   # Windows
        self.canvas.bind("<Button-4>", self._on_mousewheel)     # Linux scroll up
        self.canvas.bind("<Button-5>", self._on_mousewheel)     # Linux scroll down

        # mouse drag pan (middle button)
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

    # ======================================================
    # Run
    # ======================================================

    def run(self):
        self._fire_generation_changed()
        self.root.mainloop()