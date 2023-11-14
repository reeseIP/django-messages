import requests 
import json


URL = 'http://127.0.0.1:8000/messagelocus/inbound/'

client = requests.Session()
client.auth = ('areese','areese1234')

job_message = {"PutawayJob":{"EventType":"NEW","EventInfo":"","LicensePlate":"00001100000000001144","RequestId":"8042","JobId":"EDB18042","JobDate":"2023-11-11T00:53:52","JobPriority":"000","JobTasks":{"PutawayJobTask":[{"JobTaskId":"22272","EventAction":"","InnerLicensePlate":"","OrderId":"4400009049","OrderLineId":"0000000010","OrderTaskId":"","OrderType":"","CustOwner":"3011","SiteId":"EDB1","TaskType":"PUT","TaskTravelPriority":0,"TaskLocation":"GR-CONS","TaskZone":"","TaskWorkArea":"","TaskQty":1,"ItemNo":"78426963","ItemUPC":"","ItemDesc":"FA/PLUS GRANULE-DOG 650GM","ItemStyle":"","ItemColor":"","ItemSize":"","ItemLength":0,"ItemWidth":1,"ItemHeight":1,"ItemWeight":2,"ItemImageUrl":"","LotNo":"","SerialNo":"","Custom1":"","Custom2":"","Custom3":"","Custom4":"","Custom5":"","Custom6":"","Custom7":"","Custom8":"","Custom9":"","Custom10":""}]}}}                                                                                                                                                                                     


response = requests.post(URL,
      							json=job_message,
      							auth=('areese','areese1234'))

print(response.status_code)