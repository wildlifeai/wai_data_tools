"""Controller logic for manual annotation."""
import numpy as np

from wai_data_tools.manual_annotation.model import ManualAnnotationModel
from wai_data_tools.manual_annotation.view import ManualAnnotationView


class ManualAnnotationController:
    """Controller class for manual annotation tool."""

    def __init__(self, model: ManualAnnotationModel, view: ManualAnnotationView) -> None:
        """Initializes controller object.

        Args:
            model: Model object for tool
            view: View object for tool
        """
        self.model = model
        self.view = view
        self.frame_indices = self.model.get_frame_indices()
        self.display_index = 0

    def get_current_frame_index(self) -> int:
        """Gets current frame index.

        Returns:
            Current frame index
        """
        return self.frame_indices[self.display_index]

    def update_index(self, increasing: bool) -> None:
        """Updates current index.

        Args:
            increasing: Should current index be increased?
                        If yes, display index is increased by 1, else decreased by 1
        """
        if increasing:
            self.display_index += 1
        else:
            self.display_index -= 1

        if self.display_index < 0:
            self.display_index = len(self.frame_indices) - 1
        elif self.display_index >= len(self.frame_indices):
            self.display_index = 0

    def get_current_frame_image(self) -> np.ndarray:
        """Gets image array from current frame.

        Returns:
            Image array for current frame
        """
        return self.model.get_frame_image(self.get_current_frame_index())

    def get_current_frame_class(self) -> str:
        """Gets class name from current frame.

        Returns:
            Class name for current frame
        """
        return self.model.get_frame_class(self.get_current_frame_index())

    def toggle_current_frame_class(self) -> None:
        """Toggles class for current frame."""
        self.model.toggle_class(frame_index=self.get_current_frame_index())

    def save_video_frames(self) -> None:
        """Saves video frames."""
        self.model.save_video_frames()
