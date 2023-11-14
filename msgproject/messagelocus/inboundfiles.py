import os

import requests
import json

file_directory = 'C:\\Users\\areese\\Documents\\SAP\\SAP GUI'
files = os.listdir(file_directory)

URL = 'http://127.0.0.1:8000/messagelocus/inbound/'
client = requests.session()
client.auth = ('areese','areese1234')

for file in files:
	pattern = file[0]+file[3]
	file_path = file_directory+'\\'+file
	if pattern == 'E1':
		with open(file_path, 'r') as f:
			response = client.post(URL,
								json=json.loads(f.read()))
		
		if response.status_code == 200:
			os.remove(file_path)
			print('File {} Processed'.format(file))
		else:
			print('File {} - Server Error - {}'.format(file, request.text))