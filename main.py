from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from environs import Env
import datetime
import pandas
import collections


def decline_word(number=datetime.datetime.now().year):
    """Склонение слова "год" в зависимости от числительного.

    Примеры:
    1 -> год
    2 -> года
    9 -> лет

    """
    if 11 <= number <= 20:
        return 'лет'
    elif number % 10 == 1:
        return 'год'
    elif 2 <= number % 10 <= 4:
        return 'года'
    return 'лет'


def get_data_from_file(filepath):
    """Сортировка напитков по их категориям."""
    drinkables = pandas.read_excel(filepath, na_values=['N/A', 'NA'], keep_default_na=False).to_dict(
        orient='records')
    drinkables_categories = collections.defaultdict(list)

    for drink in drinkables:
        drinkables_categories[drink['Категория']].append(drink)
    return drinkables_categories


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    envir = Env()
    envir.read_env()

    template = env.get_template('template.html')

    creation_year = 1920

    rendered_page = template.render(
        winery_age=datetime.datetime.now().year - creation_year,
        correct_form_year=decline_word(),
        drink_assortment=get_data_from_file(envir("FILE_INFORMATION_WINE"))
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
