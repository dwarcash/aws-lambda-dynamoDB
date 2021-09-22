import boto3

# Get the service resource.
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('dwarcash_stud')

#SNS
client = boto3.client(
    "sns",
    aws_access_key_id="",
    aws_secret_access_key="",
    region_name="us-west-2"
)

#SES
def verify_email_identity(email):
    ses_client = boto3.client("ses", region_name="us-west-2")
    response = ses_client.verify_email_identity(
        EmailAddress=email
    )
    print(response)
    
def convert_empty_values(dictOrList):  
    if isinstance(dictOrList, dict):
        for key, value in dictOrList.items():
            if isinstance(value, dict) | isinstance(value, list):
                convert_empty_values(value)
            elif value == "":
                dictOrList[key] = None
    elif isinstance(dictOrList, list):
        for value in dictOrList:
            if isinstance(value, dict) | isinstance(value, list):
                convert_empty_values(value)
            elif value == "":
                dictOrList.remove(value)
                dictOrList.append(None)
    return dictOrList
    
    
def lambda_handler(event, context):
    cleaned_data = convert_empty_values(event)
    table.put_item(Item=cleaned_data)
    topic_arn = "arn:aws:sns:us-west-2:971549186174:dwarcash_stud_mail"
    email=event['email']
    
    #SNS
    client.subscribe(
        TopicArn=topic_arn,
        Protocol='email',
        Endpoint=email  
    )
    
    #SES
    verify_email_identity(email)
    
    return {"code":200, "message":f'Student Added Successfully - {email}'}
    
