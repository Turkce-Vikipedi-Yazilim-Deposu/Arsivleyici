# -*- coding: utf-8 -*-
# !/usr/bin/python
from bs4 import BeautifulSoup
import requests
import mavri

xx = mavri.login('tr.wikipedia', 'Evrifaessa')
RAPOR = '{| class="wikitable sortable"\n|-\n! Sayfa !! Damaging !! Goodfaith'
trwiki = 'https://tr.wikipedia.org'
nextpage = '/wiki/%C3%96zel:BekleyenDe%C4%9Fi%C5%9Fiklikler?limit=50'

counter = 0

while nextpage != 'DONE':
    soup = BeautifulSoup(requests.get(trwiki + nextpage, cookies=xx.cookies).text, 'html.parser')
    try:
        nextpage = soup.findAll("a", {"class": "mw-nextlink"})[0].get('href')
    except:
        nextpage = 'DONE'

    for line in soup.find("div", {"id": "mw-content-text"}).ul.find_all('li'):
        incele = line.find_all('a')[2].get('href')
        title = line.find_all('a')[0].get('title')
        incele_text = requests.get(trwiki + incele, cookies=xx.cookies).text

        if incele_text.find('diff-multi') == -1:
            diff = incele_text.split('<input id="mw-fr-input-oldid" type="hidden" value="')[1].split('"')[0]
            print title.encode('UTF-8')
            # print diff
            damaging = \
                requests.get('http://ores.wmflabs.org/v3/scores/trwiki/' + str(diff) + "/damaging").json()["trwiki"]["scores"][str(diff)][
                    "damaging"]["score"]["probability"][
                    "true"] * 100
            goodfaith = \
                requests.get('http://ores.wmflabs.org/v3/scores/trwiki/' + str(diff) + "/goodfaith").json()["trwiki"]["scores"][str(diff)][
                    "goodfaith"]["score"]["probability"][
                    "true"] * 100
            # print damaging
            # print reverted
            RAPOR += '\n|-\n| [https://tr.wikipedia.org' + incele + ' ' + title + '] || ' + str(damaging).replace('.',
                                                                                                                  ',') + ' || ' + str(
                goodfaith).replace('.', ',')
            if counter % 10 == 0:
                print mavri.change_page('tr.wikipedia', 'Kullanıcı:Evrifaessa/ORES', RAPOR, 'ORES raporu yazılıyor', xx).text
            counter += 1
RAPOR += '\n|}'

exit(0)