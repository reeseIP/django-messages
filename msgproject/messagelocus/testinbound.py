import requests 
import json


URL = 'http://127.0.0.1:8000/messagelocus/inbound/'

client = requests.Session()
client.auth = ('areese','areese1234')

#tasks = {"OrderJobTask":[{ "JobTaskId":"22276",
#               					"EventAction":"",
#               					"OrderId":"4400009049",
#               					"OrderLineId":"0000000010",
#               					"OrderTaskId":"",
#               					"CustOwner":"3011",
#               					"SiteId":"EDB1",
#               					"TaskType":"PUT",
#               					"TaskLocation":"GR-CONS",
#               					"TaskZone":"",
#               					"TaskQty":1,
#               					"ItemNo":"78426963",
#               					"ItemUPC":"",
#               					"ItemDesc":"FA/PLUS GRANULE-DOG 650GM",
#               					"ItemStyle":"",
#               					"ItemColor":"",
#               					"ItemSize":"",
#               					"ItemLength":0,
#               					"ItemWidth":1,
#               					"ItemHeight":1,
#               					"ItemWeight":2,
#               					"ItemImageUrl":"",
#               					"Custom1":"",
#               					"Custom2":"",
#               					"Custom3":"",
#               					"Custom4":"",
#               					"Custom5":"",
#               					"Custom6":"",
#               					"Custom7":"",
#               					"Custom8":"",
#               					"Custom9":"",
#               					"Custom10":"",
#               					"LotNo":"",
#               					"SerialNo":"",
#               					"CaptureLotNo":"false",
#               					"CaptureSerialNo":"false",
#               					"CaptureSerialNoQty":"0",
# 							}]}
#
#job_message = {"OrderJob": {"EventType":"NEW",
#									"JobId":"1235",
#									"JobDate":"Date",
#									"JobPriority":None,
#									"JobPriorityGroup":None,
#									"RequestId":"1232",
#									"ToteId":"HU12343543",
#									"SingleUnit":None,
#									"NextWorkArea":"",
#									"JobTasks": tasks
#									}}
#

job_message = {
   "PutawayJob":{
      "EventType":"NEW",
      "EventInfo":"",
      "LicensePlate":"",
      "RequestId":"8041",
      "JobId":"EDB18041",
      "JobDate":"2023-11-08T01:29:39",
      "JobPriority":"000",
      "JobTasks":{
         "PutAwayJobTask":[
            {
               "JobTaskId":"22274",
               "EventAction":"",
               "INNERLICENSEPLATE":"",
               "OrderId":"4400009049",
               "OrderLineId":"0000000010",
               "OrderTaskId":"",
               "OrderType":"",
               "CustOwner":"3011",
               "SiteId":"EDB1",
               "TaskType":"PUT",
               "TASKTRAVELPRIORITY":0,
               "TaskLocation":"GR-CONS",
               "TaskZone":"",
               "TaskWorkArea":"",
               "TaskQty":1,
               "ItemNo":"78426963",
               "ItemUPC":"",
               "ItemDesc":"FA/PLUS GRANULE-DOG 650GM",
               "ItemStyle":"",
               "ItemColor":"",
               "ItemSize":"",
               "ItemLength":0,
               "ItemWidth":1,
               "ItemHeight":1,
               "ItemWeight":2,
               "ItemImageUrl":"",
               "LotNo":"",
               "SerialNo":"",
               "Custom1":"",
               "Custom2":"",
               "Custom3":"",
               "Custom4":"",
               "Custom5":"",
               "Custom6":"",
               "Custom7":"",
               "Custom8":"",
               "Custom9":"",
               "Custom10":""
            }
         ]
      }
   }
}
response = requests.post(URL,
							json=json.dumps(job_message),
							auth=('areese','areese1234'))

print(response.text)