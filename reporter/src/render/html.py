from jinja2 import Environment, FileSystemLoader
from ..schema import DailyReport


def render_html(report: DailyReport, template_dir: str) -> str:
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("email_daily.html.j2")
    return template.render(report=report)
