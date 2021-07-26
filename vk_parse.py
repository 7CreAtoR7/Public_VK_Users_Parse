import requests
import pandas as pd
import seaborn as sns
import matplotlib.pylab as plt
from config import TOKEN


def main():
    group_link = "https://vk.com/charm_wood"  # ссылка на группу,
    # откуда парсим инфу о подписчиках
    # если у пользователя не указана страна проживания или
    # его странциа удалена, данный юзер пропускается
    id_group = group_link.split('/')[-1]

    countries_count = {}  # словарь с названием страны и кол-вом пользователей

    response = requests.get('https://api.vk.com/method/groups.getMembers?',
                            params={
                                'access_token': TOKEN,
                                'v': 5.92,
                                'group_id': id_group,
                                'fields': 'city, country',
                                'count': 1000
                            })
    count = response.json()['response']['count'] // 1000  # количество подписчиков в тысячах
    data = response.json()['response']['items']
    for i in range(1, count + 1):  # парсим подписчиков по одной тысяче
        response = requests.get('https://api.vk.com/method/groups.getMembers?',
                                params={
                                    'access_token': TOKEN,
                                    'v': 5.92,
                                    'group_id': id_group,
                                    'fields': 'city, country',
                                    'offset': i * 1000
                                })
        a = response.json()['response']['items']
        data += a  # общий список участников с городами
    false_list = []
    for i in range(len(data)):
        try:
            country = data[i]["country"]["title"]
            if country in countries_count:
                countries_count[country] += 1  # если у пользователя указан город в профиле, прибавляем
            else:
                countries_count[country] = 1
        except KeyError:
            name = data[i]["id"]
            false_list.append(name)  # список id пользователей, у которых не указан город проживания

    result = {'Страна': [],
              'Пользователи': []}
    for key, value in countries_count.items():
        result['Страна'].append(key)
        result['Пользователи'].append(value)

    df = pd.DataFrame(result)
    print(df)

    # отображение бар-чарт таблицы
    sns.barplot(x='Страна', y='Пользователи', data=df)
    plt.xticks(df.index, df.Страна.str.upper(),
               rotation=25, horizontalalignment='right',
               fontsize=7)

    plt.title('Количество пользователей')
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
