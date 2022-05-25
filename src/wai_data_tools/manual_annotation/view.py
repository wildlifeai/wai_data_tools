"""View logic for manual annotation."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union

from matplotlib import backend_bases as plt_types
from matplotlib import pyplot as plt
from matplotlib import widgets as pltwid

if TYPE_CHECKING:
    from wai_data_tools.manual_annotation.controller import ManualAnnotationController


class ManualAnnotationView:
    """View class for manual annotation tool."""

    def __init__(self):
        """Initialize view object."""
        fig, ax_img = plt.subplots()
        self.ax_img = ax_img

        plt.subplots_adjust(bottom=0.2)

        ax_save = plt.axes([0.1, 0.05, 0.1, 0.075])
        ax_togg = plt.axes([0.5, 0.01, 0.15, 0.075])
        ax_prev = plt.axes([0.7, 0.05, 0.1, 0.075])
        ax_next = plt.axes([0.81, 0.05, 0.1, 0.075])

        self.bsave = pltwid.Button(ax_save, "Save")
        self.bnext = pltwid.Button(ax_next, "Next")
        self.bprev = pltwid.Button(ax_prev, "Previous")
        self.btogg = pltwid.Button(ax_togg, "Toggle Class")

        self.bnext.on_clicked(self.next_button_clicked)
        self.bprev.on_clicked(self.prev_button_clicked)
        self.btogg.on_clicked(self.toggle_class_button_clicked)
        self.bsave.on_clicked(self.save_frames_button_clicked)

        fig.canvas.mpl_connect("key_press_event", self.hotkey_pressed)

        self.frame_display = None
        self.controller: Union[None, ManualAnnotationController] = None

    def set_controller(self, controller: ManualAnnotationController) -> None:
        """Set controller for view object.

        Args:
            controller: controller object for manual annotation tool
        """
        self.controller = controller
        self.frame_display = self.ax_img.imshow(self.controller.get_current_frame_image())

    def update_view(self) -> None:
        """Update view in figure.

        Raises:
            AttributeError: Raises if frame display is not initialized.
        """
        if self.frame_display is None:
            raise AttributeError("Frame display not initialized. Something went wrong.")

        self.check_controller_initialized()
        self.frame_display.set_array(self.controller.get_current_frame_image())
        self.ax_img.set_title(f"Frame {self.controller.get_current_frame_index()}")
        self.btogg.ax.set_title(f"Class: {self.controller.get_current_frame_class()}")
        plt.pause(0.001)

    @staticmethod
    def show() -> None:
        """Show figure."""
        plt.show()

    def next_button_clicked(self, _mouse_event: Optional[plt_types.MouseEvent] = None) -> None:
        """Increments frame index and updates view.

        Args:
            _mouse_event: Ignored. It is there for compatibility.
        """
        self.check_controller_initialized()
        self.controller.update_index(increasing=True)
        self.update_view()

    def prev_button_clicked(self, _mouse_event: Optional[plt_types.MouseEvent] = None) -> None:
        """Decrements frame index and updates view.

        Args:
            _mouse_event: Ignored. It is there for compatibility.
        """
        self.check_controller_initialized()
        self.controller.update_index(increasing=False)
        self.update_view()

    def toggle_class_button_clicked(self, _mouse_event: Optional[plt_types.MouseEvent] = None) -> None:
        """Toggles class for current frame and updates view.

        Args:
            _mouse_event: Ignored. It is there for compatibility.
        """
        self.check_controller_initialized()
        self.controller.toggle_current_frame_class()
        self.update_view()

    def save_frames_button_clicked(self, _mouse_event: Optional[plt_types.MouseEvent] = None) -> None:
        """Saves video frames.

        Args:
            _mouse_event: Ignored. It is there for compatibility.
        """
        self.check_controller_initialized()
        self.controller.save_video_frames()
        self.ax_img.set_title("Saved!")
        plt.pause(0.001)

    def hotkey_pressed(self, key_event: plt_types.KeyEvent) -> None:
        """Checks what hotkey is pressed and calls mapped function.

        Args:
            key_event: Key event that tracks what key was pressed
        """
        if key_event.key == "t":
            self.toggle_class_button_clicked()
        elif key_event.key == "left":
            self.prev_button_clicked()
        elif key_event.key == "right":
            self.next_button_clicked()

    def check_controller_initialized(self) -> None:
        """Checks controller is initialized, otherwise throws an error.

        Raises:
            AttributeError: Raises if controller is not initialized.
        """
        if self.controller is None:
            raise AttributeError("Controller object not initialized. Something went wrong.")
