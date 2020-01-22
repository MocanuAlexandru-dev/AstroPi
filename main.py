import logging
import logzero
import reverse_geocoder as rg
from logzero import logger
from sense_hat import SenseHat
import datetime
import os
from time import sleep
import threading
import ephem
import pprint
import math
import io

class Astro_Pi():
    """Class for every function used in experiment (a way to order the code)"""

    def __init__(self, running_time):
        """When the class obj is created create the class variables
            @param1: int
        """
        R=[255,0,0]#Red
        W=[255,255,255]#White
        B=[0,0,255]#Blue
        Y=[255,247,0]#Yellow
        BL=[0,0,0]#Black
        G=[0,255,0]#Green
        L=[24,166,255]#Light blue
        O=[255,145,0]#Orange
        DG=[131,84,40]#Dark Green
        GO=[153,101,21]#Gold
        DB=[0,41,98]#Dark Blue
        DR=[142,4,4]#Dark Red
        BR=[128,0,0]#Brown
        #Flags dict
        self.flags={"GB":[W,B,B,R,R,B,B,W,B,W,B,R,R,B,W,B,B,B,W,R,R,W,B,B,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,B,B,W,R,R,W,B,B,B,W,B,R,R,B,W,B,W,B,B,R,R,B,B,W],"FR":[B,B,B,W,W,R,R,R,B,B,B,W,W,R,R,R,B,B,B,W,W,R,R,R,B,B,B,W,W,R,R,R,B,B,B,W,W,R,R,R,B,B,B,W,W,R,R,R,B,B,B,W,W,R,R,R,B,B,B,W,W,R,R,R],"DE":[BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,],"ES":[R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,Y,Y,Y,Y,Y,Y,Y,Y,Y,BL,BL,Y,Y,Y,Y,Y,Y,BL,BL,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R],"AT":[R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,],"CH":[R,R,R,W,W,R,R,R,R,R,R,W,W,R,R,R,R,R,R,W,W,R,R,R,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,R,R,R,W,W,R,R,R,R,R,R,W,W,R,R,R,R,R,R,W,W,R,R,R,],"RO":[B,B,B,Y,Y,R,R,R,B,B,B,Y,Y,R,R,R,B,B,B,Y,Y,R,R,R,B,B,B,Y,Y,R,R,R,B,B,B,Y,Y,R,R,R,B,B,B,Y,Y,R,R,R,B,B,B,Y,Y,R,R,R,B,B,B,Y,Y,R,R,R,],"SK":[W,W,W,W,W,W,W,W,W,R,R,R,W,W,W,W,W,R,W,R,W,W,W,W,B,W,W,W,B,B,B,B,B,R,B,R,B,B,B,B,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,],"PL":[W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,],"BY":[W,R,R,R,R,R,R,R,R,W,R,R,R,R,R,R,W,R,R,R,R,R,R,R,R,W,R,R,R,R,R,R,W,R,R,R,R,R,R,R,R,W,G,G,G,G,G,G,W,R,G,G,G,G,G,G,R,W,G,G,G,G,G,G,],"GR":[B,W,B,W,W,W,W,W,W,W,W,B,B,B,B,B,B,W,B,W,W,W,W,W,B,B,B,B,B,B,B,B,W,W,W,W,W,W,W,W,B,B,B,B,B,B,B,B,W,W,W,W,W,W,W,W,B,B,B,B,B,B,B,B,],"IT":[G,G,G,W,W,R,R,R,G,G,G,W,W,R,R,R,G,G,G,W,W,R,R,R,G,G,G,W,W,R,R,R,G,G,G,W,W,R,R,R,G,G,G,W,W,R,R,R,G,G,G,W,W,R,R,R,G,G,G,W,W,R,R,R],"HR":[R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,W,W,W,W,W,W,W,W,W,W,W,R,R,W,W,W,W,W,W,W,W,W,W,W,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,],"HU":[R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,],"UA":[B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y],"TR":[R,R,R,R,R,R,R,R,R,R,W,W,R,R,R,R,R,W,R,R,R,W,R,R,R,W,R,R,W,W,W,R,R,W,R,R,R,W,R,R,R,R,W,W,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R],"RU":[W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R],"SA":[G,G,G,G,G,G,G,G,G,W,G,W,W,W,G,G,G,W,W,W,W,W,W,G,G,W,W,W,G,G,G,G,G,G,G,G,G,W,G,G,G,W,W,W,W,W,W,G,G,G,G,G,G,W,G,G,G,G,G,G,G,G,G,G,],"YE":[R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,],"IQ":[R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,W,W,W,W,W,W,W,W,W,G,W,W,G,G,W,W,W,W,G,W,W,W,G,W,W,W,W,W,W,W,W,W,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,],"IR":[G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,W,W,W,W,W,W,W,W,W,W,W,R,R,W,W,W,W,W,W,R,R,W,W,W,W,W,W,W,W,W,W,W,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,],"TM":[G,R,G,R,G,W,G,G,G,R,Y,R,G,G,W,G,G,R,R,R,G,G,W,G,G,R,G,R,G,W,G,G,G,R,Y,R,G,G,G,G,G,R,R,R,G,G,G,G,G,R,G,R,G,G,G,G,G,R,Y,R,G,G,G,G],"AF":[BL,BL,BL,R,R,G,G,G,BL,BL,BL,R,R,G,G,G,BL,BL,BL,W,W,G,G,G,BL,BL,W,W,W,W,G,G,BL,BL,W,W,W,W,G,G,BL,BL,BL,W,W,G,G,G,BL,BL,BL,R,R,G,G,G,BL,BL,BL,R,R,G,G,G,],"KZ":[L,Y,L,L,L,L,L,L,L,Y,L,L,L,L,L,L,L,Y,L,L,Y,Y,L,L,L,Y,L,Y,Y,Y,Y,L,L,Y,L,Y,Y,Y,Y,L,L,Y,L,L,Y,Y,L,L,L,Y,L,L,L,L,L,L,L,Y,L,L,L,L,L,L,],"MN":[R,R,R,B,B,R,R,R,R,Y,R,B,B,R,R,R,R,R,R,B,B,R,R,R,R,Y,R,B,B,R,R,R,R,Y,R,B,B,R,R,R,R,Y,R,B,B,R,R,R,R,Y,R,B,B,R,R,R,R,R,R,B,B,R,R,R,],"CN":[R,R,R,Y,R,R,R,R,R,Y,Y,R,Y,R,R,R,R,Y,Y,R,Y,R,R,R,R,R,R,Y,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,],"MY":[B,B,Y,B,B,R,R,R,B,Y,B,Y,B,W,W,W,B,Y,B,B,B,R,R,R,B,B,Y,B,B,W,W,W,R,R,R,R,R,R,R,R,W,W,W,W,W,W,W,W,R,R,R,R,R,R,R,R,W,W,W,W,W,W,W,W,],"PG":[BL,R,R,R,R,R,R,R,BL,BL,R,R,Y,Y,Y,R,BL,W,BL,R,R,Y,Y,R,BL,BL,BL,BL,R,R,R,R,BL,W,W,BL,BL,R,R,R,BL,BL,BL,BL,BL,BL,R,R,BL,BL,W,BL,BL,BL,BL,R,BL,BL,BL,BL,BL,BL,BL,BL,],"AU":[B,B,R,B,B,B,B,B,B,B,R,B,B,B,W,B,R,R,R,R,R,B,B,W,B,B,R,B,B,W,B,B,B,B,R,B,B,B,B,W,B,B,B,B,B,B,W,B,B,B,W,B,B,B,B,B,B,B,B,B,B,B,B,B,],"KR":[W,W,BL,W,W,BL,W,W,W,BL,W,W,W,W,BL,W,BL,W,W,W,W,W,W,BL,W,W,W,R,R,W,W,W,W,W,W,B,B,W,W,W,BL,W,W,W,W,W,W,BL,W,BL,W,W,W,W,BL,W,W,W,BL,W,W,BL,W,W,],"JP":[W,W,W,W,W,W,W,W,W,W,W,R,R,W,W,W,W,W,R,R,R,R,W,W,W,R,R,R,R,R,R,W,W,R,R,R,R,R,R,W,W,W,R,R,R,R,W,W,W,W,W,R,R,W,W,W,W,W,W,W,W,W,W,W],"TH":[R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,W,W,W,W,W,W,W,W,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,W,W,W,W,W,W,W,W,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,],"ID":[R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,],"IN":[O,O,O,O,O,O,O,O,O,O,O,O,O,O,O,O,W,W,W,W,W,W,W,W,W,W,W,B,B,W,W,W,W,W,W,B,B,W,W,W,W,W,W,W,W,W,W,W,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,],"PK":[W,W,DG,DG,DG,DG,DG,DG,W,W,DG,DG,W,DG,DG,DG,W,W,DG,W,DG,DG,W,DG,W,W,DG,W,DG,DG,DG,DG,W,W,DG,W,DG,DG,W,DG,W,W,DG,DG,W,W,DG,DG,W,W,DG,DG,DG,DG,DG,DG,W,W,DG,DG,DG,DG,DG,DG,],"NA":[B,B,B,B,B,W,R,R,B,Y,B,B,W,R,R,W,B,B,B,W,R,R,W,G,B,B,W,R,R,W,G,G,B,W,R,R,W,G,G,G,W,R,R,W,G,G,G,G,R,R,W,G,G,G,G,G,R,W,G,G,G,G,G,G,],"AO":[R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,Y,Y,R,R,R,R,R,R,R,R,Y,R,R,R,BL,BL,BL,Y,Y,BL,BL,BL,BL,BL,Y,Y,Y,BL,BL,BL,BL,BL,BL,BL,BL,Y,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,],"CD":[B,B,B,B,B,Y,R,R,B,Y,B,B,Y,R,R,Y,B,B,B,Y,R,R,Y,B,B,B,Y,R,R,Y,B,B,B,Y,R,R,Y,B,B,B,Y,R,R,Y,B,B,B,B,R,R,Y,B,B,B,B,B,R,Y,B,B,B,B,B,B,],"SS":[B,BL,BL,BL,BL,BL,BL,BL,B,B,BL,BL,BL,BL,BL,BL,B,B,B,W,W,W,W,W,B,Y,Y,B,R,R,R,R,B,Y,Y,B,R,R,R,R,B,B,B,W,W,W,W,W,B,B,G,G,G,G,G,G,B,G,G,G,G,G,G,G,],"SD":[G,R,R,R,R,R,R,R,G,G,R,R,R,R,R,R,G,G,G,R,R,R,R,R,G,G,G,G,W,W,W,W,G,G,G,G,W,W,W,W,G,G,G,BL,BL,BL,BL,BL,G,G,BL,BL,BL,BL,BL,BL,G,BL,BL,BL,BL,BL,BL,BL,],"GN":[R,R,R,Y,Y,G,G,G,R,R,R,Y,Y,G,G,G,R,R,R,Y,Y,G,G,G,R,R,R,Y,Y,G,G,G,R,R,R,Y,Y,G,G,G,R,R,R,Y,Y,G,G,G,R,R,R,Y,Y,G,G,G,R,R,R,Y,Y,G,G,G,],"ZA":[G,G,W,R,R,R,R,R,Y,G,G,W,R,R,R,R,BL,Y,G,G,W,W,W,W,BL,BL,Y,G,G,G,G,G,BL,BL,Y,G,G,G,G,G,BL,Y,G,G,W,W,W,W,Y,G,G,W,B,B,B,B,G,G,W,B,B,B,B,B,],"ET":[G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,B,B,G,G,G,Y,Y,B,Y,Y,B,Y,Y,Y,Y,B,Y,Y,B,Y,Y,R,R,R,B,B,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,],"NG":[G,G,G,W,W,G,G,G,G,G,G,W,W,G,G,G,G,G,G,W,W,G,G,G,G,G,G,W,W,G,G,G,G,G,G,W,W,G,G,G,G,G,G,W,W,G,G,G,G,G,G,W,W,G,G,G,G,G,G,W,W,G,G,G,],"NL":[O,O,O,O,O,O,O,O,O,O,O,O,O,O,O,O,W,W,W,W,W,W,W,W,W,W,W,O,O,W,W,W,W,W,W,O,O,W,W,W,W,W,W,W,W,W,W,W,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,],"TD":[B,B,B,Y,Y,R,R,R,B,B,B,Y,Y,R,R,R,B,B,B,Y,Y,R,R,R,B,B,B,Y,Y,R,R,R,B,B,B,Y,Y,R,R,R,B,B,B,Y,Y,R,R,R,B,B,B,Y,Y,R,R,R,B,B,B,Y,Y,R,R,R,],"LY":[R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,BL,BL,W,W,BL,BL,BL,BL,BL,W,BL,BL,BL,W,W,BL,BL,W,BL,BL,BL,W,W,BL,BL,BL,W,W,BL,BL,BL,BL,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,],"ML":[G,G,G,Y,Y,R,R,R,G,G,G,Y,Y,R,R,R,G,G,G,Y,Y,R,R,R,G,G,G,Y,Y,R,R,R,G,G,G,Y,Y,R,R,R,G,G,G,Y,Y,R,R,R,G,G,G,Y,Y,R,R,R,G,G,G,Y,Y,R,R,R,],"MR":[R,R,R,R,R,R,R,R,G,G,G,Y,Y,G,G,G,G,G,G,G,G,G,G,G,G,G,Y,G,G,Y,G,G,G,G,Y,G,G,Y,G,G,G,G,G,Y,Y,G,G,G,G,G,G,G,G,G,G,G,R,R,R,R,R,R,R,R,],"DZ":[G,G,G,G,W,W,W,W,G,G,G,G,W,W,W,W,G,G,G,R,R,W,W,W,G,G,R,G,W,W,R,W,G,G,R,G,W,W,R,W,G,G,G,R,R,W,W,W,G,G,G,G,W,W,W,W,G,G,G,G,W,W,W,W,],"EG":[R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,W,W,W,W,W,W,W,W,W,W,W,Y,Y,W,W,W,W,W,W,Y,Y,W,W,W,W,W,W,W,W,W,W,W,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,],"US":[W,B,W,B,W,R,R,R,B,W,B,W,B,W,W,W,W,B,W,B,W,R,R,R,B,W,B,W,B,W,W,W,R,R,R,R,R,R,R,R,W,W,W,W,W,W,W,W,R,R,R,R,R,R,R,R,W,W,W,W,W,W,W,W,],"CA":[R,W,W,W,W,W,W,R,R,W,W,W,W,W,W,R,R,W,W,R,R,W,W,R,R,W,R,R,R,R,W,R,R,W,W,R,R,W,W,R,R,W,W,R,R,W,W,R,R,W,W,W,W,W,W,R,R,W,W,W,W,W,W,R,],"BR":[G,G,G,Y,Y,G,G,G,G,G,Y,B,B,Y,G,G,G,Y,B,B,B,B,Y,G,Y,B,B,B,B,B,B,Y,Y,B,B,B,B,B,B,Y,G,Y,B,B,B,B,Y,G,G,G,Y,B,B,Y,G,G,G,G,G,Y,Y,G,G,G,],"BO":[R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,],"VE":[Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,B,B,W,W,W,W,B,B,B,W,B,B,B,B,W,B,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,],"AR":[B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,W,W,W,W,W,W,W,W,W,W,W,Y,Y,W,W,W,W,W,W,Y,Y,W,W,W,W,W,W,W,W,W,W,W,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,],"UY":[W,Y,W,B,B,B,B,B,Y,Y,Y,W,W,W,W,W,W,Y,W,B,B,B,B,B,W,W,W,W,W,W,W,W,B,B,B,B,B,B,B,B,W,W,W,W,W,W,W,W,B,B,B,B,B,B,B,B,W,W,W,W,W,W,W,W,],"UZ":[L,L,W,L,L,W,L,W,L,W,L,L,W,L,W,L,L,L,W,L,L,L,L,L,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,],"VN":[R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,Y,Y,R,R,R,R,R,Y,Y,Y,Y,R,R,R,R,R,Y,Y,R,R,R,R,R,Y,R,R,Y,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,],"ZM":[DG,DG,DG,DG,DG,DG,DG,DG,DG,DG,DG,DG,DG,O,DG,O,DG,DG,DG,DG,DG,DG,O,DG,DG,DG,DG,DG,DG,DG,DG,DG,DG,DG,DG,DG,DG,R,BL,O,DG,DG,DG,DG,DG,R,BL,O,DG,DG,DG,DG,DG,R,BL,O,DG,DG,DG,DG,DG,R,BL,O,],"ZW":[W,G,G,G,G,G,G,G,W,W,Y,Y,Y,Y,Y,Y,W,W,W,R,R,R,R,R,W,Y,W,W,BL,BL,BL,BL,W,Y,W,W,BL,BL,BL,BL,W,W,W,R,R,R,R,R,W,W,Y,Y,Y,Y,Y,Y,W,G,G,G,G,G,G,G,],"CU":[R,B,B,B,B,B,B,B,R,R,W,W,W,W,W,W,R,R,R,W,W,W,W,W,R,W,R,R,B,B,B,B,R,W,R,R,B,B,B,B,R,R,R,W,W,W,W,W,R,R,W,W,W,W,W,W,R,B,B,B,B,B,B,B,],"CZ":[B,W,W,W,W,W,W,W,B,B,W,W,W,W,W,W,B,B,B,W,W,W,W,W,B,B,B,B,W,W,W,W,B,B,B,B,R,R,R,R,B,B,B,R,R,R,R,R,B,B,R,R,R,R,R,R,B,R,R,R,R,R,R,R,],"KP":[B,B,B,B,B,B,B,B,W,W,W,W,W,W,W,W,R,R,W,W,R,R,R,R,R,W,R,R,W,R,R,R,R,W,R,R,W,R,R,R,R,R,W,W,R,R,R,R,W,W,W,W,W,W,W,W,B,B,B,B,B,B,B,B,],"PT":[G,G,G,R,R,R,R,R,G,G,G,R,R,R,R,R,G,G,Y,Y,R,R,R,R,G,Y,W,W,Y,R,R,R,G,Y,W,W,Y,R,R,R,G,G,Y,Y,R,R,R,R,G,G,G,R,R,R,R,R,G,G,G,R,R,R,R,R,],"PY":[R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,W,W,W,W,W,W,W,W,W,W,G,Y,Y,G,W,W,W,W,G,Y,Y,G,W,W,W,W,W,G,G,W,W,W,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,],"RS":[R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,Y,Y,Y,R,R,R,B,R,O,W,O,R,B,B,B,R,W,W,W,R,B,B,W,W,R,W,R,W,W,W,W,W,W,R,W,W,W,W,W,W,W,W,W,W,W,W,],"SE":[B,B,Y,Y,B,B,B,B,B,B,Y,Y,B,B,B,B,B,B,Y,Y,B,B,B,B,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,B,B,Y,Y,B,B,B,B,B,B,Y,Y,B,B,B,B,B,B,Y,Y,B,B,B,B,],"SL":[G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,],"SN":[DG,DG,Y,Y,Y,Y,R,R,DG,DG,Y,Y,Y,Y,R,R,DG,DG,Y,Y,Y,Y,R,R,DG,DG,Y,DG,DG,Y,R,R,DG,DG,Y,DG,DG,Y,R,R,DG,DG,Y,Y,Y,Y,R,R,DG,DG,Y,Y,Y,Y,R,R,DG,DG,Y,Y,Y,Y,R,R,],"SO":[L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,W,W,L,L,L,L,L,W,W,W,W,L,L,L,L,L,W,W,L,L,L,L,L,W,L,L,W,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,],"SR":[G,G,G,G,G,G,G,G,W,W,W,W,W,W,W,W,R,R,R,R,R,R,R,R,R,R,R,Y,Y,R,R,R,R,R,R,Y,Y,R,R,R,R,R,R,R,R,R,R,R,W,W,W,W,W,W,W,W,G,G,G,G,G,G,G,G,],"SY":[R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,W,W,W,W,W,W,W,W,W,DG,DG,W,W,DG,DG,W,W,DG,DG,W,W,DG,DG,W,W,W,W,W,W,W,W,W,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,],"MM":[Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,W,W,Y,Y,Y,Y,Y,W,W,W,W,Y,Y,G,G,G,W,W,G,G,G,G,G,G,W,W,G,G,G,R,R,W,R,R,W,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,],"NI":[B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,W,W,W,W,W,W,W,W,W,W,W,Y,Y,W,W,W,W,W,Y,Y,Y,Y,W,W,W,W,W,W,W,W,W,W,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,],"NE":[R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,],"MX":[DG,DG,W,W,W,W,DG,DG,DG,DG,W,W,W,W,DG,DG,DG,DG,W,BR,W,BR,DG,DG,DG,DG,W,W,BR,W,DG,DG,DG,DG,W,W,BR,BR,DG,DG,DG,DG,W,W,O,W,DG,DG,DG,DG,W,W,W,W,DG,DG,DG,DG,W,W,W,W,DG,DG,],"MZ":[DR,DG,DG,DG,DG,DG,DG,DG,DR,DR,DG,DG,DG,DG,DG,DG,DR,DR,DR,W,W,W,W,W,DR,Y,Y,DR,BL,BL,BL,BL,DR,Y,Y,DR,BL,BL,BL,BL,DR,DR,DR,W,W,W,W,W,DR,DR,DG,DG,DG,DG,DG,DG,DR,DG,DG,DG,DG,DG,DG,DG,],"AD":[B,B,B,Y,Y,R,R,R,B,B,B,Y,Y,R,R,R,B,B,B,Y,Y,R,R,R,B,B,B,GO,GO,R,R,R,B,B,B,GO,GO,R,R,R,B,B,B,Y,Y,R,R,R,B,B,B,Y,Y,R,R,R,B,B,B,Y,Y,R,R,R,],"AE":[R,R,G,DG,DG,DG,DG,DG,R,R,DG,DG,DG,DG,DG,DG,R,R,DG,DG,DG,DG,DG,DG,R,R,W,W,W,W,W,W,R,R,W,W,W,W,W,W,R,R,BL,BL,BL,BL,BL,BL,R,R,BL,BL,BL,BL,BL,BL,R,R,BL,BL,BL,BL,BL,BL,],"AL":[R,R,R,R,R,R,R,R,R,R,BL,R,R,BL,R,R,R,BL,R,BL,BL,R,BL,R,R,R,BL,BL,BL,BL,R,R,R,R,R,BL,BL,R,R,R,R,R,BL,BL,BL,BL,R,R,R,R,R,BL,BL,R,R,R,R,R,R,R,R,R,R,R,],"AM":[R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,GO,GO,GO,GO,GO,GO,GO,GO,GO,GO,GO,GO,GO,GO,GO,GO,GO,GO,GO,GO,GO,GO,GO,GO,],"AZ":[L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,R,R,W,W,R,R,R,R,R,W,R,R,R,W,W,R,R,W,R,R,R,W,W,R,R,R,W,W,R,R,R,R,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,],"BA":[B,W,GO,GO,GO,GO,GO,B,B,W,GO,GO,GO,GO,GO,B,B,B,W,GO,GO,GO,GO,B,B,B,W,GO,GO,GO,GO,B,B,B,B,W,GO,GO,GO,B,B,B,B,B,W,GO,GO,B,B,B,B,B,W,GO,GO,B,B,B,B,B,B,W,GO,B,],"BD":[DG,DG,DG,DG,DG,DG,DG,DG,DG,DG,DG,R,R,DG,DG,DG,DG,DG,R,R,R,R,DG,DG,DG,R,R,R,R,R,R,DG,DG,R,R,R,R,R,R,DG,DG,DG,R,R,R,R,DG,DG,DG,DG,DG,R,R,DG,DG,DG,DG,DG,DG,DG,DG,DG,DG,DG,],"BE":[BL,BL,BL,Y,Y,R,R,R,BL,BL,BL,Y,Y,R,R,R,BL,BL,BL,Y,Y,R,R,R,BL,BL,BL,Y,Y,R,R,R,BL,BL,BL,Y,Y,R,R,R,BL,BL,BL,Y,Y,R,R,R,BL,BL,BL,Y,Y,R,R,R,BL,BL,BL,Y,Y,R,R,R,],"BF":[R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,Y,Y,R,R,R,G,G,G,Y,Y,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,],"BG":[W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,DG,DG,DG,DG,DG,DG,DG,DG,DG,DG,DG,DG,DG,DG,DG,DG,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,],"BH":[W,W,W,R,R,R,R,R,W,W,R,R,R,R,R,R,W,W,W,R,R,R,R,R,W,W,R,R,R,R,R,R,W,W,W,R,R,R,R,R,W,W,R,R,R,R,R,R,W,W,W,R,R,R,R,R,W,W,R,R,R,R,R,R,],"BI":[W,R,R,R,R,R,R,W,G,W,R,R,R,R,W,G,G,G,W,W,W,W,G,G,G,G,W,R,R,W,G,G,G,G,W,R,R,W,G,G,G,G,W,W,W,W,G,G,G,W,R,R,R,R,W,G,W,R,R,R,R,R,R,W,],"BJ":[DG,DG,DG,Y,Y,Y,Y,Y,DG,DG,DG,Y,Y,Y,Y,Y,DG,DG,DG,Y,Y,Y,Y,Y,DG,DG,DG,Y,Y,Y,Y,Y,DG,DG,DG,R,R,R,R,R,DG,DG,DG,R,R,R,R,R,DG,DG,DG,R,R,R,R,R,DG,DG,DG,R,R,R,R,R,],"BN":[W,W,Y,Y,Y,Y,Y,Y,BL,W,W,Y,Y,Y,Y,Y,BL,BL,W,R,R,Y,Y,Y,Y,BL,R,R,R,R,Y,Y,Y,Y,R,R,R,R,Y,Y,Y,Y,Y,R,R,W,W,Y,Y,Y,Y,Y,BL,BL,W,W,Y,Y,Y,Y,Y,BL,BL,W,],"BW":[L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,W,W,W,W,W,W,W,W,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,W,W,W,W,W,W,W,W,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,],"CF":[DB,DB,DB,R,R,DB,DB,DB,DB,Y,DB,R,R,DB,DB,DB,W,W,W,R,R,W,W,W,W,W,W,R,R,W,W,W,G,G,G,R,R,G,G,G,G,G,G,R,R,G,G,G,Y,Y,Y,R,R,Y,Y,Y,Y,Y,Y,R,R,Y,Y,Y,],"CG":[G,G,G,G,G,G,G,Y,G,G,G,G,G,G,Y,Y,G,G,G,G,G,Y,Y,R,G,G,G,G,Y,Y,R,R,G,G,G,Y,Y,R,R,R,G,G,Y,Y,R,R,R,R,G,Y,Y,R,R,R,R,R,Y,Y,R,R,R,R,R,R,],"CI":[O,O,O,W,W,G,G,G,O,O,O,W,W,G,G,G,O,O,O,W,W,G,G,G,O,O,O,W,W,G,G,G,O,O,O,W,W,G,G,G,O,O,O,W,W,G,G,G,O,O,O,W,W,G,G,G,O,O,O,W,W,G,G,G,],"CL":[DB,DB,DB,W,W,W,W,W,DB,W,DB,W,W,W,W,W,DB,W,DB,W,W,W,W,W,DB,DB,DB,W,W,W,W,W,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,],"CM":[DG,DG,R,R,R,R,Y,Y,DG,DG,R,R,R,R,Y,Y,DG,DG,R,R,R,R,Y,Y,DG,DG,R,Y,Y,R,Y,Y,DG,DG,R,Y,Y,R,Y,Y,DG,DG,R,R,R,R,Y,Y,DG,DG,R,R,R,R,Y,Y,DG,DG,R,R,R,R,Y,Y,],"CO":[Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,DB,DB,DB,DB,DB,DB,DB,DB,DB,DB,DB,DB,DB,DB,DB,DB,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,],"CR":[DB,DB,DB,DB,DB,DB,DB,DB,W,W,W,W,W,W,W,W,R,R,R,R,R,R,R,R,R,R,W,W,R,R,R,R,R,R,W,W,R,R,R,R,R,R,R,R,R,R,R,R,W,W,W,W,W,W,W,W,DB,DB,DB,DB,DB,DB,DB,DB,],"DK":[R,R,W,W,R,R,R,R,R,R,W,W,R,R,R,R,R,R,W,W,R,R,R,R,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,R,R,W,W,R,R,R,R,R,R,W,W,R,R,R,R,R,R,W,W,R,R,R,R,],"DO":[DB,DB,DB,W,W,R,R,R,DB,DB,DB,W,W,R,R,R,DB,DB,DB,W,W,R,R,R,W,W,W,DB,R,W,W,W,W,W,W,R,DB,W,W,W,R,R,R,W,W,DB,DB,DB,R,R,R,W,W,DB,DB,DB,R,R,R,W,W,DB,DB,DB,],"EC":[Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,L,L,Y,Y,Y,DB,DB,DB,G,G,DB,DB,DB,DB,DB,DB,Y,Y,DB,DB,DB,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,],"PH":[W,DB,DB,DB,DB,DB,DB,DB,Y,W,DB,DB,DB,DB,DB,DB,W,W,W,DB,DB,DB,DB,DB,W,Y,Y,W,DB,DB,DB,DB,W,Y,Y,W,R,R,R,R,W,W,W,R,R,R,R,R,Y,W,R,R,R,R,R,R,W,R,R,R,R,R,R,R,],"UG":[BL,BL,BL,BL,BL,BL,BL,BL,Y,Y,Y,Y,Y,Y,Y,Y,R,R,R,W,W,R,R,R,R,R,W,BL,W,W,R,R,BL,BL,W,BL,BL,W,BL,BL,BL,BL,BL,W,W,BL,BL,BL,Y,Y,Y,Y,Y,Y,Y,Y,R,R,R,R,R,R,R,R,],"TZ":[G,G,G,G,G,G,Y,BL,G,G,G,G,G,Y,BL,BL,G,G,G,G,Y,BL,BL,Y,G,G,G,Y,BL,BL,Y,L,G,G,Y,BL,BL,Y,L,L,G,Y,BL,BL,Y,L,L,L,Y,BL,BL,Y,L,L,L,L,BL,BL,Y,L,L,L,L,L,],"TN":[R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,W,W,R,R,R,R,R,W,R,R,W,R,R,R,R,W,R,R,W,R,R,R,R,R,W,W,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,],"NO":[R,W,DB,DB,W,R,R,R,R,W,DB,DB,W,R,R,R,W,W,DB,DB,W,W,W,W,DB,DB,DB,DB,DB,DB,DB,DB,DB,DB,DB,DB,DB,DB,DB,DB,W,W,DB,DB,W,W,W,W,R,W,DB,DB,W,R,R,R,R,W,DB,DB,W,R,R,R,],"ME":[R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,GO,R,R,GO,R,R,R,R,GO,GO,GO,GO,R,R,R,R,R,GO,GO,R,R,R,R,R,GO,GO,GO,GO,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,],"OM":[R,R,R,W,W,W,W,W,R,W,R,W,W,W,W,W,R,R,R,W,W,W,W,W,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,G,G,G,G,G,R,R,R,G,G,G,G,G,R,R,R,G,G,G,G,G,],"PA":[W,W,W,W,R,R,R,R,W,DB,DB,W,R,R,R,R,W,DB,DB,W,R,R,R,R,W,W,W,W,R,R,R,R,DB,DB,DB,DB,W,W,W,W,DB,DB,DB,DB,W,R,R,W,DB,DB,DB,DB,W,R,R,W,DB,DB,DB,DB,W,W,W,W,],"PE":[R,R,W,W,W,W,R,R,R,R,W,W,W,W,R,R,R,R,W,G,G,W,R,R,R,R,G,W,W,G,R,R,R,R,G,R,R,G,R,R,R,R,W,G,G,W,R,R,R,R,W,W,W,W,R,R,R,R,W,W,W,W,R,R,],"MK":[Y,R,R,Y,Y,R,R,Y,R,Y,R,Y,Y,R,Y,R,R,R,Y,Y,Y,Y,R,R,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,R,R,Y,Y,Y,Y,R,R,R,Y,R,Y,Y,R,Y,R,Y,R,R,Y,Y,R,R,Y,],"MG":[W,W,W,R,R,R,R,R,W,W,W,R,R,R,R,R,W,W,W,R,R,R,R,R,W,W,W,R,R,R,R,R,W,W,W,DG,DG,DG,DG,DG,W,W,W,DG,DG,DG,DG,DG,W,W,W,DG,DG,DG,DG,DG,W,W,W,DG,DG,DG,DG,DG,],"EE":[L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W],"FI":[W,W,B,B,W,W,W,W,W,W,B,B,W,W,W,W,W,W,B,B,W,W,W,W,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,W,W,B,B,W,W,W,W,W,W,B,B,W,W,W,W,W,W,B,B,W,W,W,W],"GA":[G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L],"GE":[W,W,W,R,R,W,W,W,W,R,W,R,R,W,R,W,W,W,W,R,R,W,W,W,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,W,W,W,R,R,W,W,W,W,R,W,R,R,W,R,W,W,W,W,R,R,W,W,W],"GH":[R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,Y,Y,Y,BL,BL,Y,Y,Y,Y,Y,BL,BL,BL,BL,Y,Y,Y,Y,Y,BL,BL,Y,Y,Y,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G,G],"GT":[L,L,W,W,W,L,L,L,L,L,W,W,W,L,L,L,L,L,W,DG,W,L,L,L,L,L,DG,Y,DG,L,L,L,L,L,W,DG,W,L,L,L,L,L,W,W,W,L,L,L,L,L,W,W,W,L,L,L,L,L,W,W,W,L,L,L],"GY":[W,W,W,W,W,W,G,G,BL,Y,Y,Y,Y,Y,W,G,R,BL,BL,Y,Y,Y,W,G,R,R,R,BL,Y,Y,Y,W,R,R,R,BL,Y,Y,Y,W,R,BL,BL,Y,Y,Y,W,G,BL,Y,Y,Y,Y,W,G,G,W,W,W,W,W,G,G,G],"HN":[B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,W,W,W,W,W,W,W,W,W,W,B,W,W,B,W,W,W,B,W,W,W,W,B,W,W,W,W,W,W,W,W,W,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B],"IE":[G,G,G,W,W,O,O,O,G,G,G,W,W,O,O,O,G,G,G,W,W,O,O,O,G,G,G,W,W,O,O,O,G,G,G,W,W,O,O,O,G,G,G,W,W,O,O,O,G,G,G,W,W,O,O,O,G,G,G,W,W,O,O,O],"IL":[W,W,W,W,W,W,W,W,B,B,B,B,B,B,B,B,W,W,W,W,W,W,W,W,W,W,W,W,B,W,W,W,W,W,W,B,W,W,W,W,W,W,W,W,W,W,W,W,B,B,B,B,B,B,B,B,W,W,W,W,W,W,W,W],"IS":[B,W,R,R,W,B,B,B,B,W,R,R,W,B,B,B,W,W,R,R,W,W,W,W,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,W,W,R,R,W,W,W,W,B,W,R,R,W,B,B,B,B,W,R,R,W,B,B,B],"KE":[BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,BL,R,R,BL,BL,BL,W,W,W,R,R,W,W,W,R,R,BL,W,R,BL,R,R,R,R,BL,R,W,BL,R,R,W,W,W,R,R,W,W,W,G,G,G,R,R,G,G,G,G,G,G,G,G,G,G,G],"KH":[B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,R,R,R,R,R,R,R,R,R,R,R,W,W,R,R,R,R,R,R,W,W,R,R,R,R,R,W,W,W,W,R,R,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B],"LA":[R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,B,B,B,W,W,B,B,B,B,B,W,W,W,W,B,B,B,B,W,W,W,W,B,B,B,B,B,W,W,B,B,B,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R,R],"LR":[B,B,B,R,R,R,R,R,B,W,B,R,R,R,R,R,B,B,B,W,W,W,W,W,R,R,R,R,R,R,R,R,W,W,W,W,W,W,W,W,R,R,R,R,R,R,R,R,W,W,W,W,W,W,W,W,R,R,R,R,R,R,R,R],"LT":[DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR],"MA":[DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,G,G,DR,DR,DR,DR,DR,G,G,G,G,DR,DR,DR,DR,DR,G,G,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR,DR],"NZ":[W,R,W,B,B,B,B,B,R,R,R,B,B,B,B,B,W,R,W,B,B,R,B,B,B,B,B,B,B,B,B,B,B,B,B,B,R,B,R,B,B,B,B,B,B,B,B,B,B,B,B,B,B,R,B,B,B,B,B,B,B,B,B,B],"LV":[BR,BR,BR,BR,BR,BR,BR,BR,BR,BR,BR,BR,BR,BR,BR,BR,BR,BR,BR,BR,BR,BR,BR,BR,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,W,BR,BR,BR,BR,BR,BR,BR,BR,BR,BR,BR,BR,BR,BR,BR,BR,BR,BR,BR,BR,BR,BR,BR,BR,]}
        
        # Create a datetime variable to store the end time of the experiment
        stop_delta = datetime.timedelta(minutes=running_time)

        # Creates a datetime variable to store the start time of the experiment
        start_time = datetime.datetime.now()

        # Sets the aproximatly distance from earth surface to ISS
        self.distance_ISS_earth = 400000
        
        # Sets earth mass
        self.earth_mass = 5.9722 * (10 ** 24)

        # Sets the gravital constant for earth
        self.gravitational_constant = 6.67 * (10 ** -11)

        # Sets ISS mass
        self.ISS_mass = 419700

        # Earth radius
        self.earth_radius = 6371 * (10 ** 3)
        
        # Sets the running_time (in min) for the experiment
        self.running_time = running_time

        # Calculates the stop_time for the experiment
        self.stop_time = start_time + stop_delta

    def calculate_force(self):
        """Calculating force and speed for the ISS
            @return: dict
        """

        # Calculating force
        force = (self.gravitational_constant * self.ISS_mass * self.earth_mass) / ((self.distance_ISS_earth + self.earth_radius) ** 2)

        # Calculating speed
        speed = math.sqrt((self.gravitational_constant * self.earth_mass) / (self.distance_ISS_earth + self.earth_radius))
        
        # Formats the speed and force
        measurements_dict = {'force': force, 'speed': speed}

        return measurements_dict

    def check_time(self):
        """Checks if the time for the experiment is up
            @return: Boolean
        """
        # Create a datetime variable to store the current time
        now_time = datetime.datetime.now() 

        # Checks if the experiment time has ran up
        if (now_time < self.stop_time):
            return True
        return False

    def check_sleep(self, timedelta_seconds):
        """Checks if can sleep or if the current_time + sleep_time exceeds project time
            @param1: int
            @return: Boolean
        """
        # Gets current time
        now = datetime.datetime.now()

        # Calculates time after sleep
        after_timedelta = datetime.timedelta(seconds=timedelta_seconds)

        # Checks if it is possible to sleep
        if (now + after_timedelta < self.stop_time):
            return True
        return False

    def get_coordinates_ISS(self):
        """Get's current ISS coordinates
            @return: dict
        """
        # Sets the constant variables for finding the ISS location
        name = "ISS (ZARYA)"
        satellite1 = "1 25544U 98067A   20013.25395446  .00001038  00000-0  26560-4 0  9999"
        satellite2 = "2 25544  51.6448  40.0308 0005021 125.1468 332.5313 15.49559205207846"
        
        # Gets ISS location
        iss = ephem.readtle(name, satellite1, satellite2)
        iss.compute()
        
        # Formats the coordinates
        lat = int(str(iss.sublat).split(":")[0]) + int(str(iss.sublat).split(":")[1])*0.01
        long = int(str(iss.sublong).split(":")[0]) + int(str(iss.sublong).split(":")[1])*0.01
        coordinates_dict = {'lat': lat, 'long': long}

        return coordinates_dict

    def write_data_continuously(self, files):
        """Writes humidity, temperature and pressure for the current time (every 60s)
            @return: None
        """
        #If you have time left for the experiment and the file was created correctly
        while (self.check_time()):
            # Writes data to file
            self.write_data_csv(files[0])
            self.write_force_csv(files[1])

            # Sleeps if possible
            if (self.check_sleep(60)):
                sleep(60)
            else:
                return None

    def write_data_csv(self, file):
        """Writes current data to the csv file"""
        # Connect to the Sense HAT
        sh = SenseHat()
        
        # Get current time formatted
        now = datetime.datetime.utcnow()
        dt_string = now.strftime("%d/%m/%Y, %H:%M:%S")

        # Read data from Sense HAT
        temperature = sh.get_temperature()
        humidity = sh.get_humidity()
        pressure = sh.get_pressure()

        # Format the data from the Sense HAT
        temperature = "{0:.2f}".format(temperature)
        humidity = "{0:.2f}".format(humidity)
        pressure = "{0:.2f}".format(pressure)

        # Save the data to the file
        file.info("%s, %s, %s, %s", dt_string, humidity, temperature, pressure)

    def setup_logger(self, dir_path, name):
        """Tries to create csv logger object"""
        try:
            #Try to create a file at the dir_path
            handler = logging.FileHandler(dir_path)
            formatter = logging.Formatter('%(message)s')
            handler.setFormatter(formatter)
        
            logger = logging.getLogger(name)
            logger.setLevel(logging.DEBUG)
            logger.addHandler(handler)

            self.created_file = True
            return logger
        except:
            self.created_file = False

    def write_force_csv(self, file):
        """Writes the force and speed data to the designated csv file"""
        #Gets measurements
        measurements = self.calculate_force()
        force = measurements['force']
        speed = measurements['speed']
        
        force = "{0:.2f}".format(force)
        speed = "{0:.2f}".format(speed)
        
        # Get current time formatted
        now = datetime.datetime.utcnow()
        dt_string = now.strftime("%d/%m/%Y, %H:%M:%S")
        
        # Save the data to the file
        file.info("%s, %s, %s", dt_string, speed, force)

    def show_country_countinously(self):
        """Updates the country flags on the SenseHat LED Matrix (every 5s)"""
        self.geo = rg.RGeocoder(mode=2, verbose=True, stream=io.StringIO(open(os.path.dirname(os.path.realpath(__file__)) + '/custom.csv', encoding='utf-8').read()))
        #If you have time left for the experiment and the file was created correctly
        while (self.check_time()):
            self.show_country()

            # Sleeps if possible
            if (self.check_sleep(5)):
                sleep(5)
            else:
                return None

    def show_country(self):
        """Gets the country that is below ISS
            @return: dict
        """
        # Gets ISS coordinates 
        coordinates_dict = self.get_coordinates_ISS()
        coordinates = (coordinates_dict['lat'], coordinates_dict['long']),
        
        # Find the country below ISS
        result = self.geo.query(coordinates)[0]['cc']
        
        sense = SenseHat()
        #Displays the ocean name
        if result == 'InO':
            sense.show_message('Indian Ocean', text_colour = [255, 255, 255], back_colour = [0, 0, 255])
            return
        elif result == 'AtO':
            sense.show_message('Atlantic Ocean', text_colour = [255, 255, 255], back_colour = [0, 0, 255])
            return
        elif result == 'PaO':
            sense.show_message('Pacific Ocean', text_colour = [255, 255, 255], back_colour = [0, 0, 255])
            return

        #Displays the country flag
        for flag in self.flags:
            if result == flag:
                sense.set_pixels(self.flags[flag])
                return

# Creates the class object for Astro_Pi()
runtime = 1

ASTRO_PI_OBJ = Astro_Pi(runtime)
ASTRO_PI_OBJ1 = Astro_Pi(runtime)

# Sets the dir_path for the csv file
dir_path01 = os.path.dirname(os.path.realpath(__file__)) + "/data01.csv"

file01 = ASTRO_PI_OBJ.setup_logger(dir_path01, 'data01.csv')
file01.info("%s, %s, %s, %s, %s", 'Date(UTC)', 'Time(UTC)', 'Humidity', 'Temperature(C)', 'Pressure(hPa)')

dir_path02 = os.path.dirname(os.path.realpath(__file__)) + "/data02.csv"

file02 = ASTRO_PI_OBJ.setup_logger(dir_path02, 'data02.csv')
file02.info("%s, %s, %s, %s", 'Date(UTC)', 'Time(UTC)', 'Speed(m/s)', 'Force(N)')

# Starts a thread to write in the csv file
x = threading.Thread(target=ASTRO_PI_OBJ.write_data_continuously, args = ([file01, file02], ))
y = threading.Thread(target=ASTRO_PI_OBJ1.show_country_countinously)
x.start()
y.start()

# Waits for the threads to finish and closes them
x.join()
y.join()
