import boto3
import json
import os

if os.getenv('AWS_SAM_LOCAL'):
    dynamodb = boto3.resource('dynamodb', endpoint_url = 'http://dynamodb-local:8000').Table('system')
else:
    dynamodb = boto3.resource('dynamodb').Table('system')

def usersGet(event, context):
    username = event['requestContext']['authorizer']['claims']['email']

    user = dynamodb.get_item(Key = { 'pk': 'USER', 'sk': username }).get('Item')

    user.pop('pk')
    user.pop('sk')

    return {
        'statusCode': 200,
        'body': json.dumps(user)
    }

def usersPut(event, context):
    body = json.loads(event['body'])
    username = event['requestContext']['authorizer']['claims']['email']

    required_keys = ['firstname', 'lastname', 'email', 'phone']

    if not all(body.get(key) for key in required_keys):
        return {
            'statusCode': 400,
            'body': 'Validation Error: Missing required keys.'
        }

    response = dynamodb.update_item(
        Key = {
            'pk': 'USER',
            'sk': username
        },
        UpdateExpression="set firstname=:0,lastname=:1,email=:2,phone=:3",
        ExpressionAttributeValues={
            ':0': body['firstname'],
            ':1': body['lastname'],
            ':2': body['email'],
            ':3': body['phone']
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }

def handle(event, context):
    response = None

    methods = {
        'GET': usersGet,
        'PUT': usersPut
    }

    httpMethod = event['httpMethod']

    response = methods[httpMethod](event, context)
    
    response['headers'] = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
    }

    return response
