import boto3
import json
import os

if os.getenv('AWS_SAM_LOCAL'):
    dynamodb = boto3.resource('dynamodb', endpoint_url = 'http://dynamodb-local:8000').Table('system')
else:
    dynamodb = boto3.resource('dynamodb').Table('system')

def eventsPost(event, context):
    body = json.loads(event['body'])

    return {
        'statusCode': 200,
        'body': json.dumps({ 'response': 'Success!' })
    }

def eventsGet(event, context):
    username = event['requestContext']['authorizer']['claims']['email']

    response = dynamodb.get_item(
        Key = {
            'pk': 'EVENT',
            'sk': username
        }
    )

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
