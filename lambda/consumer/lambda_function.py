def lambda_handler(event, context):

    for record in event['Records']:

        kinesis_data = record['kinesis']['data']
        decoded_data = base64.b64decode(kinesis_data).decode('utf-8')

        try:
            payload = json.loads(decoded_data)

        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar JSON: {e}")
            continue

        now = datetime.utcnow()

        year = now.strftime("%Y")
        month = now.strftime("%m")
        day = now.strftime("%d")

        file_name = (
            f"raw/iot/"
            f"year={year}/"
            f"month={month}/"
            f"day={day}/"
            f"evento.json"
        )

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
