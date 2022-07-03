from bs4 import BeautifulSoup

def change_big_table_price(filename):
    with open('html_pages/proekti.html', 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'lxml')
    items = soup.find_all('li', class_='item')

    for item in items:
        stroka = item.find('span', class_='item-price')
        if stroka is not None:
            price = int(item.find('span', class_='item-price').text.replace(' ', ''))
            new_price = change_price(price, 'increase', 'rub', 100000)
            new_price = '{0:,}'.format(new_price).replace(',', ' ')
            stroka.string = new_price
    with open('proekti.html', 'w', encoding='utf-8') as file:
        file.write(str(soup))

def change_big_price(filename):
    with open('html_pages/list/valeriy-dom-4x6.html', 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'lxml')
    min_price_page = soup.find(class_='imp_price')
    price = int(min_price_page.text.replace(' ₽\nЗаказать', '').replace('от ', '').replace(' ', ''))
    new_price = change_price(price, 'increase', 'rub', price)
    new_price = '{0:,}'.format(new_price).replace(',', ' ')
    min_price_page.string = f'от {new_price}'
    new_div = soup.new_tag("div", **{'class': 'imp_rub'})
    new_a = soup.new_tag("a", **{'class': 'form_order js-form_files'})
    new_a.string = 'Заказать'
    new_div.string = '₽'
    min_price_page.insert(1, new_div)
    min_price_page.insert(2, new_a)
    with open('valeriy-dom-test.html', 'w', encoding='utf-8') as file:
        file.write(str(soup))


def change_table_price(filename):
    with open('html_pages/list/valeriy-dom-4x6.html', 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'lxml')
    table_trs = soup.find_all(attrs={'data-actions': '1'})
    i = 0
    for tr in table_trs:
        j = 0
        for td in tr.find_all('td'):
            if j != 0:
                price = int(td.text.strip().replace(' ', '').replace('₽', ''))
                new_price = change_price(price, 'increase', 'rub', 100000)
                new_price = '{0:,}'.format(new_price).replace(',', ' ') + ' ₽'

                td.string = f'{new_price}'
            else:
                j += 1
        i += 1

    with open('valeriy-dom-test.html', 'w', encoding='utf-8') as file:
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
    else:
        price_last = (math.ceil(price / 5000)) * 5000
    # if price_last < 2500 and price_last < 5000:
    #     price_last = price - price_last
    # elif 2500 < price_last < 5000:
    #     price_last = (math.ceil(price / 5000)) * 5000
    # elif 7500 > price_last > 5000:
    #     price_last = (math.floor(price / 5000)) * 5000
    # elif 7500 < price_last > 5000:
    #     price_last = (math.ceil(price / 5000)) * 5000
    # elif price_last == 5000 or price_last == 0:
    #     price_last = price
    return price_last


def main():
    change_big_table_price('a')


if __name__ == '__main__':
    main()
