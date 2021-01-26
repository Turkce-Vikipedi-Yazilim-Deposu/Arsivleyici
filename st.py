# -*- coding: utf-8 -*-
# !/usr/bin/python

import re
import socket
import time
from datetime import datetime
import platform
import pytz

import mavri

wiki = 'tr.wikipedia'
username = 'Arşivleyici'
xx = mavri.login(wiki, username)
title = 'Vikipedi:Şablon tartışmaları'
version = 'V3.0g'
summary_ek = " (" + username + ", " + version + " running on " + \
    platform.system() + "), ([[Kullanıcı mesaj:Evrifaessa|hata bildir]])"
ignore_list = []
mpa = dict.fromkeys(range(32))
utc = pytz.timezone('UTC')
ist = pytz.timezone('Europe/Istanbul')

monthList = [
    'Ocak',
    'Şubat',
    'Mart',
    'Nisan',
    'Mayıs',
    'Haziran',
    'Temmuz',
    'Ağustos',
    'Eylül',
    'Ekim',
    'Kasım',
    'Aralık'
]

while 1:
    now = datetime.now(ist)
    content = mavri.content_of_page(wiki, title)

    regex = r"(?<=Şablon tartışmaları/)[^}]*"

    if content != '{{/Başlık}}' and content != '{{/Başlık}}\n== Tartışmalar ==':
        pages = re.findall(regex.decode('UTF-8'), content)
        for page in pages:
            try:
                pageContent = mavri.content_of_page(wiki, title +"/" + page.decode('UTF-8'))
                timestampMonth = monthList[now.month-1]
                preTimestampMonth = monthList[now.month-2]
                timestampYear = now.year
                archivePage = title +"/Kayıt/" + \
                    str(timestampYear) + "_" + str(timestampMonth)
                preArchivePage = title +"/Kayıt/" + \
                    str(timestampYear) + "_" + str(preTimestampMonth)
                contentLow = pageContent.lower()
                resolved = '{{sas son}}' in contentLow
                pinned = "{{mesaj sabitle" in contentLow or "{{pin message" in contentLow or "{{mesaj_sabitle" in contentLow or "{{pin_message" in contentLow

                content2 = pageContent

                content2 = content2.replace("Ocak", "January")
                content2 = content2.replace("Şubat", "February")
                content2 = content2.replace("Mart", "March")
                content2 = content2.replace("Nisan", "April")
                content2 = content2.replace("Mayıs", "May")
                content2 = content2.replace("Haziran", "June")
                content2 = content2.replace("Temmuz", "July")
                content2 = content2.replace("Ağustos", "August")
                content2 = content2.replace("Eylül", "September")
                content2 = content2.replace("Ekim", "October")
                content2 = content2.replace("Kasım", "November")
                content2 = content2.replace("Aralık", "December")

                regex = r"\d{2}\.\d{2}\,\s\d{1,2}\s\w+\s\d{4}\s\(UTC\)"
                matches = re.finditer(
                    regex, content2.decode('UTF-8'), re.MULTILINE)

                signatureTimes = []

                for matchNum, match in enumerate(matches, start=1):
                    date_time_obj = utc.localize(datetime.strptime(
                        str(match.group()), '%H.%M, %d %B %Y (%Z)'))
                    signatureTimes.append(date_time_obj)

                youngest = max(dt for dt in signatureTimes if dt < now)
                youngestDiff = now - youngest

                archiveContent = mavri.content_of_page(wiki, archivePage.decode('UTF-8'))
                preArchiveContent = mavri.content_of_page(
                    wiki, preArchivePage.decode('UTF-8'))
                hasBeenPreArchived = '{{'+title +"/" + \
                    page + '}}' in preArchiveContent
                hasBeenArchived = '{{title +"/" + \
                    page + '}}' in archiveContent

                if hasBeenArchived == False and hasBeenPreArchived == False:
                    append = '\n' + \
                        '{{'+title +"/" + page + '}}'
                    archiveSummary = 'Arşiv sayfalarında bulunmayan [['+title +"/" + \
                        page + '|SAS alt sayfası]] arşivlere ekleniyor - ' + summary_ek
                    mavri.appendtext_on_page(wiki, archivePage.decode(
                        'UTF-8'), append, archiveSummary, xx)
                    print(page + ' arşiv sayfasına eklendi.')

                if pinned == False:
                    if resolved and youngestDiff.total_seconds() >= 3600:
                        summary = '[['+title +'/' + page + \
                            '|Sonuçlandırılan ST]] arşivleniyor - ' + summary_ek
                        print(page + " ST sayfasından kaldırılıyor.")
                        newContent = content.replace(
                            "{{"+title +'/' + page + "}}", "")
                        newContent = re.sub(
                            r"^[ \t]*$\r?\n", "", newContent, flags=re.MULTILINE)
                        mavri.change_page(wiki, title, newContent, summary, xx)
                else:
                    print(page + ' sabitlenmiş.')
            except ValueError:
                pass
    else:
        time.sleep(60)
