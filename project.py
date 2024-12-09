import glob
import csv
from prettytable import PrettyTable


class PriceMachine:
    
    def __init__(self):
        self.data = []
        self.result = ''
    
    def load_prices(self):
        '''
            Сканирует указанный каталог. Ищет файлы со словом price в названии.
            В файле ищет столбцы с названием товара, ценой и весом.
            Допустимые названия для столбца с товаром:
                товар
                название
                наименование
                продукт

            Допустимые названия для столбца с ценой:
                розница
                цена

            Допустимые названия для столбца с весом (в кг.)
                вес
                масса
                фасовка

            Создает file.csv со всеми товарами из найденных файлов.
        '''

        list_name = ['товар', 'название', "наименование", "продукт"]
        list_price = ['розница', 'цена']
        list_weight = ['вес', 'масса', 'фасовка']

        dict_ = {}

        with open('file.csv', 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['наименование', 'цена', 'вес', 'файл', 'цена за кг'],
                                    delimiter=',')
            writer.writeheader()

        for filename in glob.glob('price*.csv'):

            with open(filename, encoding='utf-8') as f:
                reader = csv.DictReader(f)

                for line in reader:
                    for name in list_name:
                        if name in line:
                            dict_['наименование'] = line[name]

                    for price in list_price:
                        if price in line:
                            dict_['цена'] = line[price]

                    for weight in list_weight:
                        if weight in line:
                            dict_['вес'] = line[weight]

                    dict_['файл'] = filename
                    dict_['цена за кг'] = round(float(dict_['цена']) / float(dict_['вес']), 2)

                    with open('file.csv', 'a', newline='') as file:
                        writer = csv.DictWriter(file, fieldnames=['наименование', 'цена', 'вес', 'файл',
                                                                  'цена за кг'], delimiter=',')
                        writer.writerow(dict_)

    def export_to_html(self, fname='output.html'):
        '''
        Экспортирует результаты поиска в HTML файл.
        '''

        result = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Позиции продуктов</title>
        </head>
        <body>
            <table>
                <tr>
                    <th>Номер</th>
                    <th>Название</th>
                    <th>Цена</th>
                    <th>Фасовка</th>
                    <th>Файл</th>
                    <th>Цена за кг.</th>
                </tr>
        '''

        number = 1
        for line in self.data:
            result += f'<tr>'
            result += f'<td>{number}</td>'
            result += f'<td>{line["наименование"]}</td>'
            result += f'<td>{line["цена"]}</td>'
            result += f'<td>{line["вес"]}</td>'
            result += f'<td>{line["файл"]}</td>'
            result += f'<td>{line["цена за кг"]}</td>'
            result += f'</tr>'
            number += 1
        result += '''
        </table>
        </body>
        </html>
        '''
        with open(fname, 'w') as f:
            f.write(result)

    def find_text(self, text):
        '''
        Находит и отображает текст в таблице.
        '''

        with open('file.csv') as file:
            reader = csv.DictReader(file)
            check_item = 0
            for row in reader:
                if text in row['наименование'].lower():
                    self.data.append(row)
                    check_item = 1

        self.data = sorted(self.data, key=lambda d: d['цена за кг'])

        if check_item == 0:
            print(f'Товар {text} не найден')
        else:
            table = PrettyTable()
            table.field_names = ['№', 'наименование', 'цена', 'вес', 'файл', 'цена за кг']
            number = 1
            for line in self.data:
                table.add_rows([
                    [f"{number}",f"{line['наименование']}", f"{line['цена']}", f"{line['вес']}", f"{line['файл']}", f"{line['цена за кг']}"]
                ])
                number += 1
            print(table.get_string(sortby='№', reversesort=True))
        return self.data


pm = PriceMachine()
pm.load_prices()

while True:
    text = input('Введите название товара:')
    if text == 'exit':
        break
    pm.find_text(text)
    print("Для завершения работы введите 'exit'.")

print(pm.export_to_html())
