import boto3
import json
import os

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
        'body': json.dumps({ 'response': response })
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

    return {
        'statusCode': 200,
        'body': json.dumps({ 'response': response })
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
        'body': json.dumps({ 'response': response })
    }

def getUser(event, context):
    token = event['queryStringParameters']['token']

    cognito = boto3.client("cognito-idp", region_name="us-west-2")

    response = cognito.get_user(
        AccessToken = token
    )

    return {
        'statusCode': 200,
        'body': json.dumps({ 'response': response })
    }

def handle(event, context):
    response = None

    methods = {
        'POST': {
            '/auth/signup': signUp,
            '/auth/signupconfirm': signUpConfirm,
            '/auth/signin': signIn
        },
        'GET': {
            '/auth/user': getUser
        }
    }

    httpMethod = event['httpMethod']
    path = event['path']

    response = methods[httpMethod][path](event, context)
    
    response['headers'] = {
        'Access-Control-Allow-Origin': '*'
    }

    return response
