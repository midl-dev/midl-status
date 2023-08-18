from flask import Blueprint, Response, current_app, jsonify

# Blueprint Configuration
home_bp = Blueprint(name="home_bp", import_name=__name__)


@home_bp.route(rule="/", methods=["GET"])
def home() -> tuple[Response, int]:
    return (
        jsonify(
            {
                "status": "running",
            }
        ),
        200,
    )


@home_bp.route(rule="/config", methods=["GET"])
def config() -> tuple[Response, int]:
    return (
        jsonify(
            {
                "environment": current_app.config.get("ENV"),
                "debug": current_app.config.get("DEBUG"),
                "clusters": current_app.config.get("MIDL_CLUSTER_INFO"),
                "loki": current_app.config.get("MIDL_LOKI_URL"),
            }
        ),
        200,
    )
