import json
import urllib.request
import boto3
import os

SQS_QUEUE_URL = os.environ['SQS_QUEUE_URL']

def lambda_handler(event, context):
    url = "https://top-movies.s3.eu-central-1.amazonaws.com/Top250Movies.json"
    
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read())

    top_10 = data['items'][:10]

    sqs = boto3.client('sqs')

    for movie in top_10:
        sqs.send_message(
            QueueUrl=SQS_QUEUE_URL,
            MessageBody=json.dumps(movie)
        )

    return {
        "statusCode": 200,
        "body": "Top 10 movies sent to SQS"
    }
