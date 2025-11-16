from pathlib import Path
import string
from genetic.ui import UserInterface
from constants import CANVAS_HEIGHT, CANVAS_WIDTH


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
    def ui_to_html(ui: UserInterface, output_path: Path):
        """
        Render the UserInterface to an HTML file.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        ui_elements_html = "".join(
            [element.to_html_element() for element in ui.elements]
        )
        with open(output_path, "w") as f:
            f.write(
                HTML_TEMPLATE.substitute(
                    canvas_height=CANVAS_HEIGHT,
                    canvas_width=CANVAS_WIDTH,
                    ui_elements=ui_elements_html,
                )
            )

    @staticmethod
    def get_styled_element(
        html_element: str, styles_dict: dict, extra_attributes: dict[str, str] = {}
    ) -> str:
        """
        Wrap the given HTML element with a div that applies the given styles.
        """
        styles = ";".join(f"{k}: {v}" for k, v in styles_dict.items())
        extra_attrs = " ".join(f'{k}="{v}"' for k, v in extra_attributes.items())
        return f'<{html_element} style="{styles}" {extra_attrs}></{html_element}>'
