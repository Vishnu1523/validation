from re import X
from urllib import response
from urllib.parse import urlparse,parse_qs
import asyncio
#import requests
import json
from pyodide.http import pyfetch
myUrl = urlparse("https://staging.formen.health/?order_id=928373&address1=sdfsfgtht1hgthtyhtyhythtrgtrgththt&address2=nefgtfhythjytjyjngnghtyhty&city=hyderabad&state=ts&pincode=500084")
#myUrl = urlparse(url)
myQuery = parse_qs(myUrl.query)
cnt=0
#print(myUrl)
# print(type(myQuery))
final = {"status":"green","reason":"none"}
lent = len(myQuery['address1'][0])+len(myQuery['address2'][0])
if lent<45:
    final['status'] = 'red'
    final['reason']='length of address is small' 
    #print(final)
elif any(map(str.isdigit, myQuery['address1'][0])) or any(map(str.isdigit,myQuery['address2'][0])):
# print(myQuery['pincode'])
    url = "https://api.postalpincode.in/pincode/"+myQuery['pincode'][0]
    response = await pyfetch(url = url,method = "GET")
    if not response:
        final['status'] = 'red'
        final['reason'] = 'pincode incorrect'
        #print(final)
    data = response.json()

    for i in range(len(data[0]['PostOffice'])):
        name = data[0]['PostOffice'][i]['Name'].lower()
        region = data[0]['PostOffice'][i]['Region']
        district = data[0]['PostOffice'][i]['District'].lower()
        # print(name,district)
        if name == myQuery['city'][0] or district == myQuery['city'][0].lower():
            final['status'] = 'green'
            final['reason']='everything is fine'
        else:
            final['reason']="city/town are not matching"
            final['status'] = 'red'
        #print(final)
else:
    final["reason"]="No Digits in the address at all"
    final['status'] = 'red'
    #print(final)

print(json.dumps(final))


        


