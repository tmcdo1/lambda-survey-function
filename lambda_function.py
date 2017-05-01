import os
import urllib
import random

import boto3

from boto3.session import Session
from boto3.dynamodb.conditions import Key
from twilio.twiml.messaging_response import MessagingResponse

# Add S3 and DynamoDB session
s3 = boto3.resource('s3')
session = Session()

# Add Twilio credentials
account_sid = os.environ['ACCOUNT_SID']
auth_token = os.environ['AUTH_TOKEN']

# Add DynamoDB
dynamodb = boto3.resource('dynamodb','us-west-2')
table_users = dynamodb.Table('Vize-Survey-Table')

def lambda_handler(event, context):
    response = MessagingResponse()
    print('Event:', event)

    message = event['Body']
    from_number = event['From']

    dynamo_response = table_users.query(KeyConditionExpression = Key('User_ID').eq(from_number))

    if dynamo_response['Count'] == 0:
        table_users.put_item(Item={'User_ID': from_number, })
        response.message("Hello, welcome to this Vize survey")
        return str(response)
    else:
        response.message("Welcome back!")
        return str(response)