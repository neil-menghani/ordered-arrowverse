from sanic import Blueprint

from .views import Index, IndexWithHiddenSeries
from ..constants import GET, POST


episode_list = Blueprint(name='list')

episode_list.add_route(
    Index.as_view(),
    uri='/',
    methods=[GET],
)

episode_list.add_route(
    Index.as_view(),
    uri='/<newest_first>',
    methods=[GET],
)

episode_list.add_route(
    IndexWithHiddenSeries.as_view(),
    uri='/hide/<hide_list:(\w+\+?)+>/',
    methods=[GET],
)

episode_list.add_route(
    IndexWithHiddenSeries.as_view(),
    uri='/hide/<hide_list:(\w+\+?)+>/<newest_first>',
    methods=[GET],
)
