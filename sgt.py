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
title = 'Vikipedi:Sürüm gizleme talepleri'
version = 'V3.0g'
summary_ek = " (" + username + ", " + version + " running on " + platform.system() + "), ([[Kullanıcı mesaj:Evrifaessa|hata bildir]])"
section = 1
ignore_list=[]
mpa = dict.fromkeys(range(32))

while 1:
        now = datetime.now()
        content = mavri.content_of_section(wiki, title, section, xx)

        if content != '':
            timestamp = re.findall('\{\{\s*User:Evrifaessa\/SGT\s*\|\s*([^\|\}]*)\s*\|\s*[^\|\}]*\s*\}\}', content)
            informer = re.findall('\{\{\s*User:Evrifaessa\/SGT\s*\|\s*[^\|\}]*\s*\|\s*([^\|\}]*)\s*\}\}', content)
            if timestamp and informer:
                timestamp = timestamp[0]
                informer = informer[0]
                contentLow = content.lower()
                resolved = "{{yapıldı}}" in contentLow or "{{done}}" in contentLow or "{{yapılmadı}}" in contentLow or "{{yapılmadı2}}" in contentLow or "{{yapılmadı ve yapılmayacak}}" in contentLow 
                pinned = "{{mesaj sabitle}}" in contentLow or "{{pin message}}" in contentLow or "{{mesaj_sabitle}}" in contentLow or "{{pin_message}}" in contentLow
                not_time = datetime(int(timestamp[:4]), int(timestamp[4:6]), int(timestamp[6:8]), int(timestamp[8:10]), int(timestamp[10:12]), int(timestamp[12:14]))
                diff = now - not_time

                content2 = content

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

                if resolved:
                    if diff.total_seconds() > 60 * 60 * 3 and youngestDiff.total_seconds() >= 60 * 15:
                        if pinned == False:
                            summary = 'Sürüm gizleme talebi sonuçlandırılmış - ' + summary_ek
                            mavri.section_clear(wiki, title, section, summary, xx)
                        else:
                            print('Tartışma sabitlenmiş, arşivlenmiyor.')
                    else:
                        print('Talep sonuçlandırılmış ama gereken süre geçmemiş, arşivlenmiyor.')
                else:
                    print('Talep henüz sonuçlandırılmamış, arşivlenmiyor.')
            section += 1
        else:
            section = 1