API Gateway Setup Instructions

This document provides step-by-step instructions to set up an API Gateway for the serverless login and registration system project. The API Gateway handles HTTP requests from the front-end (hosted on S3) and routes them to Lambda functions (LoginFunction and RegisterFunction) for processing. Additionally, CORS is configured to allow cross-origin requests from the S3-hosted website.

Step 1: Create the API

Log into AWS Console:

Open the AWS Management Console (https://console.aws.amazon.com/).

Search for API Gateway in the search bar and select it.

Create a New API:

Click Create API.

Choose REST API (not HTTP API) > Build.

Note: REST API is used here because it provides more flexibility for CORS configuration, which is necessary for this project.

API Name: Enter LoginAppAPI.

Description (optional): "API for login and registration system."

Endpoint Type: Select Regional.

Click Create API.

Step 2: Create Resources

You need to create two resources: /login and /register, which will handle the login and registration requests.


Create the /login Resource:


In the API Gateway console, under Resources, click Actions > Create Resource.

Resource Name: login

Resource Path: /login (auto-filled based on the name).

Leave "Enable API Gateway CORS" unchecked (we’ll configure CORS manually for more control).

Click Create Resource.

Create the /register Resource:


Repeat the process:

Click Actions > Create Resource.

Resource Name: register

Resource Path: /register.

Click Create Resource.

Step 3: Create Methods for /login

The /login resource needs two methods: POST (to handle login requests) and OPTIONS (for CORS preflight requests).

3.1: Create the POST Method for /login

Select the /login Resource:

In the Resources tree, click on /login.

Create the POST Method:

Click Actions > Create Method.

From the dropdown, select POST and click the checkmark.

Integration Type: Choose Lambda Function.

Lambda Region: Select ap-south-1 (or your region).

Lambda Function: Select LoginFunction (ensure this function exists in Lambda).

Check Use Lambda Proxy integration.

Click Save.

If prompted, grant API Gateway permission to invoke the Lambda function by clicking OK.

Test the POST Method (Optional):

Click on the POST method.

In the Method Execution view, click Test.

In the Request Body, enter:

{
    "username": "testuser",
    "password": "testpass"
}

Click Test. You should see a response like {"message": "Hey, welcome!"} if the Lambda function and DynamoDB are set up correctly.

3.2: Create the OPTIONS Method for /login (CORS)

The OPTIONS method handles the browser’s preflight request to check if the POST request is allowed (CORS).

Create the OPTIONS Method:

With /login selected, click Actions > Create Method.

From the dropdown, select OPTIONS and click the checkmark.

Integration Type: Choose Mock (no Lambda function is needed for OPTIONS; it just returns CORS headers).

Click Save.

Configure the Integration Response for OPTIONS:

Click on the OPTIONS method.

Go to the Integration Response tab.

Expand HTTP Status Code 200.

Under HTTP Headers, click Add Header to add the following:

Name: Access-Control-Allow-Origin, Value: '*'

Name: Access-Control-Allow-Headers, Value: Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token

Name: Access-Control-Allow-Methods, Value: OPTIONS,POST

Save the changes.

Configure the Method Response for OPTIONS:

Go to the Method Response tab.

Expand HTTP Status 200.

Under Response Headers, add the same headers as above:

Access-Control-Allow-Origin

Access-Control-Allow-Headers

Access-Control-Allow-Methods

Save the changes.

Step 4: Create Methods for /register

Repeat the process for the /register resource.

4.1: Create the POST Method for /register

Select the /register Resource:

In the Resources tree, click on /register.

Create the POST Method:

Click Actions > Create Method.

Select POST and click the checkmark.

Integration Type: Lambda Function.

Lambda Region: ap-south-1.

Lambda Function: RegisterFunction.

Check Use Lambda Proxy integration.

Click Save and grant permissions if prompted.

Test the POST Method (Optional):

Click on the POST method.

In the Method Execution view, click Test.

In the Request Body, enter:

{
    "name": "New User",
    "username": "newuser",
    "password": "newpass"
}

Click Test. You should see a response like {"message": "Registration successful"}.

4.2: Create the OPTIONS Method for /register (CORS)

Create the OPTIONS Method:

With /register selected, click Actions > Create Method.

Select OPTIONS and click the checkmark.

Integration Type: Mock.

Click Save.

Configure the Integration Response for OPTIONS:

Go to the Integration Response tab.

Expand HTTP Status Code 200.

Add the following headers:

Name: Access-Control-Allow-Origin, Value: '*'

Name: Access-Control-Allow-Headers, Value: Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token

Name: Access-Control-Allow-Methods, Value: OPTIONS,POST

Save the changes.

Configure the Method Response for OPTIONS:

Go to the Method Response tab.

Expand HTTP Status 200.

Add the same headers as above.

Save the changes.

Step 5: Enable CORS (Optional Double-Check)

API Gateway has a shortcut to enable CORS, but we’ve manually configured it for more control. To double-check:

Select the /login resource.

Click Actions > Enable CORS.
Verify the headers match the ones above.

Repeat for /register.

If prompted to overwrite existing headers, choose Yes.

Step 6: Deploy the API

Create a Stage:

Click Actions > Deploy API.

Deployment Stage: Select New Stage.

Stage Name: prod.

Stage Description (optional): "Production stage for login and registration API."

Click Deploy.

Note the Invoke URL:

After deployment, go to Stages > prod.

Note the Invoke URL, e.g., https://vrto2y1edb.execute-api.ap-south-1.amazonaws.com/prod.

The full endpoints will be:

/login: https://vrto2y1edb.execute-api.ap-south-1.amazonaws.com/prod/login

/register: https://vrto2y1edb.execute-api.ap-south-1.amazonaws.com/prod/register

Step 7: Test the API Endpoints

Use a tool like curl or Postman to test the endpoints:

Test /login:

curl -X POST https://vrto2y1edb.execute-api.ap-south-1.amazonaws.com/prod/login \
-H "Content-Type: application/json" \
-d '{"username": "testuser", "password": "testpass"}'

Expected response: {"message": "Hey, welcome!"}

Test /register:

curl -X POST https://vrto2y1edb.execute-api.ap-south-1.amazonaws.com/prod/register \
-H "Content-Type: application/json" \
-d '{"name": "New User", "username": "newuser", "password": "newpass"}'

Expected response: {"message": "Registration successful"}

Test CORS with OPTIONS:

curl -X OPTIONS https://vrto2y1edb.execute-api.ap-south-1.amazonaws.com/prod/login -v

Look for headers in the response:

Access-Control-Allow-Origin: *

Access-Control-Allow-Headers: Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token

Access-Control-Allow-Methods: OPTIONS,POST

Troubleshooting Tips

CORS Errors: If the front-end (S3 website) shows CORS errors, double-check the OPTIONS method headers.

Lambda Errors: If the POST method fails, check the Lambda function logs in CloudWatch.

Redeploy After Changes: Always redeploy the API to the prod stage after making changes.

Notes

Region: This setup uses the ap-south-1 region. Adjust the region as needed.

CORS: The CORS headers are critical for allowing requests from the S3-hosted front-end (http://my-login-app-2025.s3-website-ap-south-1.amazonaws.com).

Security: For production, consider adding API Gateway authorization (e.g., API keys, IAM roles, or AWS Cognito).
