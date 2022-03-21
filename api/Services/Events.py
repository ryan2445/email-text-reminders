import boto3
from boto3.dynamodb.conditions import Key
import json
import os
import uuid

if os.getenv('AWS_SAM_LOCAL'):
    dynamodb = boto3.resource('dynamodb', endpoint_url = 'http://dynamodb-local:8000').Table('system')
else:
    dynamodb = boto3.resource('dynamodb').Table('system')

def eventsPost(event, context):
    body = json.loads(event['body'])
    username = event['requestContext']['authorizer']['claims']['email']

    required_keys = ['title', 'description']

    if not all(body.get(key) for key in required_keys):
        return {
            'statusCode': 400,
            'body': 'Validation Error: Missing required keys.'
        }
    
    event_id = str(uuid.uuid4())
    
    dynamodb.put_item(
        Item = {
            'pk': 'EVENT',
            'sk': username + '#' + event_id,
            'title': body['title'],
            'description': body['description'],
            'uuid': event_id
        }
    )

    return {
        'statusCode': 200,
        'body': 'Success!'
    }

def eventsGet(event, context):
    username = event['requestContext']['authorizer']['claims']['email']

    response = dynamodb.query(KeyConditionExpression = Key('pk').eq("EVENT") & Key('sk').begins_with(username))

    items = response.get('Items') or []

    return {
        'statusCode': 200,
        'body': json.dumps({ 'items': items })
    }

def handle(event, context):
    response = None

    methods = {
        'POST': {
            '/events': eventsPost
        },
        'GET': {
            '/events': eventsGet
        }
    }

    httpMethod = event['httpMethod']
    path = event['path']

    response = methods[httpMethod][path](event, context)
    
    response['headers'] = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
    }

    return response
