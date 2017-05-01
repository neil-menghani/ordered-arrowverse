from sanic import Sanic
from sanic_jinja2 import SanicJinja2

from .blueprints import register_blueprints


# Initializing Sanic app
app = Sanic(__name__)

# Jinja2 Setup
jinja2 = SanicJinja2()
jinja2.init_app(app)


# Make it easy to get render function in views
def render(template, request, **context):
    context['series_map'] = app.config['SHOW_DICT']
    return jinja2.render(template, request, **context)

# Add template filters
from .filters import episode_url_filter

jinja2.env.filters['episode_url'] = episode_url_filter

# Config
app.config.from_pyfile('settings.py')
app.static(app.config.STATIC_URL, file_or_directory=app.config.STATIC_ROOT)

# Blueprints
register_blueprints()

# Middleware
from .middleware import inject_newest_first, inject_oldest_first_url
