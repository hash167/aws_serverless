import os
import json
import logging

from handlers import decimalencoder
import boto3
from boto3.dynamodb.conditions import Key, Attr
dynamodb = boto3.resource('dynamodb')


def get(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    location_id = event['pathParameters']['location_id']
    id = event['pathParameters']['id']

    filtering_exp1 = Key('id').eq(id)
    filtering_exp2 = Key('location_id').eq(int(location_id))

    result = table.query(KeyConditionExpression=filtering_exp1 & filtering_exp2)

    test = table.query(KeyConditionExpression=filtering_exp1, ScanIndexForward=False, Limit=1)
    logging.error("Value of test",test["Items"][0])


    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(test,#result["Items"],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
