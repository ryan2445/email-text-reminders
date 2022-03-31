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

    required_keys = ['title', 'description', 'dates', 'times']

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
            'dates': body['dates'],
            'times': body['times'],
            'uuid': event_id
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps({'event_id': event_id})
    }

def eventsPut(event, context):
    body = json.loads(event['body'])
    username = event['requestContext']['authorizer']['claims']['email']

    required_keys = ['uuid', 'title', 'description', 'dates', 'times']

    if not all(body.get(key) for key in required_keys):
        return {
            'statusCode': 400,
            'body': 'Validation Error: Missing required keys.'
        }
    
    dynamodb.update_item(
        Key={
            'pk': 'EVENT',
            'sk': username + "#" + body['uuid']
        },
        UpdateExpression="set title=:0,description=:1,dates=:2,times=:3",
        ExpressionAttributeValues={
            ':0': body['title'],
            ':1': body['description'],
            ':2': body['dates'],
            ':3': body['times']
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

def eventsDelete(event, context):
    body = json.loads(event['body'])
    username = event['requestContext']['authorizer']['claims']['email']

    if not body.get('uuid'):
        return {
            'statusCode': 400,
            'body': 'Validation Error: Missing required keys.'
        }
    
    dynamodb.delete_item(
        Key = {
            'pk': 'EVENT',
            'sk': username + '#' + body['uuid']
        }
    )

    return {
        'statusCode': 200,
        'body': 'Success!'
    }

def handle(event, context):
    response = None

    methods = {
        'POST': {
            '/events': eventsPost
        },
        'PUT': {
            '/events': eventsPut,
            '/events/delete': eventsDelete
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
