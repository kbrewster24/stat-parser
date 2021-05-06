import json

import requests
from bs4 import BeautifulSoup as BSoup
from pymongo import MongoClient as Mongo
from test2 import creds




def parseForUrl(url, document):
    #url = event['url']
    #url = 'https://www.umbcretrievers.com/sports/msoc/2019-20/teams/umbc?view=lineup&r=0&pos=kickers'

    page = requests.get(url, headers={'User-Agent': 'Custom'})


    bs_obj = BSoup(page.text, 'html.parser')

    tables = bs_obj.find_all('table')

    #for table in tables:
    #print(tables[3])

    rows = tables[1].find_all('tr')

    # count = 0
    # for table in tables:
    #     print(f'table {count}')
    #     print(table)


    stats = []
    schoolsStats = db.teamStatsStorage

    #print(len(rows))

    for row in rows:
        cells = row.find_all('td')
        name = row.find('th').get_text()
        #print(len(cells))

        if(len(cells) <= 0):
            continue


        minsPlayed = cells[-12].get_text()
        goals = cells[-11].get_text()
        assists = cells[-10].get_text()
        pts = cells[-9].get_text()
        sh = cells[-8].get_text()
        sog = cells[-6].get_text()
        land_area_km = cells[-4].get_text()
        water_area_km = cells[-2].get_text()
        num = cells[0].get_text()
        #name2 = name.split()[0] + name.split()[1]

        obj = {'name': name,
                'mins': minsPlayed,
                'goals': goals, 'assists': assists,
                'number': num, 'pts': pts,
                'shots': sh, 'sog': sog,
                 'imgUrl': ''}
        stats.append(obj)

    #print(stats)
    # urlBase = 'https://hokiesports.com/'
    # html = requests.get('https://hokiesports.com/sports/mens-soccer/roster')
    # bs = BSoup(html.text, 'html.parser')
    # #print(bs)
    # images = bs.findAll('img', {'data-src':re.compile('.jpg')})
    # #print(len(images))
    # # images = [x['src'] for x in bs.find_all('img', {'class': 'lazyload'})]
    # for image in images:
    #     for stat in stats:
    #         #print(stat['lname'] + " "  + image['data-src'])
    #         if(stat['lname'].replace('-', '_') in image['data-src']):
    #             #print(urlBase + image['data-src'] + " " + stat['lname'])
    #             #download_imag = url
    #             stat['imgUrl'] = urlBase + image['data-src']
    print(len(stats))
    print(json.dumps(stats))


    teamStatForInsert = {"team": document['name'], "stats": stats}

    schoolsStats.update_one({"team": document["name"]}, {"$set":teamStatForInsert}, upsert=True)

client = Mongo(f'mongodb+srv://{creds.username}:{creds.password}@cluster0.vgnup.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = client.test
# client = Mongo()
# client

db = client["myLinkStorage"]
schools = db.myLinkStorageSchools


for doc in schools.find():
    print(doc["name"])
    if(doc["name"] != "UMBC"):
        parseForUrl(doc["stats"], doc)
