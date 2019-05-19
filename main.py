# -*- coding: utf-8 -*-

import argparse
import os
import csv
import time

import requests
from pyquery import PyQuery

def save(id, title, rows, lang):
    dir_name = '{}/{}'.format(lang, id)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name + '/audio')

    file_name = '{}/{}.csv'.format(dir_name, title)
    with open(file_name, 'a') as f:
        writer = csv.writer(f)
        for row in rows:
            file_url = row[2]
            file_name = file_url[-8:]
            file_path = '{}/audio/{}'.format(dir_name, file_name)
            with open(file_path, 'wb') as auio_file:
                auio_file.write(requests.get(file_url).content)
            writer.writerow([row[0], row[1], file_name])
            time.sleep(1)


def parse(html, lang=None):
    html = PyQuery(html)
    table = html('table').eq(3)
    id = table('.Stil36').text().split('[')[0]
    title = table('.Stil36').eq(1).text().replace('/', '／')

    table = html('table').eq(6)
    rows = []

    for tr in table('tr'):
        tr = PyQuery(tr)
        chinese = tr('div.Stil35')
        if not chinese.is_('div'):
            continue
        chinese = chinese.text().replace(' ', '')
        foreign_lang = tr('div.Stil45 div').eq(1)('a')
        foreign_lang('div').remove()
        foreign_lang = foreign_lang.text()
        if lang == 'JA':
            foreign_lang = foreign_lang.replace(' ', '')
        audio = tr('audio source').attr('src')
        print(chinese, foreign_lang, audio)
        rows.append([chinese, foreign_lang, audio])


    return id, title, rows

def download(url):
    headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36' }
    html = requests.get(url, headers=headers).text
    # f = open('temp.txt', 'w')
    # f.write(html)
    # f.close()
    # f = open('temp.txt')
    # html = f.read()
    # f.close()
    return html

def page(lang, index):
    url = 'https://www.goethe-verlag.com/book2/ZH/ZH{lang}/ZH{lang}{index}.HTM'.format(lang=lang, index=str(index).zfill(3))
    # print(url)
    html = download(url)
    # print(html)
    id, title, rows = parse(html, lang)
    save(id, title, rows, lang)

def main(lang, start):

    for i in range(start, 103):
         page(lang, i)
         time.sleep(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--lang', default='JA')
    parser.add_argument('-s', '--start', type=int, default=3)

    a = parser.parse_args()
    main(a.lang, a.start)
