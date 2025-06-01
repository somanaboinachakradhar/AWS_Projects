import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Users')

    headers = {
        "Access-Control-Allow-Origin": "*",  # adjust for your domain in production
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "POST"
    }

    try:
        # Parse incoming request body (Lambda proxy integration)
        body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        username = body['username']
        password = body['password']

        # Get user from DynamoDB
        response = table.get_item(Key={'username': username})
        if 'Item' not in response:
            return {
                'statusCode': 401,
                'headers': headers,
                'body': json.dumps({'message': 'User not found'})
            }

        stored_password = response['Item'].get('password')

        # Plain text password check (for testing ONLY!)
        if password == stored_password:
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({'message': 'Hey, welcome!'})
            }
        else:
            return {
                'statusCode': 401,
                'headers': headers,
                'body': json.dumps({'message': 'Incorrect password'})
            }

    except KeyError as e:
        return {
            'statusCode': 400,
            'headers': headers,
            'body': json.dumps({'message': f'Missing field: {str(e)}'})
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'message': f'Database error: {str(e)}'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'message': f'Unexpected error: {str(e)}'})
        }
