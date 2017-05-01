from sanic.views import HTTPMethodView

from .. import render


class Index(HTTPMethodView):
    async def get(self, request):
        return render('index.html', request, title='ABC')


# @app.route('/', methods=['GET'])
# @app.route('/<newest_first>', methods=['GET'])
# def index(newest_first=None):
#     context = {}
#
#     episode_list = get_full_series_episode_list()
#
#     if newest_first == 'newest_first':
#         episode_list = episode_list[::-1]
#
#     context['table_content'] = episode_list
#
#     return app.jinja.render_template('index.html', **context)
#
#
# @app.route('/hide/<list:hide_list>/', methods=['GET'])
# @app.route('/hide/<list:hide_list>/<newest_first>', methods=['GET'])
# def index_with_hidden(hide_list, newest_first=None):
#     context = {}
#
#     episode_list = get_full_series_episode_list(hide_list)
#
#     if newest_first == 'newest_first':
#         episode_list = episode_list[::-1]
#
#     context['hidden_list'] = hide_list
#     context['table_content'] = episode_list
#
#     return app.jinja.render_template('index.html', **context)
