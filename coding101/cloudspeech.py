from aiy.voice.audio import AudioFormat, play_wav, record_file, Recorder
from aiy.board import Board
import requests
import time
import math
import json
import os
import sys

seconds=5
play_file=False

def check_file_exist():
    home = os.path.expanduser("~")
    filename = home + "/coding101_cloudservices.json"
    try:
        with open(filename, 'r') as file:
            text = file.readlines()
            json_dict = json.loads(text[0].rstrip())
            if 'host' in json_dict:
                return True, json_dict['host'], json_dict['client_id']
            else:
                return False, ""
    except:
        return False, ""
      
def _wait_for_duration():
    global seconds
    time.sleep(seconds)

def playback_after_recognize(status=False):
    global play_file
    play_file = status

def recognize(language_code='en_US', wait=None, duration=5):
    global seconds
    global play_file
    
    status, host, client_id = check_file_exist()
    if status == False:
        print("ERROR: Can't find the credential file")
        sys.exit(1)
    
    timestamp = math.ceil(time.time())
    filename = '/tmp/file-' + str(timestamp)
    #print(filename)
    
    if wait != None:
        record_file(AudioFormat.CD, filename=filename, wait=wait, filetype='wav')
    else:
        seconds = duration
        record_file(AudioFormat.CD, filename=filename, wait=_wait_for_duration, filetype='wav')
        
    try:
        #url = "http://192.168.101.153:8081/client/ABCDE"
        url = host + "/voice/" + client_id
        files = {'file':open(filename,'rb')}
        values = {'languageCode': language_code}
        req = requests.post(url, files=files, data=values)

        #play_wav(filename)
        if play_file == True:
            play_wav(filename)

        os.remove(filename)
        #print(req.text)
        reply = json.loads(req.text)
        if reply["status"] == True:
            return reply["transcript"]
        else:
            if reply["error"] != None:
                print("ERROR:", reply["error"])
            return ""
    except Exception as err: 
        return ""

'''
with Board() as board:
    
    def wait():
        board.button.wait_for_press()
    
    print("wait for button")
    board.button.wait_for_press()
    print("say something")
    text = recognize(language_code='zh_HK', duration=3)
    print("text: " + text)
    print("done")
'''

