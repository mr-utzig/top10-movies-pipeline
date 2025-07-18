import json
import boto3
import requests
import os
from datetime import datetime

OMDB_API_KEY = os.environ['OMDB_API_KEY']
DEST_BUCKET = os.environ['DEST_BUCKET']

def lambda_handler(event, context):
    s3 = boto3.client('s3')

    for record in event['Records']:
        movie = json.loads(record['body'])
        imdb_id = movie['id']

        response = requests.get(f"https://www.omdbapi.com/?apikey={OMDB_API_KEY}&i={imdb_id}")
        omdb_data = response.json()

        movie['omdb'] = omdb_data

        filename = f\"{movie['id']}_{datetime.utcnow().isoformat()}.json\"
        
        s3.put_object(
            Bucket=DEST_BUCKET,
            Key=filename,
            Body=json.dumps(movie),
            ContentType='application/json'
        )

    return {
        'statusCode': 200,
        'body': 'Movie enriched and stored'
    }
