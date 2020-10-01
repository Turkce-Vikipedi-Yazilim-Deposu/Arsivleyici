# -*- coding: utf-8 -*-
# !/usr/bin/python

import re
import socket
import time
from datetime import datetime
import platform

import mavri

wiki = 'tr.wikipedia'
username = 'Arşivleyici'
xx = mavri.login(wiki, username)
title = 'Vikipedi:Kategori_tartışmaları'
version = 'V3.0g'
summary_ek = " (" + username + ", " + version + " running on " + platform.system() + "), ([[Kullanıcı mesaj:Evrifaessa|hata bildir]])"
ignore_list=[]
mpa = dict.fromkeys(range(32))

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
    now = datetime.now()
    content = mavri.content_of_page(wiki, title.decode('UTF-8'))
    regex = r'(?<=Kategori tartışmaları/)[^}]*'

    if content != '':
        pages = re.findall(regex.decode('UTF-8'), content)
        for page in pages:
            pageContent = mavri.content_of_page(wiki, "Vikipedi:Kategori tartışmaları/" + page)
            timestampMonth = monthList[now.month-1]
            preTimestampMonth = monthList[now.month-2]
            timestampYear = now.year
            archivePage = "Vikipedi:Kategori_tartışmaları/Kayıt/" + str(timestampYear) + "_" + str(timestampMonth)
            preArchivePage = "Vikipedi:Kategori_tartışmaları/Kayıt/" + str(timestampYear) + "_" + str(preTimestampMonth)
            contentLow = pageContent.lower()
            resolved = '{{kt-son}}' in contentLow

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
            matches = re.finditer(regex, content2.decode('UTF-8'), re.MULTILINE)

            signatureTimes = []

            for matchNum, match in enumerate(matches, start=1):
                date_time_obj = datetime.strptime(str(match.group()), '%H.%M, %d %B %Y (%Z)')
                signatureTimes.append(date_time_obj)
                
            youngest = max(dt for dt in signatureTimes if dt < now)
            youngestDiff = now - youngest

            archiveContent = mavri.content_of_page(wiki, archivePage.decode('UTF-8'))
            preArchiveContent = mavri.content_of_page(wiki, preArchivePage.decode('UTF-8'))
            hasBeenPreArchived = '{{Vikipedi:Kategori tartışmaları/' + page + '}}' in preArchiveContent
            hasBeenArchived = '{{Vikipedi:Kategori tartışmaları/' + page + '}}' in archiveContent

            if hasBeenArchived == False and hasBeenPreArchived == False:
                append = '\n' + '{{Vikipedi:Kategori tartışmaları/' + page + '}}'
                archiveSummary = 'Arşiv sayfalarında bulunmayan KT alt sayfası arşivlere ekleniyor - ' + summary_ek
                mavri.appendtext_on_page(wiki, archivePage.decode('UTF-8'), append, archiveSummary, xx)
                print(page + ' arşiv sayfasına eklendi.')

            if resolved and youngestDiff.total_seconds() >= 60 * 60 * 12:
                summary = 'Sonuçlandırılan KT arşivleniyor - ' + summary_ek
                print(page + " KT sayfasından kaldırılıyor.")
                newContent = content.replace("{{Vikipedi:Kategori tartışmaları/" + page + "}}", "")
                mavri.change_page(wiki, title, newContent, summary, xx)
    else:
        time.sleep(60)