import boto3
import json
import os

if os.getenv('AWS_SAM_LOCAL'):
    dynamodb = boto3.resource('dynamodb', endpoint_url = 'http://dynamodb-local:8000').Table('system')
else:
    dynamodb = boto3.resource('dynamodb').Table('system')

def signUp(event, context):
    body = json.loads(event['body'])

    username = body['username']
    password = body['password']

    cognito = boto3.client("cognito-idp", region_name="us-west-2")

    response = cognito.sign_up(
        ClientId=os.environ["COGNITO_CLIENT_ID"],
        Username=username,
        Password=password
    )

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }

def signUpConfirm(event, context):
    body = json.loads(event['body'])

    username = body['username']
    code = body['code']

    cognito = boto3.client("cognito-idp", region_name="us-west-2")

    response = cognito.confirm_sign_up(
        ClientId=os.environ["COGNITO_CLIENT_ID"],
        Username=username,
        ConfirmationCode=code
    )

    dynamodb.put_item(
        Item = {
            'pk': 'USER',
            'sk': username,
            'email': username,
            'firstname': None,
            'lastname': None,
            'phone': None
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }

def signIn(event, context):
    body = json.loads(event['body'])

    username = body['username']
    password = body['password']

    cognito = boto3.client("cognito-idp", region_name="us-west-2")

    response = cognito.initiate_auth(
        ClientId=os.environ["COGNITO_CLIENT_ID"],
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={
            "USERNAME": username,
            "PASSWORD": password
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }

def signOut(event, context):
    body = json.loads(event['body'])

    access_token = body['accessToken']

    cognito = boto3.client("cognito-idp", region_name="us-west-2")

    response = cognito.global_sign_out(
        AccessToken=access_token
    )

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }

def getUser(event, context):
    token = event['queryStringParameters']['token']

    cognito = boto3.client("cognito-idp", region_name="us-west-2")

    response = cognito.get_user(
        AccessToken = token
    )

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }

def handle(event, context):
    response = None

    methods = {
        'POST': {
            '/auth/signup': signUp,
            '/auth/signupconfirm': signUpConfirm,
            '/auth/signin': signIn,
            '/auth/signout': signOut
        },
        'GET': {
            '/auth/user': getUser
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
