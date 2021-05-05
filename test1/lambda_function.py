from bs4 import BeautifulSoup as BSoup
import requests
import json
import re

def lambda_handler(event, context):
    url = event['url']
    #url = 'https://uvmathletics.com/sports/mens-soccer/stats/2019'

    page = requests.get(url)

    bs_obj = BSoup(page.text, 'html.parser')

    rows = bs_obj.find_all('table')[1].find('tbody').find_all('tr')

    stats = []

    print(len(rows))

    for row in rows:
        cells = row.find_all('td')
        name = row.find('th').get_text()

        gsgp = cells[-12].get_text()
        goals = cells[-11].get_text()
        assists = cells[-10].get_text()
        pts = cells[-9].get_text()
        sh = cells[-8].get_text()
        sog = cells[-6].get_text()
        land_area_km = cells[-4].get_text()
        water_area_km = cells[-2].get_text()
        num = cells[0].get_text()
        name2 = name.split()[0] + name.split()[1]

        obj = {'name': name2, 'gsgp': gsgp,
                'goals': goals, 'assists': assists,
                'number': num, 'pts': pts,
                'shots': sh, 'sog': sog,
               'lname': name.split()[0][0:-1], 'imgUrl': ''}
        stats.append(obj)

    urlBase = 'https://hokiesports.com/'
    html = requests.get('https://hokiesports.com/sports/mens-soccer/roster')
    bs = BSoup(html.text, 'html.parser')
    images = bs.findAll('img', {'data-src':re.compile('.jpg')})

    for image in images:
        for stat in stats:
            if(stat['lname'].replace('-', '_') in image['data-src']):
                stat['imgUrl'] = urlBase + image['data-src']

    return {
        'statusCode': 200,
        'body': json.dumps(stats)
    }

