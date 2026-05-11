import json
import random
import boto3
from datetime import datetime

kinesis_client = boto3.client('kinesis')

def generate_warehouse_event():
    return {
        'sensor_type': 'warehouse',
        'warehouse_id': f"WH-{random.randint(1, 6)}",
        'temperature': round(random.uniform(10, 30), 2),
        'humidity': round(random.uniform(30, 70), 2),
        'timestamp': datetime.utcnow().isoformat()
    }

def generate_vehicle_event():
    return {
        'sensor_type': 'vehicle',
        'vehicle_id': f"VH-{random.randint(1, 6)}",
        'speed': round(random.uniform(30, 120), 2),
        'fuel_level': round(random.uniform(5, 100), 2),
        'gps_location': {
            'latitude': round(random.uniform(-90, 90), 6),
            'longitude': round(random.uniform(-180, 180), 6)
        },
        'timestamp': datetime.utcnow().isoformat()
    }


STREAM_NAME = 'iot'

def lambda_handler(event, context):

    sensor_type = random.choices(
        ['warehouse', 'vehicle'],
        weights=[70, 30]
    )[0]

    if sensor_type == 'warehouse':
        sensor_data = generate_warehouse_event()
    else:
        sensor_data = generate_vehicle_event()

    sensor_data_json = json.dumps(sensor_data)

    response = kinesis_client.put_record(
        StreamName=STREAM_NAME,
        Data=sensor_data_json,
        PartitionKey=str(random.randint(1, 1000))
    )

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Data sent to Kinesis',
            'sensor_data': sensor_data,
            'kinesis_response': response
        })
    }
