from . import app


def name_to_url(episode_name):
    return episode_name.replace(' ', '_')


def episode_url_filter(episode_name, series):
    root_url = app.config['SHOW_DICT'][series]['root']
    wikipedia_url = 'wikipedia' in root_url
    pilot_episode = episode_name.upper() == 'PILOT'

    name_as_url = name_to_url(episode_name)
    series_as_url = name_to_url(f'({series})')

    if pilot_episode or wikipedia_url:
        name_as_url = f'{name_as_url}_{series_as_url}'

    return f'{root_url}{name_as_url}'
