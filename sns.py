import boto3
from botocore.exceptions import ClientError

# Get the service resource.
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('dwarcash_stud')
client = boto3.client('dynamodb')

client_sns = boto3.client(
    "sns",
    aws_access_key_id="",
    aws_secret_access_key="",
    region_name="us-west-2"
)

def getStudById(enroll_no):
    response = table.get_item(
    Key={
        'enroll_no': enroll_no
    })
    item = response['Item']
    list = [(k, v) for k, v in item.items()]
    email = (list[1][1])
    send_plain_email(email)
    return {"code":200, "message":item}

def send_email_all():
    topic_arn = ""
    client_sns.publish(TopicArn=topic_arn, 
            Message="Hello from Dwarcash", 
            Subject="Hello from Dwarcash")
    return {"code":200, "message":"Mail sent to all successfully ✅"}
    

  
def verify_email_identity(email):
    ses_client = boto3.client("ses", region_name="us-west-2")
    response = ses_client.verify_email_identity(
        EmailAddress=email
    )
    print(response)

def send_plain_email(email):
    ses_client = boto3.client("ses", region_name="us-west-2")
    CHARSET = "UTF-8"

    response = ses_client.send_email(
        Destination={
            "ToAddresses": [
                email,
            ],
        },
        Message={
            "Body": {
                "Text": {
                    "Charset": CHARSET,
                    "Data": "Hello, world!",
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": "Hello from dwarcash",
            },
        },
        Source="dwarkeshkaswala777@gmail.com",
    )

def lambda_handler(event, context):
    if (event['option'] == 'broadcast'):    
        return send_email_all()
    else:
        enroll_no = event['option']
        return getStudById(enroll_no)
