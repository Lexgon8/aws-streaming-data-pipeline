import json
import boto3
import base64
from datetime import datetime

s3_client = boto3.client('s3')

BUCKET_NAME = 'globalsupplydata'

def lambda_handler(event, context):

    for record in event['Records']:

        kinesis_data = record['kinesis']['data']
        decoded_data = base64.b64decode(kinesis_data).decode('utf-8')
        

        try:
            payload = json.loads(decoded_data)
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar o JSON: {e}")
            continue
        

        current_date = datetime.utcnow().strftime('%Y/%m/%d')
        

        file_name = f"iot_data/{current_date}/sensor_data_{datetime.utcnow().strftime('%H%M%S')}.json"
        

        file_content = json.dumps(payload)
        

        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=file_name,
            Body=file_content
        )


    return {
        'statusCode': 200,
        'body': json.dumps('Data processed and saved to S3')
    }

