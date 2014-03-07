#coding=utf-8

from sock import Sock
import sys, os

from DJPostgres import DB

class MusicPipeline(object):
    def __init__(self):
        self.sock = Sock()
        self.db = DB('music', 'postgres', 'dj')
    
    def process_item(self, item, spider):
        if len(self.db.query("""SELECT * FROM songs WHERE title=%s""", (item['title'], ))) == 0:
            self.db.transaction(("""INSERT INTO songs (title, artist) VALUES (%s, %s)""",), ((item['title'],item['artist']),))
            
            msg = item.type + '[*]' + item['title'] + '[*]' + item['download_link'] 
            self.sock.send_msg(msg)

if __name__ == '__main__':
    homepath = '/'.join(os.getcwd().split('/')[0:3])
    print homepath     
