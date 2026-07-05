import shutil
import subprocess
import tempfile
from copy import deepcopy
from pathlib import Path
from typing import Optional, cast

import bs4
from playwright.sync_api import Browser, Playwright, sync_playwright

from logger import get_new_logger
from optimization.nsga3.result import ContainerOptimizationResult, OptimizedContainer
from rendering.util import styles_dict_to_str
from ui.components.placeholder_container import PlaceholderContainer
from ui.container import Container

logger = get_new_logger("rendering.renderer")

# Load HTML template from file
HTML_TEMPLATE_PATH = Path(__file__).parent / "template.html"
HTML_TEMPLATE_STR = HTML_TEMPLATE_PATH.read_text()
HTML_TEMPLATE = bs4.BeautifulSoup(HTML_TEMPLATE_STR, "html.parser")


class HTMLRenderer:
    """
    Singleton class to render Container elements to HTML files, PNG or video.
    Uses playwright to render HTML to image and ffmpeg to create a video from the images.
    """

    _instance: Optional["HTMLRenderer"] = None
    _pw: Playwright
    _browser: Browser

    def __init__(self) -> None:
        # Playwright setup
        self._pw = sync_playwright().start()
        self._browser = self._pw.chromium.launch()
        self._page = self._browser.new_page()

    @classmethod
    def get_instance(cls) -> "HTMLRenderer":
        """
        Returns singleton instance of HTMLRenderer.
        :return: Singleton HTMLRenderer instance
        """
        if cls._instance is None:
            cls._instance = HTMLRenderer()
        return cls._instance

    def screenshot_container(
        self,
        container: Container,
        output_path: Path,
        blueprint_label: Optional[str] = None,
        generation_number: Optional[int] = None,
        containers: Optional[dict[str, Container]] = None,
    ):
        """
        Write a screenshot of a Container to a PNG file to disk.
        Uses Playwright under the hood to render the HTML and take a screenshot.
        Optionally adds a header with the blueprint label and generation number to the screenshot.

        :param container: The Container to render.
        :param blueprint_label: The label of the blueprint being optimized.
        :param generation_number: The current generation number of the optimization process.
        :param output_path: The path to write the PNG file to.
        :param containers: Optional dictionary of containers to render (used for nested/children containers)
        """
        container_html_str = container.to_html_element(containers=containers)
        html_str = self._format_html(
            container.width_px,
            container.height_px,
            container_html_str,
            blueprint_label,
            generation_number,
        )
        self._page.set_content(html_str)
        self._page.locator("main").screenshot(type="png", path=output_path)

    def render_generation_progression_video(
        self,
        root_blueprint_id: str,
        optimized_container_results: dict[str, ContainerOptimizationResult],
        output_video_path: Path,
        ms_per_frame: int = 10,
    ):
        """
        Render a video showing the step by step optimization progression of each generation for each container.
        NOTE: ffmpeg is required in PATH to render the video.

        :param root_blueprint_id: The blueprint ID of the root container.
        :param optimized_container_results: A dict mapping blueprint IDs to their corresponding ContainerOptimizationResult.
        :param output_video_path: The path to write the output video file to.
        :param ms_per_frame: Milliseconds per frame in the output video (determines framerate).
        """
        root_optimization_result = optimized_container_results[root_blueprint_id]
        if root_optimization_result.best_container is None:
            raise ValueError(
                f"Best container for blueprint {root_optimization_result.blueprint.label} is None. This should not happen."
            )
        root_best_container = root_optimization_result.best_container.container

        tmp_dir_location = Path(tempfile.mkdtemp())
        logger.debug(f"Writing individual images to '{tmp_dir_location}'")
        blueprint_id_queue = [root_blueprint_id]
        rendered_containers: dict[str, Container] = {}
        count = 1
        while blueprint_id_queue:
            blueprint_id = blueprint_id_queue.pop(0)
            blueprint_label = optimized_container_results[blueprint_id].blueprint.label
            optimization_result = optimized_container_results[blueprint_id]
            for _, row in optimization_result.df.iterrows():
                gen_best_container = cast(
                    OptimizedContainer, row["best_container"]
                ).container
                output_path = tmp_dir_location / f"{count}.png"
                generation_number = cast(int, row["generation"])

                # If we currently optimize the root blueprint show the current best container
                if blueprint_id == root_blueprint_id:
                    self.screenshot_container(
                        gen_best_container,
                        output_path,
                        blueprint_label,
                        generation_number,
                    )
                else:
                    children_containers = rendered_containers.copy()
                    children_containers[blueprint_id] = gen_best_container
                    self.screenshot_container(
                        root_best_container,
                        output_path,
                        blueprint_label,
                        generation_number,
                        children_containers,
                    )

                count += 1

            if optimization_result.best_container is None:
                raise ValueError(
                    f"Best container for blueprint {blueprint_id} is None. This should not happen."
                )
            best_container = optimization_result.best_container.container
            rendered_containers[blueprint_id] = best_container

            # Add children to the queue
            for element in best_container.elements:
                if isinstance(element, PlaceholderContainer):
                    blueprint_id_queue.append(element.blueprint_id)

        # Check if ffmpeg is installed
        if not shutil.which("ffmpeg"):
            raise RuntimeError(
                "ffmpeg is not installed or not found in PATH. Please install ffmpeg to render the video."
            )

        # Render video using ffmpeg to output path
        ffmpeg_cmd = [
            "ffmpeg",
            "-y",
            "-framerate",
            str(1000 / ms_per_frame),
            "-start_number",
            "1",
            "-i",
            f"{tmp_dir_location}/%d.png",
            "-c:v",
            "libx264",
            "-crf",
            "18",
            "-pix_fmt",
            "yuv420p",
            str(output_video_path),
        ]

        try:
            logger.debug("Running ffmpeg...")
            subprocess.run(
                ffmpeg_cmd,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"ffmpeg command failed with error: {e}. Please check if ffmpeg is installed."
            )

        # Remove tempdir
        logger.debug(f"Removing temporary directory {tmp_dir_location}")
        shutil.rmtree(tmp_dir_location)

    def write_container_to_html(
        self,
        container: Container,
        output_path: Path,
        containers: Optional[dict[str, Container]] = None,
    ):
        """
        Render a Container to an HTML element.
        :param container: The Container to render.
        :param output_path: The path to write the HTML file to.
        :param containers: Optional dictionary of containers to render (used for nested/children containers)
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        container_html_str = container.to_html_element(containers=containers)
        # Set canvas width and height to main element
        formatted_html = self._format_html(
            canvas_width=container.width_px,
            canvas_height=container.height_px,
            container_html_str=container_html_str,
        )
        output_path.write_text(formatted_html)

    def _format_html(
        self,
        canvas_width: float,
        canvas_height: float,
        container_html_str: str,
        blueprint_label: Optional[str] = None,
        generation_number: Optional[int] = None,
    ):
        """
        Format the HTML template with given canvas width, height, and container HTML string.
        Optionally adds a header with the blueprint label and generation number.
        NOTE: Both blueprint_label and generation_number must be provided together or not at all.

        :param canvas_width: Width of the canvas in pixels.
        :param canvas_height: Height of the canvas in pixels.
        :param container_html_str: HTML string of the container to render.
        :param blueprint_label: Optional label of the blueprint being optimized.
        :param generation_number: Optional current generation number of the optimization process.
        :return: Prettified HTML string
        """
        html = deepcopy(HTML_TEMPLATE)
        main_element = html.find("main")
        if main_element is None:
            raise ValueError("HTML template must contain a <main> element.")
        main_element["style"] = f"width: {canvas_width}px;"

        canvas_root_element = html.new_tag("div")
        canvas_root_element["class"] = "canvas-root"
        canvas_root_element["style"] = styles_dict_to_str(
            {
                "width": f"{canvas_width}px",
                "height": f"{canvas_height}px",
                "position": "relative",
            }
        )

        container_html_fragment = bs4.BeautifulSoup(container_html_str, "html.parser")
        for child in container_html_fragment.contents:
            canvas_root_element.append(child)

        main_element.append(canvas_root_element)

        if blueprint_label is not None and generation_number is not None:
            ui_info_wrapper = html.new_tag("div")
            ui_info_wrapper["style"] = styles_dict_to_str(
                {
                    "width": f"{canvas_width}px",
                    "padding": "10px",
                    "text-align": "center",
                    "border-bottom": "3px dashed #000000",
                    "box-sizing": "border-box",
                    "background-color": "#f0f0f0",
                }
            )
            h1 = html.new_tag("h1")
            h1["style"] = "margin: 0px; font-family: Arial;"
            h1.string = blueprint_label

            h2 = html.new_tag("h2")
            h2["style"] = "margin: 0px; font-family: Arial;"
            h2.string = f"Generation: {generation_number}"

            ui_info_wrapper.append(h1)
            ui_info_wrapper.append(h2)
            main_element.insert(0, ui_info_wrapper)

        return html.prettify()
