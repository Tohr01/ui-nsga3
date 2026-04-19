import string
from pathlib import Path
from typing import Optional

from ui.container import Container

HTML_TEMPLATE = string.Template("""
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <style>
    html {
      margin: 0;
      padding: 0;
      overflow: hidden;
    }
    body {
      margin: 0;
      padding: 0;
      width: 100vw;
      height: 100vh;
      background-color: #f0f0f0;
    }
    body main {
      height: ${canvas_height}px;
      width: ${canvas_width}px;
      position: relative;
      background-color: #ffffff;
    }
    main > * {
      position: absolute;
    }
  </style>
</head>
<body>
  <main>$ui_elements</main>
</body>
</html>
""")


class HTMLRenderer:
    @staticmethod
    def write_container_to_html(
        container: Container,
        output_path: Path,
        containers: Optional[dict[str, Container]] = None,
    ):
        """
        Render a Container to an HTML element.
        """
        # TODO: Todo recursive rendering of nested containers

        output_path.parent.mkdir(parents=True, exist_ok=True)
        container_html_str = container.to_html_element(containers=containers)
        with open(output_path, "w") as f:
            f.write(
                HTML_TEMPLATE.substitute(
                    canvas_height=container.height_px,
                    canvas_width=container.width_px,
                    ui_elements=container_html_str,
                )
            )
