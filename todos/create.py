import json
import logging
import os
import time
import uuid

import boto3
dynamodb = boto3.resource('dynamodb')


def create(event, context):
    data = json.loads(event['body'])
    if 'text' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't create the todo item.")
        return

    timestamp = int(time.time() * 1000)
    items = {}   
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    for word in data['text'].split(' '):
        items[word] = {'id': str(uuid.uuid1()),'text': word, 'checked': False,'createdAt': timestamp,'updatedAt': timestamp}
	#items.append(item)
        # write the todo to the database
        table.put_item(Item=items[word])
	#items[word] = json.dumps(item)

    # create a response
    #items = {k: items[k] for key in items.keys()}
    response = {
        "statusCode": 200,
        "body": json.dumps(items) 
    }

    return response
