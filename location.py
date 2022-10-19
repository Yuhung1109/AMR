import os, json, random, time
from subprocess import *
from flask import Flask
from flask_cors import cross_origin
from flask_api import status
from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font

app = Flask(__name__)

def Transfer(RSRP_ini):
    DongleRSRP = RSRP_ini
    x_axis = 1
    y_axis = -140
    value = DongleRSRP - x_axis
    RSRP_fix = y_axis + value
    return RSRP_fix

@app.route('/data', methods = ['GET'])
@cross_origin()
def data():
    data_json = {}
    res = os.popen("rosrun tf tf_echo /base_odom /base_laser")
    num = 0
    for read_num in range(3):
        xy = res.readline()
        temp = xy[16:29].split('u')[0].split('P')[0]
        if num % 5 == 1 :
            p = Popen("adb shell atcli at+cesq", shell=True, stdout=PIPE)
            output = str(p.communicate()[0])
            if str(output[47]) == ",":
                result = Transfer(int(output[48:50]))
            else:
                result = Transfer(int(output[47:49]))
            data = temp.replace(' ', '')
            print(data)
            for op in range(len(data)):
                if data[op] == ',':
                    break
            data_json['X'] = data[0:op]
            data_json['Y'] = data[op+1:len(data)]
            data_json['RSRP'] = str(result)
        num =  num + 1
    return json.dumps(data_json), status.HTTP_200_OK

app.run(host = '0.0.0.0', port = 6789, debug = True, threaded = True)

#res = os.popen("rosrun tf tf_echo /base_odom /base_laser")
#num = 0
#while(1):
    #xy = res.readline()
    #temp = xy[16:29].split('u')[0].split('P')[0]
    #if num % 5 == 1 :
        #data = temp.replace(' ', '')
        #print(data)
        #x = data[0:6]
        #print(x)
        #y = data[7:13]
        #print(y)
    #num = num + 1