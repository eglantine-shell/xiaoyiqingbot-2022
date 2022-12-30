# -*-coding:utf-8-*- 
import re
import json
import random
import requests
from bs4 import BeautifulSoup
import sqlite3 as sql
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import sys
sys_type = sys.getfilesystemencoding()

headers = {
        'Cookie': 'ntes_kaola_ad=1; WM_NI=48p6P6zmdXh3XjjcIyLQ8FS7is5o71U4inTUKH%2Bnj4mHKgCwC3OJsxeqwX6EQwG%2BAAi1NhDABgxLDSJk1w8HklPBAcVztknKH220HsK8Q%2BzF8XcqYBhZTQipXPRXddiaaEs%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eea9f9508cebfda7b56d86b08fb6d44a878f8f86d469a38aa5d1e84ba597e5a6b82af0fea7c3b92af8e8c0d7d33ebab3acb9eb399cb6a684cc73908ff8a7d23dabadfb90b63b97eca78fd75f8998e58fe940af988588c27d81ed81abf274a7afb9b9b54f93a989ccc44babef8289c74b82b9b8adc7598ab5ff98bb44a9b4a0a3c46996a6bc8ced418ceefed1cb7989e89fccf94efc88ad92dc4aac869cb2ec7c9c909eb9e770abbfafa6f237e2a3; WM_TID=j7JbJmEZbzlBEUEBEQbAZNYFbXEiZXA7; JSESSIONID-WYYY=kkiKdEFgvfCcRuBV74Ewo0vgt3U5yGw2Efa96CjHZZ9StZFnAOFS55uqIxrhB%2FE35NE%5Ctozwh6st%2FI7UmF79tZRHB2H6xmXWyopHRfjwqO72%2BdY9FW9Hk%2F%2BDBoMAhIOlk5Kfb3I7fV2V%5CG5xie6i%2BkKccEMuVyXkMDoa4FjxHnZABvlO%3A1669746636727; _iuqxldmzr_=32; MUSIC_U=c71238d18343e1c928b081b308cbb30546a3c9787bbc89e87473edf8d00a511d993166e004087dd3bfb19b3641ce47b56a21755aad9610d0dfefbe7d251bd1606b43ddcc51022099a0d2166338885bd7; __csrf=f190e84b955a3e7cefe90911ed8775b3; YD00000558929251%3AWM_NI=aFTh87NI2%2Bk5aN%2Fq%2B64EecsU2feLy3Ilj31jbP7gBMmbejxXH9vLUqLAC32SliyLytktKBSHBAiC8dOM4OOJ7dBPD8c7vt6OwsajeWs0yTko3OxCK2KaOL4nqEQAt85XM1g%3D; YD00000558929251%3AWM_NIKE=9ca17ae2e6ffcda170e2e6eeaaea72a28a84d4b63a8cac8ea6d45f878a9fb0d152a8f5bad0f940f199a6cce72af0fea7c3b92aa39a9c89bb3d8e97feccea3fa392e192aa3ef89bab84f25ff2baabadfc398bb4a6d4b462a290f988c147afbeab8bfb548ce7baadd87b909f8dd4b159b0b7b7adfc80a9ac85a3d244829fa7a4bb708d93fcb0ce42f5bc8eb1c734a1e9ba95b545b5adaf8be85db1f0b7b5ea65f191b8a4ca3a89bf81adb766b39b9fa2f734f78883d2e637e2a3; YD00000558929251%3AWM_TID=P133CscGTHVBBFEUAFOVNNrq6n5jCyqJ; gdxidpyhxdE=TrW0B%5CnrL%2BeNl8ivlGQUM5mZ9BtJMNdzVeDb%5CJoKOZVHt12gRv%2Fk1%2FwT0iekBqOBIPJrYa39vyDYlvp3L6%2BTyQhTtEnM6TrJuDPfgcm7V7YHqpR2M1QfTmG%2F6xg7EImhKAl94mie%2BNccdULLdV2pX1oa%2F2Vz3RIBnHQgIXLhyv%2BvCx9H%3A1669668867387; __snaker__id=MaHSnubhTE2kkRJf; _ntes_nnid=ddb268ee7ee171b8685789e0d34839ae,1669667964072; _ntes_nuid=ddb268ee7ee171b8685789e0d34839ae; NMTID=00OfGdmVxoMw6rQZkQMstJQPIndxy0AAAGEkGRN_w',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Host': 'music.163.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15',
        'Accept-Language': 'zh-TW,zh-Hant;q=0.9',
        'Referer': 'https://www.google.com/'
    }

class DB:

    def __init__(self):
        self.db_name = 'music163.sqlite'
        self.con = sql.connect(self.db_name)
        self.cur = self.con.cursor()

    def createDB(self):
        self.cur.executescript('''
            DROP TABLE IF EXISTS List;
            CREATE TABLE List(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                listID CHAR(15) NOT NULL UNIQUE
            );
            INSERT INTO List (listID) VALUES ('409883996');
            INSERT INTO List (listID) VALUES ('711751040');
            DROP TABLE IF EXISTS Song;
            CREATE TABLE Song(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                songID CHAR(15) NOT NULL UNIQUE, 
                list INTEGER NOT NULL,
                name TEXT
            );
        ''')

    def addSong(self, l):
        #get list id from List Table
        id = self.cur.execute('SELECT ListID FROM List WHERE List.id = ?', (l,)).fetchone()[0]
        #get songs url form lists then insert into table
        ListURL = 'https://music.163.com/playlist?id=' + id
        res = requests.get(url=ListURL, headers=headers).text
        soup = BeautifulSoup(res, 'lxml')
        songs = soup.find('ul',class_="f-hide").find_all('a')
        for song in songs:
            songID = song['href'].replace('/song?id=','')
            name = song.text
            self.cur.execute('INSERT OR IGNORE INTO Song (songID, list, name) VALUES (?, ?, ?)', (songID, id, name))

    def randomSong(self):
        self.songs = self.cur.execute('SELECT * FROM Song').fetchall()
        ran = random.choice(self.songs)
        return ran

    def disconnection(self):
        self.cur.close()

if __name__ == '__main__':
    obj = DB()
    obj.createDB()
    obj.disconnection()
            

    
    
