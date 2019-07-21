from aiy.board import Board
from picamera import PiCamera
import requests
import time
import math
import json
import os
import sys

camera = PiCamera()
camera.resolution = (320, 240)

def check_file_exist():
    home = os.path.expanduser("~")
    filename = home + "/coding101_cloudservices.json"
    try:
        with open(filename, 'r') as file:
            text = file.readlines()
            json_dict = json.loads(text[0].rstrip())
            if 'host' in json_dict and 'client_id' in json_dict:
                return True, json_dict['host'], json_dict['client_id']
            else:
                return False, "", ""
    except:
        return False, "", ""
      
def _wait_for_duration():
    global seconds
    time.sleep(seconds)

def get_faces():
    status, host, client_id = check_file_exist()
    if status == False:
        print("ERROR: Can't find the credential file")
        sys.exit(1)
    
    timestamp = math.ceil(time.time())
    filename = '/tmp/file-' + str(timestamp) + '.jpg'
    
    camera.capture(filename)
        
    try:
        #url = "http://192.168.101.153:8081/client/ABCDE"
        url = host + '/face/' + client_id
        files = {'file':open(filename,'rb')}
        req = requests.post(url, files=files)
        os.remove(filename)
        #print(req.text)
        reply = json.loads(req.text)
        if reply["status"] == True:
            return reply["faces"]
        else:
            if reply["error"] != None:
                print("ERROR:", reply["error"])
            return ""
    except Exception as err: 
        return "" 

def get_labels():
    status, host, client_id = check_file_exist()
    if status == False:
        print("ERROR: Can't find the credential file")
        sys.exit(1)
    
    timestamp = math.ceil(time.time())
    filename = '/tmp/file-' + str(timestamp) + '.jpg'
    
    camera.capture(filename)
        
    try:
        #url = "http://192.168.101.153:8081/client/ABCDE"
        url = host + '/label/' + client_id
        #print("url:", url)
        files = {'file':open(filename,'rb')}
        req = requests.post(url, files=files)
        os.remove(filename)
        #print(req.text)
        reply = json.loads(req.text)
        if reply["status"] == True:
            return reply["labels"]
        else:
            if reply["error"] != None:
                print("ERROR:", reply["error"])
            return ""
    except Exception as err: 
        print (err)
        return ""

def examine_labels():
    #labels_dict = json.loads(labels)
    labels = get_labels()

    results = []
    for label in labels:
        results.append({ "description" : label['description'], "score" : label['score']})
    return results

'''
with Board() as board:
    
    print("wait for button")
    board.button.wait_for_press()
    faces = get_faces()
    print("faces: " + str(len(faces)))
    print("done")
'''


