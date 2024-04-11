# sendxml.py
import requests 
import xml.etree.ElementTree as ET

URL = 'http://localhost:8000/messagelocus/EW1/inbound_xml/'
username = 'areese'
password = 'areese1234'

client = requests.Session()

# create xml document
methodcall = ET.Element('methodcall')
name = ET.SubElement(methodcall, 'name')
params = ET.SubElement(methodcall, 'params')
taskgroup_id = ET.SubElement(params, 'taskgroup_id').text = '134523'

client.get(URL)  # sets cookie

# send xml document
response = client.post(URL, data=ET.tostring(methodcall, encoding='utf-8', xml_declaration=True))