########################################################################################################################
# Written by: Rishi Uppal
# Date: Jan 5, 2023
# Module: wh132_json.py
# This module creates JSON files for each test
# Requires global_vars.py for all libraries
########################################################################################################################

import json
import global_vars as gv
import global_vars
from termcolor import colored
import gcs_uploader_wh132
import os

local_path = r'wh132_json_files/'
directory = os.path.dirname(local_path)

try:
    os.stat(directory)
except:
    os.mkdir(directory)


def make_json():

    file = open(local_path + str(gv.qr_id) + '-' + str(int(gv.test_output['timestamp'])) + '.json', 'w')

    json.dump(gv.test_output, file, indent=4, sort_keys=True)

    file.close()

    fileName = str(file)
    fileName = fileName.split('/')
    fileName = fileName[1].split(',')
    fileName = (fileName[0])[0:-29]

    print(colored('\nJSON file ' + fileName + ' created\n', 'yellow'))

    # gcs_uploader_wh132.gcs_upload(fileName)