import re
import requests

from bs4 import BeautifulSoup
from datetime import datetime
from operator import itemgetter

from . import app


def get_episode_list(series_soup, series):
    episode_list = []
    season = 0
    wikipedia_url = 'wikipedia' in app.config['SHOW_DICT'][series]['root']

    if wikipedia_url:
        tables = series_soup.find_all('table', class_='wikiepisodetable')
    else:
        tables = series_soup.find_all('table')

    for table in tables:
        if 'series overview' in table.getText().lower():
            continue

        season += 1
        if wikipedia_url:
            table = [
                [j.getText() for j in itemgetter(1, 3, 5, 11)(i.contents)]
                for i in table.find_all(class_='vevent')
            ]
        else:
            table = [
                row.strip().split('\n')
                for row in table.getText().split('\n\n') if row.strip()
            ]

        for row in table:
            if wikipedia_url:
                row[-1] = row[-1].split('(')[0].replace(u'\xa0', ' ').strip()

            episode_name = row[-2].replace('"', '')

            if '[' in episode_name:
                episode_name = episode_name.split('[')[0]

            episode_num = row[-3]
            try:
                date = row[-1]
                reference = re.search(r'\[\d+\]$', row[-1])
                date = date[:reference.start()] if reference else date
                row[-1] = air_date = datetime.strptime(date, '%B %d, %Y')
            except ValueError:
                continue

            if air_date and 'TBA' not in row:
                episode_data = {
                    'series': series,
                    'episode_id': f'S{season:>02}E{episode_num:>02}',
                    'episode_name': episode_name,
                    'air_date': air_date,
                }
                episode_list.append(episode_data)
    return episode_list


def sort_episodes(show_list_set):
    full_list = []

    for show_list in show_list_set:
        full_list.extend(show_list)

    full_list = sorted(full_list, key=lambda episode: episode['air_date'])

    # Fix screening time error caused by network
    # This fix corrects all the list errors.
    if len(full_list) > 80:
        problem_episodes = (full_list[78], full_list[79])

        one_is_arrow = False
        one_is_flash = False

        for episode in problem_episodes:
            one_is_arrow = one_is_arrow or episode['series'].upper() == 'ARROW'
            one_is_flash = one_is_flash or episode['series'].upper() == 'THE FLASH'

        both_are_episode_17 = all(
            episode['episode_id'].endswith('E17') for episode in problem_episodes
        )

        if one_is_arrow and one_is_flash and both_are_episode_17:
            full_list[78], full_list[79] = full_list[79], full_list[78]

    count = 0
    for row in full_list:
        count += 1
        row['row_number'] = count
        row['air_date'] = row['air_date'].strftime('%B %d, %Y')

    return full_list


# @app.cache.memoize(timeout=43200)
def get_url_content(url):
    return requests.get(url).content


def get_full_series_episode_list(excluded_series=None):
    excluded_series = excluded_series or []
    show_list_set = []

    for show in app.config['SHOWS']:
        if show['id'] not in excluded_series:
            show_url = show['root'] + show['url']

            show_html = get_url_content(show_url)

            series_soup = BeautifulSoup(show_html, 'html.parser')
            show_list = get_episode_list(series_soup, show['name'])

            show_list_set.append(show_list)

    return sort_episodes(show_list_set)
