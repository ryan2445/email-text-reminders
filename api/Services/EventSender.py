import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime
import os
import pytz
import re

if os.getenv('AWS_SAM_LOCAL'):
    dynamodb = boto3.resource('dynamodb', endpoint_url = 'http://dynamodb-local:8000').Table('system')
else:
    dynamodb = boto3.resource('dynamodb').Table('system')

sns = boto3.client('sns')
ses = boto3.client('ses')

def handle(event, context):
    response = dynamodb.query(KeyConditionExpression=Key('pk').eq('EVENT')).get('Items')

    events = list(filter(lambda item: not item.get('disabled'), response))

    pst = pytz.timezone('America/Los_Angeles')
    [curr_date, curr_time] = str(datetime.now(pst)).split()
    day_name = datetime.now(pst).strftime("%A")

    for _event in events:
        username = _event['sk'].split("#")[0]

        user = dynamodb.get_item(Key = { 'pk': 'USER', 'sk': username })['Item']
        user_phone = '+1' + re.sub('[^0-9]','', user['phone'])
        user_email = user['email']

        dates = _event['recurringDays'] if _event['recurring'] else _event['dates']
        times = _event['times']

        is_curr_date = False
        for date in dates:
            if _event['recurring']:
                if day_name in date:
                    is_curr_date = True
                    break
            else:
                if curr_date == date:
                    is_curr_date = True
                    break

        is_curr_time = False
        for time in times:
            time_12hr = datetime.strptime(time, "%I:%M %p")
            time_24hr = datetime.strftime(time_12hr, "%H:%M")
            if time_24hr == curr_time[0:5]:
                is_curr_time = True
                break

        if is_curr_date and is_curr_time:
            if _event['sendSms']:
                sns.publish(
                    PhoneNumber = user_phone,
                    Message = f"{_event['title']}: {_event['description']}"
                )
            
            if _event['sendEmail']:
                ses.send_email(
                    Destination={
                        "ToAddresses": [
                            user_email,
                        ]
                    },
                    Message={
                        "Subject": {
                            "Charset": "UTF-8",
                            "Data": _event['title']
                        },
                        "Body": {
                            "Text": {
                                "Charset": "UTF-8",
                                "Data": _event['description']
                            }
                        }
                    },
                    Source="ryanhoffman2445@gmail.com",
                )

    return 'Success!'
