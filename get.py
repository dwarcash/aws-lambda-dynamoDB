import boto3

# Get the service resource.
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('dwarcash_stud')
client = boto3.client('dynamodb')

def dump_table(table_name):
    results = []
    last_evaluated_key = None
    while True:
        if last_evaluated_key:
            response = client.scan(
                TableName=table_name,
                ExclusiveStartKey=last_evaluated_key
            )
        else: 
            response = client.scan(TableName=table_name)
        last_evaluated_key = response.get('LastEvaluatedKey')
        
        results.extend(response['Items'])
        
        if not last_evaluated_key:
            break
    return results
    
def getStudById(enroll_no):
    response = table.get_item(
    Key={
        'enroll_no': enroll_no
    })
    item = response['Item']
    list = [(k, v) for k, v in item.items()]
    email = (list[1][1])
    return {"code":200, "message":item}
    
    
def lambda_handler(event, context):
    if event:
        return getStudById(event['enroll_no'])
    else:
        return dump_table('dwarcash_stud')

