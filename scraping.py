import requests

from bs4 import BeautifulSoup


def scrape_endpoint():
    response = requests.get('https://www.heritage.org/index/ranking')
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


list_levels_freedom = scrape_endpoint().find_all('h3')

categories = list(level_freedom.text for level_freedom in list_levels_freedom)

list_countries = scrape_endpoint().find_all('td', class_='country')

countries = list(country.text for country in list_countries)

list_points = scrape_endpoint().find_all('td', class_='overall')

points = list(point.text for point in list_points)


def float_or_na(value):
    return float(value) if value != 'N/A' else -1


def int_or_na(value):
    return int(value) if value != 'N/A' else 1000


def check_overall_for_each_category(overall: float | str) -> str:
    if 100.0 >= overall >= 80.0:
        return 'Free'

    elif 79.9 >= overall >= 70.0:
        return 'Mostry Free'

    elif 69.9 >= overall >= 60.0:
        return 'Moderately Free'

    elif 59.9 >= overall >= 50.0:
        return 'Mostry Unfree'

    elif 49.9 >= overall >= 0:
        return 'Repressed'

    else:
        return 'Not Ranked'


def retorn_list_by_category(country_list_test):
    matriz = []
    free_list = []
    mostry_free_list = []
    moderately_free_list = []
    mostry_unfree_list = []
    repressed_list = []
    not_ranked_list = []
    for country in country_list_test:
        category_test = check_overall_for_each_category(float_or_na(country['Overall']))

        if category_test == 'Free':
            free_list.append(country)

        elif category_test == 'Mostry Free':
            mostry_free_list.append(country)

        elif category_test == 'Moderately Free':
            moderately_free_list.append(country)

        elif category_test == 'Mostry Unfree':
            mostry_unfree_list.append(country)

        elif category_test == 'Repressed':
            repressed_list.append(country)

        elif category_test == 'Not Ranked':
            not_ranked_list.append(country)

    matriz.append(free_list)
    matriz.append(mostry_free_list)
    matriz.append(moderately_free_list)
    matriz.append(mostry_unfree_list)
    matriz.append(repressed_list)
    matriz.append(not_ranked_list)

    return matriz


def main_method():
    category_list = []
    country_list = []
    rank_list = []
    for category in categories:

        ranks = scrape_endpoint().find_all('td', class_=f'rank {category.lower().replace(" ", "-")}')
        rank_category_list = list(rank.text for rank in ranks)

        for rank in rank_category_list:
            rank_list.append(rank)

    for (rank, country, point) in zip(rank_list, countries, points):
        country_dict = {'Rank': rank,
                        'Country': country,
                        'Overall': point}

        country_list.append(country_dict)

    country_list.sort(key=lambda k: int_or_na(k['Rank']))

    for category, lista in zip(categories, retorn_list_by_category(country_list)):
        category_dict = {f'{category}': lista}

        category_list.append(category_dict)

    print(category_list)
