from dash import Dash
from flask import render_template
from markupsafe import Markup


class FlaskDash(Dash):
    def interpolate_index(
        self,
        metas: str = "",
        title: str = "",
        css: str = "",
        config: str = "",
        scripts: str = "",
        app_entry: str = "",
        favicon: str = "",
        renderer: str = "",
    ) -> str:
        # markupsafe.Markup is used to
        # prevent Jinja from
        # escaping the Dash-rendered markup
        return render_template(
            "dash.html",
            metas=Markup(metas),
            css=Markup(css),
            # config is mapped to dash_config
            # to avoid shadowing the global Flask config
            # in the Jinja environment
            dash_config=Markup(config),
            scripts=Markup(scripts),
            app_entry=Markup(app_entry),
            renderer=Markup(renderer),
        )
