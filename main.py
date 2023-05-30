from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
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


def information_wines(file):
    """Сортировка напитков по их категориям."""
    data_about_wines = pandas.read_excel(file, na_values=['N/A', 'NA'], keep_default_na=False).to_dict(
        orient='records')
    sort_by_category = collections.defaultdict(list)

    for value in data_about_wines:
        sort_by_category[value['Категория']].append(value)
    return sort_by_category


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    rendered_page = template.render(
        years=datetime.datetime.now().year - 1920,
        correct_form_year=correct_form(),
        assortment_wine=information_wines('data_wines.xlsx')
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    print(main())
