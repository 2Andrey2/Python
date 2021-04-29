
import argparse
import os
import struct

class Sound(object):
    author = ""
    name = ""
    alb_name = ""
    teg = ""
    number = ""


class Ex1(object):
    tracklist = []

    def decoding(self):

        for file in os.listdir(path):
            with open(path+'\\'+file, 'rb') as f:
                f.seek(-128, 2)
                obj = f.read()
                sn = Sound()
                sn.teg, sn.name, sn.author, sn.alb_name, sn.number = struct.unpack('<3s30s30s30s35s', obj)
                self.tracklist.append(sn)
                del sn
        for track in self.tracklist:
            print('[ ' + track.author.decode('windows-1251') + " ]  -  [ " +
                  track.name.decode('windows-1251') + " ]  -  [ " +
                  track.alb_name.decode('windows-1251') + " ]")

parser = argparse.ArgumentParser()
parser.add_argument('-d', type=bool, default=False)
path ="C:\\Users\\Andrey\\Desktop\\Учеба\\питон\\LB4\\music"
objec = Ex1()
objec.decoding()
