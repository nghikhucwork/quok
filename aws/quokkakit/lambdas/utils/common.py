from __future__ import print_function
import uuid
from datetime import datetime
from boto3.dynamodb.conditions import Key

pagesize = 5
rootSrc = "QUOKKA"

def getValueOfTimeStartDay(time: datetime):
    """Function get timestamp early in the day."""
    return time.replace(hour=0, minute=0, second=0, microsecond=0).timestamp()

def getValueOfTimeEndDay(time: datetime):
    """Function get timestamp by the end of day."""
    return time.replace(hour=23, minute=59, second=59, microsecond=0).timestamp()

def scanAllPagination(page = 1, table:any = None):
    """Function get notes."""

    remain_page = page
    result = []

    scan_kwargs = {
        "IndexName": 'src_idx',
        "Limit": pagesize,
        "KeyConditionExpression": Key('src').eq(rootSrc),
        "ScanIndexForward": False,
    }

    try:
        done = False
        start_key = None
        while not done:
            if start_key:
                scan_kwargs["ExclusiveStartKey"] = start_key

            response = table.query(**scan_kwargs)
            start_key = response.get("LastEvaluatedKey", None)
            done = start_key is None
            
            if remain_page == 1: 
                done = True
                result.extend(response.get("Items", []))

            remain_page -= 1

    except Exception as err:
        print(err)
        raise Exception("Batch error")

    return result


def queryPaginationByUsername(page = 1, username: str = '' ,table:any = None):
    """Function get notes by username."""

    remain_page = page
    result = []
    scan_kwargs = {
        "IndexName": 'username_idx',
        "Limit": pagesize,
        "KeyConditionExpression": Key('username').eq(username),
        "ScanIndexForward": False,
    }

    try:
        done = False
        start_key = None
        while not done:
            if start_key:
                scan_kwargs["ExclusiveStartKey"] = start_key

            response = table.query(**scan_kwargs)
            start_key = response.get("LastEvaluatedKey", None)
            done = start_key is None
            
            if remain_page == 1: 
                done = True
                result.extend(response.get("Items", []))

            remain_page -= 1

    except Exception as err:
        print(err)
        raise Exception("Batch error")

    return result

def putNoteItem(item:any, table:any):
    """Create note."""
    payload = {
                'id': str(uuid.uuid4()),
                'content': item.get('content', '---'),
                'timestamp': int(datetime.utcnow().timestamp()),
                'username': item.get('username', 'empty'),
                'src': rootSrc
            }
    table.put_item(Item=payload)
    return payload
        