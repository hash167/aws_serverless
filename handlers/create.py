import json
import logging
import os
from collections import Counter
import boto3
from boto3.dynamodb.conditions import Key, Attr
dynamodb = boto3.resource('dynamodb')


def batch_write(table, items):
    """
    Batch write items to given table name
    """
    with table.batch_writer() as batch:
        for item in items:
            batch.put_item(Item=item)
    return True

def create(event, context):
    data = json.loads(event['body'])
    if 'text' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't create the word item.")
        return
    if 'email' not in data:
        logging.error("Validation for email Failed")
        raise Exception("Couldn't create the word item.")
        return


    email = data["email"]
    items = {}
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    #response = table.scan()
    filtering_exp1 = Key('id').eq(email)
    try:
        query_db_for_last_location = table.query(KeyConditionExpression=filtering_exp1, ScanIndexForward=False,\
                                  Limit=1)
        no_of_items = int(query_db_for_last_location["Items"][0]["location_id"])

    except IndexError:
        no_of_items = 0


    #len(response['Items'])
    for i,word in enumerate(data['text'].split(' ')):
        dosages = ["a","t","g","c"]
        word_only_dosage = ("".join([e for e in word.lower() if e in dosages]))
        if word_only_dosage.isalpha():

            c = Counter(word_only_dosage)
            max_of_dosages = max(c.values())
            sum_of_dosages = sum(c.values())
            call = sorted(c, key= lambda x:c[x], reverse=True)
            if len(call) > 1:
                if(c[call[0]] != c[call[1]]):
                    call = call[0]
                    confidence = "{}/{}".format(max_of_dosages, sum_of_dosages)
                else:
                    call = "-"
                    confidence = 0

            else:
                call = call[0]
                confidence = "{}/{}".format(max_of_dosages, sum_of_dosages)


            # write the todo to the database
        else:

            call = "-"
            confidence = 0

        no_of_items += 1
        items[word] = {'id': email, 'text': word, 'call': call, 'confidence': confidence,
                       'location_id': no_of_items}

        #table.put_item(Item=items[word])

    # Write to Dynamodb in write batches
    if not batch_write(table,items.values()):
        logging.error("Write to Database failed")
        raise Exception("Couldn't create the word item. Database write failed")
        return


    # Create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(items) 
    }

    return response
