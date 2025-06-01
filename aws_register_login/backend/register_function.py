import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Users')

    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "POST"
    }

    try:
        body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        name = body['name']
        username = body['username']
        password = body['password']

        response = table.get_item(Key={'username': username})
        if 'Item' in response:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'message': 'Username already exists'})
            }

        # WARNING: Plain text password storage for testing only!
        table.put_item(Item={
            'username': username,
            'name': name,
            'password': password
        })

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'message': 'Registration successful'})
        }

    except KeyError as e:
        return {
            'statusCode': 400,
            'headers': headers,
            'body': json.dumps({'message': f'Missing required field: {str(e)}'})
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'message': f'Server error: {str(e)}'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'message': f'Unexpected error: {str(e)}'})
        }
