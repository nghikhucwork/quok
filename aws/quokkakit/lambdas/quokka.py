from __future__ import print_function
import json
import os
import boto3
import utils.common as common
# Get the service resource.
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

# set environment variable

def lambda_handler(event = {}, context = {}):

    try:
        payload_json = dict(event).get('body', dict())
        payload = json.loads(payload_json)
        body = payload.get('body', dict())
        query = payload.get('query', dict())
        method = payload.get('method', 'GET')

        table = dynamodb.Table(os.environ['NoteItemsTable'])

        if method == 'GET':
            page = query.get('page', 1)

            data = []

            username = query.get('username', None)
            if bool(username):
                data = common.queryPaginationByUsername(page, username, table)
            else: data = common.scanAllPagination(page, table)
            return {"data": data, "httpCode": 200}

        if  not bool(body.get('content', None)) or not bool(body.get('username', None)):
                raise Exception("Method POST, Body missing fields")

        if method == 'POST':
            item = common.putNoteItem(body, table)
            
            return {"httpCode": 200, "data": item}
        
        raise Exception("Nothing")
    except Exception as err:
        return {"statusCode": 400, 'body': {"error": str(err)} }