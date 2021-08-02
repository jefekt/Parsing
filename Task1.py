from bs4 import BeautifulSoup as bs
import requests
import json

search = input('Введите профессию: ')
pages = int(input('Количество страниц для поиска: '))

url = 'https://hh.ru'
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/91.0.4472.135 YaBrowser/21.6.2.855 Yowser/2.5 Safari/537.36"}
vacancy_list = []

for page in range(pages):
    params = {'area': 1, 'fromSearchLine': 'true', 'st': 'searchVacancy', 'text': search, 'page': page - 1}

    response = requests.get(url + '/search/vacancy', params=params, headers=headers)
    html = response.text
    soup = bs(html, 'html.parser')
    vacancy_search_list = soup.find_all('div', attrs={'class': 'vacancy-serp-item'})

    for vacancy in vacancy_search_list:
        vacancy_data = {}
        vacancy_name = vacancy.find('a', attrs={'class': 'bloko-link'}).getText()
        vacancy_wage = vacancy.find("div", {"class": "vacancy-serp-item__sidebar"}).text
        if vacancy_wage is not None:
            if vacancy_wage.find("–") != -1:
                vacancy_wage_min = vacancy_wage.split("–")[0].replace('\u202f', '').strip()
                vacancy_wage_max = vacancy_wage.split("–")[1].replace('\u202f', '').replace('руб.', '').strip()
                vacancy_wage_valute = vacancy_wage.split("–")[1].split()[-1].replace('.', '').strip()
            elif vacancy_wage.find("от") != -1:
                vacancy_wage_min = vacancy_wage.split(' ')[1].replace('\u202f', '')
                vacancy_wage_max = None
                vacancy_wage_valute = vacancy_wage.split(' ')[-1].replace('.', '')
            elif vacancy_wage.find("до") != -1:
                vacancy_wage_min = None
                vacancy_wage_max = vacancy_wage.split(' ')[1].replace('\u202f', '')
                vacancy_wage_valute = vacancy_wage.split(' ')[-1].replace('.', '')
            else:
                vacancy_wage_min = None
                vacancy_wage_max = None
                vacancy_wage_valute = None
        else:
            vacancy_wage_min = None
            vacancy_wage_max = None
            vacancy_wage_valute = None
        vacancy_url = vacancy.find('a', attrs={'class': 'bloko-link'}).get('href')
        vacancy_site = url
        try:
            vacancy_employer = vacancy.find('a', attrs={'class': 'bloko-link bloko-link_secondary'}).getText()
        except AttributeError:
            vacancy_employer = None
        vacancy_employer_site = url + vacancy.find('a', attrs={'class': 'bloko-link bloko-link_secondary'}).get('href')
        vacancy_city = vacancy.find('span', attrs={'class': 'vacancy-serp-item__meta-info'}).getText()

        vacancy_data['name'] = vacancy_name
        vacancy_data['wage_min'] = vacancy_wage_min
        vacancy_data['wage_max'] = vacancy_wage_max
        vacancy_data['wage_value'] = vacancy_wage_valute
        vacancy_data['url'] = vacancy_url
        vacancy_data['employer'] = vacancy_employer
        vacancy_data['employer_site'] = vacancy_employer_site
        vacancy_data['city'] = vacancy_city
        vacancy_data['site'] = vacancy_site

        vacancy_list.append(vacancy_data)

with open('vacancy.json', 'w', encoding='utf-8') as f:
    json.dump({'works': vacancy_list}, f, ensure_ascii=False, indent=4)
