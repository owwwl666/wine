from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from environs import Env
import datetime
import pandas
import collections


def correct_form(number=datetime.datetime.now().year):
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


def sort_the_file(file):
    """Сортировка напитков по их категориям."""
    information_about_wines = pandas.read_excel(file, na_values=['N/A', 'NA'], keep_default_na=False).to_dict(
        orient='records')
    sort_by_category = collections.defaultdict(list)

    for information in information_about_wines:
        sort_by_category[information['Категория']].append(information)
    return sort_by_category


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    envir = Env()
    envir.read_env()

    template = env.get_template('template.html')

    age_winery = 1920

    rendered_page = template.render(
        years=datetime.datetime.now().year - age_winery,
        correct_form_year=correct_form(),
        assortment_wine=sort_the_file(envir("FILE_INFORMATION_WINE"))
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    print(main())
