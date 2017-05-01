from sanic.views import HTTPMethodView

from .. import render
from ..utils import get_full_series_episode_list


class Index(HTTPMethodView):
    async def get(self, request, newest_first=None):
        episode_list = get_full_series_episode_list()

        if newest_first == 'newest_first':
            episode_list = episode_list[::-1]

        context = {
            'table_content': episode_list,
        }

        return render('index.html', request, **context)


class IndexWithHiddenSeries(HTTPMethodView):
    async def get(self, request, hide_list, newest_first=None):
        episode_list = get_full_series_episode_list(hide_list)

        if newest_first == 'newest_first':
            episode_list = episode_list[::-1]

        context = {
            'hidden_list': hide_list,
            'table_content': episode_list,
        }

        return render('index.html', request, **context)
