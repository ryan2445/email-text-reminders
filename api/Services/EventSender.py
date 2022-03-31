import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime
import os
import pytz

if os.getenv('AWS_SAM_LOCAL'):
    dynamodb = boto3.resource('dynamodb', endpoint_url = 'http://dynamodb-local:8000').Table('system')
else:
    dynamodb = boto3.resource('dynamodb').Table('system')

sns = boto3.client('sns')

def handle(event, context):
    response = dynamodb.query(
        KeyConditionExpression=Key('pk').eq('EVENT')
    ).get('Items')

    events = list(filter(lambda item: not item.get('disabled'), response))

    pst = pytz.timezone('America/Los_Angeles')
    [curr_date, curr_time] = str(datetime.now(pst)).split()

    for _event in events:
        disableEvent = True

        dates = _event['dates']
        times = _event['times']

        is_curr_date = False
        for date in dates:
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
            sns.publish(
                PhoneNumber = '+19257868567',
                Message = f"{_event['title']}: {_event['description']}"
            )

    return 'Success!'