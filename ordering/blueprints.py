def _import_blueprints():
    from .list.routes import episode_list

    blueprints = (
        ('/', episode_list),
    )

    return blueprints


def register_blueprints():
    from . import app

    blueprints = _import_blueprints()

    for url_prefix, blueprint in blueprints:
        app.blueprint(blueprint, url_prefix=url_prefix)
