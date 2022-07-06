from bs4 import BeautifulSoup
import os


def change_big_table_price(filename, data):
    with open(filename, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'lxml')
    items = soup.find_all('li', class_='item')

    for item in items:
        stroka = item.find('span', class_='item-price')
        if stroka is not None:
            price = int(item.find('span', class_='item-price').text.replace(' ', ''))
            line = data['strings'][0]
            new_price = change_price(price, line['work'], line['change_type'], line['value'])
            new_price = '{0:,}'.format(new_price).replace(',', ' ')
            stroka.string = new_price
    with open('proekti.html', 'w', encoding='utf-8') as file:
        file.write(str(soup))


def change_big_price(filename, data):
    with open('new_pages\\' + filename.split('\\')[-1], 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'lxml')
    min_price_page = soup.find(class_='imp_price')
    price = int(min_price_page.text.replace(' ₽\nЗаказать', '').replace('от ', '').replace(' ', ''))
    line = data['strings'][0]
    new_price = change_price(price, line['work'], line['change_type'], line['value'])
    new_price = '{0:,}'.format(new_price).replace(',', ' ')
    min_price_page.string = f'от {new_price}'
    new_div = soup.new_tag("div", **{'class': 'imp_rub'})
    new_a = soup.new_tag("a", **{'class': 'form_order js-form_files'})
    new_a.string = 'Заказать'
    new_div.string = '₽'
    min_price_page.insert(1, new_div)
    min_price_page.insert(2, new_a)
    with open('new_pages\\' + filename.split('\\')[-1], 'w', encoding='utf-8') as file:
        file.write(str(soup))


def change_table_price(filename, data):
    with open(filename, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'lxml')
    table_trs = soup.find_all(attrs={'data-actions': '1'})
    i = 0
    for tr in table_trs:
        j = 0
        for td in tr.find_all('td'):
            if j != 0:
                price = int(td.text.strip().replace(' ', '').replace('₽', ''))
                try:
                    line = data['strings'][i]
                    new_price = change_price(price, line['work'], line['change_type'], line['value'])
                    new_price = '{0:,}'.format(new_price).replace(',', ' ') + ' ₽'

                    td.string = f'{new_price}'
                except IndexError:
                    pass
            else:
                j += 1
        i += 1
    with open('new_pages\\' + filename.split('\\')[-1], 'w', encoding='utf-8') as file:
        print('new_pages\\' + filename.split('\\')[-1])
        file.write(str(soup))


def change_price(old_price, work, change_type, value):
    new_price = int()
    """
    work = increase.decrease.nochange
    change_type = percent.rub
    value = int
    
    change_price(price, 'increase', 'rub', 100000)
    """

    if work == 'nochange':
        new_price = old_price

    elif work == 'increase':
        if change_type == 'rub':
            new_price = old_price + value
        elif change_type == 'percent':
            per = (value * old_price) / 100
            new_price = old_price + per

    elif work == 'decrease':
        if change_type == 'rub':
            new_price = old_price - value
        elif change_type == 'percent':
            per = (value * old_price) / 100
            new_price = old_price - per
    print(f'old price: {old_price}\nnew_price: {new_price} {work}:{change_type}:{value}', )
    return convert_price(new_price)


def convert_price(price):
    import math
    price_last = price % 10000
    if price_last < 2500:
        price_last = (math.floor(price / 5000)) * 5000
    elif price_last < 7500:
        price_last = (math.floor(price / 5000)) * 5000
    else:
        price_last = (math.ceil(price / 5000)) * 5000
    print(price, price_last)
    return price_last





def menu():
    data = {
    }

    path = input("Введите путь до папки: ")
    type = int(input("Введите тип страницы \n1 - много параметров\n2 - 1 параметр\nВвод: "))
    data['path'] = path
    data['type'] = type
    strings = []
    if type == 1:
        numbers = int(input("Введите кол-во строк:"))
        for i in range(numbers):
            action = input(f"Введите действие над строкой {i + 1}: ")
            if action == '-':
                strings.append({"num": i + 1,
                                "work": "nochange",
                                "change_type": "none",
                                "value": 0
                                })
            else:
                work = action.split(' ')[0]
                if work == '+':
                    work = 'increase'
                elif work == '-':
                    work = 'decrease'
                value = int(action.split(' ')[1])
                if len(action.split(' ')) == 3:
                    change_type = 'percent'
                else:
                    change_type = 'rub'
                strings.append({"num": i + 1,
                                "work": work,
                                "change_type": change_type,
                                "value": value
                                })
    elif type == 2:
        action = input(f"Введите действие над строкой: ")
        if action == '-':
            strings.append({"num": 1,
                            "work": "nochange",
                            "change_type": "none",
                            "value": 0
                            })
        else:
            work = action.split(' ')[0]
            value = int(action.split(' ')[1])
            if len(action.split(' ')) == 3:
                change_type = 'percent'
            else:
                change_type = 'rub'
            strings.append({"num": 1,
                            "work": work,
                            "change_type": change_type,
                            "value": value
                            })
    data['strings'] = strings
    return data

def main():
    data = menu()
    path = 'pages'
    html_files = os.listdir(path)
    if os.path.exists('new_pages') is False:
        os.mkdir('new_pages')
    for html_file in html_files:
        if data['type'] == 1:
            change_table_price(path + "\\" + html_file, data)
            change_big_price(path + "\\" + html_file, data)
        elif data['type'] == 2:
            change_big_table_price(path + "\\" + html_file, data)


if __name__ == '__main__':
    main()
