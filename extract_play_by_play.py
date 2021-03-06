# Created by Chaowei Gao
# 2014.3.17
# Used to extract the information from a text live html
from bs4 import BeautifulSoup
from pylab import *
import csv

def extract_play_by_play(filename):
    soup = BeautifulSoup(open(filename))
    html = soup.html
    body = html.body
    table = ''
    for child in body:
        if(child.name == 'div' and child['id'] == 'mantle_skin'):
            for adiv in child:
                try:
                    if(adiv['id'] == 'pageRow'):
                        tmp_divs = adiv.find_all('div')
                        for div in tmp_divs:
                            try:
                                if(div['class'][0] == 'column1'):
                                    for childdiv in div:
                                        if(childdiv.name == 'table'):
                                            table = childdiv
                            except:
                                continue
                except:
                    continue
    
    outfilename = filename.replace('html','csv')
    outfilename = outfilename.replace('text_live_file','play_by_play_file')
    results = open(outfilename,'wb')
    playbyplay_rows = list()
    arow = list()
    period = ''
    for tag in table:
        try:
            if(tag['id'] == 'period'):
                period = tag.string.encode('utf-8','ignore')
            elif(tag['id'] == 'noteam'):
                playbyplay_rows.append(list(arow))
                arow[:] = []
                arow.append(period)
                for noteam_td in tag:
                    try:
                        arow.append(noteam_td.string.encode('utf-8','ignore'))
                    except:
                        arow.append(noteam_td.string.encode('utf-8','ignore'))
        except:
            playbyplay_rows.append(list(arow))
            arow[:] = []
            arow.append(period)
            for play_td in tag:
                try:
                    for a in play_td:
                        arow.append(a.string.replace(',', ';').encode('utf-8','ignore'))
                except:
                    arow.append(play_td.string.replace(',', ';').encode('utf-8','ignore'))
    playbyplay_rows.append(['PERIOD','TIME','SCORE','TEAM','PLAY'])
    playbyplay_rows.reverse()
    for i in xrange(len(playbyplay_rows)):
        for j in xrange(len(playbyplay_rows[i])):
            playbyplay_rows[i][j].replace(',', ';')
            
        if(len(playbyplay_rows[i]) == 0):
            del playbyplay_rows[i]
        elif(playbyplay_rows[i][2] == '\xc2\xa0'):
            playbyplay_rows[i][2] = playbyplay_rows[i-1][2]
            if(playbyplay_rows[i][2] == 'SCORE' ):
                playbyplay_rows[i][2] = '0-0'
        elif(playbyplay_rows[i][2].find('End') == 0 ):
            playbyplay_rows[i].insert(2, playbyplay_rows[i-1][2])
            playbyplay_rows[i].insert(3, '\xc2\xa0')
            
    csv.writer(results).writerows(playbyplay_rows)
    results.close()

    