import requests 
import json


URL = 'http://localhost:8000/messagelocus/ew1/inbound/'

#username = input('Username: ')
#password = input('Password: ')
username = 'areese'
password = 'areese1234'
#job_message = json.loads(input('Job Message: '))

#job_message = {"PutawayJob":{"EventType":"NEW","EventInfo":"","LicensePlate":"1100000000001144","RequestId":"100001","JobId":"EDB1100001","JobDate":"2023-11-11T00:53:52","JobPriority":"000","JobTasks":{"PutawayJobTask":[{"JobTaskId":"A00001","EventAction":"","InnerLicensePlate":"","OrderId":"4400009045","OrderLineId":"0000000010","OrderTaskId":"","OrderType":"","CustOwner":"3011","SiteId":"EDB1","TaskType":"PUT","TaskTravelPriority":0,"TaskLocation":"12-32-23-03","TaskZone":"","TaskWorkArea":"","TaskQty":1,"ItemNo":"78426963","ItemUPC":"","ItemDesc":"FA/PLUS GRANULE-DOG 650GM","ItemStyle":"","ItemColor":"","ItemSize":"","ItemLength":0,"ItemWidth":1,"ItemHeight":1,"ItemWeight":2,"ItemImageUrl":"","LotNo":"","SerialNo":"","Custom1":"","Custom2":"","Custom3":"","Custom4":"","Custom5":"","Custom6":"","Custom7":"","Custom8":"","Custom9":"","Custom10":""}]}}}
#job_message = {"PutawayJob":{"EventType":"NEW","EventInfo":"","LicensePlate":"1100000000001145","RequestId":"100002","JobId":"EDB1100002","JobDate":"2023-11-11T00:53:52","JobPriority":"000","JobTasks":{"PutawayJobTask":[{"JobTaskId":"A00002","EventAction":"","InnerLicensePlate":"","OrderId":"4400009046","OrderLineId":"0000000010","OrderTaskId":"","OrderType":"","CustOwner":"3011","SiteId":"EDB1","TaskType":"PUT","TaskTravelPriority":0,"TaskLocation":"43-23-20-06","TaskZone":"","TaskWorkArea":"","TaskQty":1,"ItemNo":"78426963","ItemUPC":"","ItemDesc":"FA/PLUS GRANULE-DOG 650GM","ItemStyle":"","ItemColor":"","ItemSize":"","ItemLength":0,"ItemWidth":1,"ItemHeight":1,"ItemWeight":2,"ItemImageUrl":"","LotNo":"","SerialNo":"","Custom1":"","Custom2":"","Custom3":"","Custom4":"","Custom5":"","Custom6":"","Custom7":"","Custom8":"","Custom9":"","Custom10":""},{"JobTaskId":"A00003","EventAction":"","InnerLicensePlate":"","OrderId":"4400009049","OrderLineId":"0000000010","OrderTaskId":"","OrderType":"","CustOwner":"3011","SiteId":"EDB1","TaskType":"PUT","TaskTravelPriority":0,"TaskLocation":"GR-CONS","TaskZone":"","TaskWorkArea":"","TaskQty":1,"ItemNo":"78426963","ItemUPC":"","ItemDesc":"FA/PLUS GRANULE-DOG 650GM","ItemStyle":"","ItemColor":"","ItemSize":"","ItemLength":0,"ItemWidth":1,"ItemHeight":1,"ItemWeight":2,"ItemImageUrl":"","LotNo":"","SerialNo":"","Custom1":"","Custom2":"","Custom3":"","Custom4":"","Custom5":"","Custom6":"","Custom7":"","Custom8":"","Custom9":"","Custom10":""}]}}}

job_message = {"OrderJob":{"EventType":"NEW","JobId":"EDB1900001","JobDate":"2023-11-11T00:53:52","JobPriority":"002","JobPriorityGroup":"2023-11-11T00:53:52","RequestId":"900001","ToteId":"1100000000001146","JobTasks":{"OrderJobTask":[{"JobTaskId":"Z00001","EventAction":"","OrderId":"4400009047","OrderLineId":"0000000010","OrderTaskId":"","CustOwner":"","SiteId":"EDB1","TaskType":"PICK","TaskLocation":"01-10-01-02","TaskZone":"","TaskQty":1,"ItemNo":"78426963","ItemUPC":"","ItemDesc":"FA/PLUS GRANULE-DOG 650GM","ItemStyle":"","ItemColor":"","ItemSize":"","ItemLength":0,"ItemWidth":1,"ItemHeight":1,"ItemWeight":2,"ItemImageUrl":"","Custom1":"","Custom2":"","Custom3":"","Custom4":"","Custom5":"","Custom6":"","Custom7":"","Custom8":"","Custom9":"","Custom10":"","LotNo":"","SerialNo":"","CaptureLotNo":"false","CaptureSerialNo":"true","CaptureSerialNoQty":"2"}]}}}
#job_message = {"OrderJob":{"EventType":"NEW","JobId":"EDB1900002","JobDate":"2023-11-11T00:53:52","JobPriority":"002","JobPriorityGroup":"2023-11-11T00:53:52","RequestId":"900002","ToteId":"1100000000001147","JobTasks":{"OrderJobTask":[{"JobTaskId":"Z00002","EventAction":"","OrderId":"4400009048","OrderLineId":"0000000010","OrderTaskId":"","CustOwner":"","SiteId":"EDB1","TaskType":"PICK","TaskLocation":"04-50-04-03","TaskZone":"","TaskQty":1,"ItemNo":"78426963","ItemUPC":"","ItemDesc":"FA/PLUS GRANULE-DOG 650GM","ItemStyle":"","ItemColor":"","ItemSize":"","ItemLength":0,"ItemWidth":1,"ItemHeight":1,"ItemWeight":2,"ItemImageUrl":"","Custom1":"","Custom2":"","Custom3":"","Custom4":"","Custom5":"","Custom6":"","Custom7":"","Custom8":"","Custom9":"","Custom10":"","LotNo":"","SerialNo":"","CaptureLotNo":"false","CaptureSerialNo":"false","CaptureSerialNoQty":"0"},{"JobTaskId":"Z00003","EventAction":"","OrderId":"4400009048","OrderLineId":"0000000010","OrderTaskId":"","CustOwner":"","SiteId":"EDB1","TaskType":"PICK","TaskLocation":"04-50-04-03","TaskZone":"","TaskQty":1,"ItemNo":"78426963","ItemUPC":"","ItemDesc":"FA/PLUS GRANULE-DOG 650GM","ItemStyle":"","ItemColor":"","ItemSize":"","ItemLength":0,"ItemWidth":1,"ItemHeight":1,"ItemWeight":2,"ItemImageUrl":"","Custom1":"","Custom2":"","Custom3":"","Custom4":"","Custom5":"","Custom6":"","Custom7":"","Custom8":"","Custom9":"","Custom10":"","LotNo":"","SerialNo":"","CaptureLotNo":"false","CaptureSerialNo":"false","CaptureSerialNoQty":"false"}]}}} 

response = requests.post(URL, json=job_message, auth=(username,password))
print(username,password,URL)

print('{}: {}'.format(response.status_code, response.text))
