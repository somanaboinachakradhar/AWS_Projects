## Serverless Login and Registration System
A serverless web application for user login and registration, built using AWS services (S3, API Gateway, Lambda, DynamoDB) and styled with Tailwind CSS. This project was developed as a student project to gain hands-on experience with serverless architecture, AWS services, and front-end development.


Features

User registration with full name, username, and password.
User login with username and password validation.
Redirects to a welcome page upon successful login.
Error handling for incorrect credentials and duplicate usernames.
Styled with Tailwind CSS for a clean, responsive UI.
Serverless back-end using AWS Lambda and API Gateway.
Data storage in DynamoDB with a Users table.

Screenshots
Login Page
  see screenshots/loginpage.png

Registration Page
  see screenshots/register.png
Welcome Page
    see screenshots/welcome.png
Architecture
This project follows a serverless architecture with the following components:

Front-End: Static HTML files (login.html, register.html, welcome.html) hosted on Amazon S3, styled with Tailwind CSS (via CDN).
Back-End:
API Gateway: Handles HTTP requests (/login and /register) and routes them to Lambda functions.
Lambda Functions: Two Python functions (LoginFunction, RegisterFunction) handle login and registration logic.
DynamoDB: Stores user data in a Users table with username as the partition key.


IAM Role: A custom role (LambdaDynamoDBRole) grants Lambda functions access to DynamoDB and CloudWatch Logs.
CORS: Configured in API Gateway to allow cross-origin requests from the S3-hosted front-end.

Architecture Diagram
[User] --> [S3 Static Website]
                  |
                  v
[API Gateway] --> [Lambda Functions] --> [DynamoDB]

Project Structure
login-registration-system/
├── frontend/
│   ├── login.html          # Login page
│   ├── register.html       # Registration page
│   └── welcome.html        # Welcome page
├── backend/
│   ├── login_function.py   # Lambda function for login (LoginFunction)
│   └── register_function.py # Lambda function for registration (RegisterFunction)
├── infrastructure/
│   ├── api_gateway_setup.md # API Gateway setup instructions
│   ├── dynamodb_setup.md    # DynamoDB setup instructions
│   └── iam_role_setup.md    # IAM role setup instructions
├── screenshots/
│   ├── login_page.png       # Screenshot of login page
│   ├── register_page.png    # Screenshot of registration page
│   └── welcome_page.png     # Screenshot of welcome page
└── README.md               # Project documentation

Setup Instructions
To replicate this project, follow these steps. Note: This project uses AWS services, so an AWS account is required. Stay within the Free Tier to avoid charges.
Prerequisites

AWS account with access to S3, API Gateway, Lambda, DynamoDB, and IAM.
Basic knowledge of HTML, JavaScript, Python, and AWS services.
Local setup: Git and a code editor (e.g., VS Code) to manage files.

1. Set Up IAM Role

Create an IAM role (LambdaDynamoDBRole) to grant Lambda functions permissions to access DynamoDB and write logs to CloudWatch.
Attach the AWSLambdaBasicExecutionRole and AmazonDynamoDBFullAccess policies.
See infrastructure/iam_role_setup.md for detailed steps.

2. Set Up DynamoDB

Create a DynamoDB table named Users with username as the partition key (String).
Optionally, add a test user (e.g., username: testuser, name: Test User, password: testpass).
See infrastructure/dynamodb_setup.md for detailed steps.

3. Set Up Lambda Functions

Create Lambda Functions:
Create two Lambda functions: LoginFunction and RegisterFunction.
Set the runtime to Python 3.x.
Attach the LambdaDynamoDBRole IAM role to both functions.


Upload Code:
For LoginFunction, upload the code from backend/login_function.py.
For RegisterFunction, upload the code from backend/register_function.py.


Test the Functions:
Test LoginFunction with:{
    "body": "{\"username\": \"testuser\", \"password\": \"testpass\"}"
}


Expected response: {"message": "Hey, welcome!"}


Test RegisterFunction with:{
    "body": "{\"name\": \"New User\", \"username\": \"newuser\", \"password\": \"newpass\"}"
}


Expected response: {"message": "Registration successful"}





4. Set Up API Gateway

Create an API (LoginAppAPI) with /login and /register resources.
Add POST methods to invoke the respective Lambda functions (LoginFunction, RegisterFunction).
Add OPTIONS methods for CORS with the following headers:
Access-Control-Allow-Origin: '*'
Access-Control-Allow-Headers: Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token
Access-Control-Allow-Methods: OPTIONS,POST


Deploy the API to the prod stage and note the invoke URL (e.g., https://vrto2y1edb.execute-api.ap-south-1.amazonaws.com/prod).
See infrastructure/api_gateway_setup.md for detailed steps.

5. Set Up S3 for Static Website Hosting

Create an S3 Bucket:
Create a bucket named my-login-app-2025 (or a unique name of your choice).
Region: ap-south-1 (Mumbai).


Upload Files:
Upload the files from frontend/ (login.html, register.html, welcome.html) to the bucket.


Enable Static Website Hosting:
Go to the bucket’s Properties tab.
Enable Static website hosting.
Set the Index document to login.html.
Note the website endpoint (e.g., http://my-login-app-2025.s3-website-ap-south-1.amazonaws.com).


Set Bucket Policy for Public Access:
Go to the Permissions tab.
Edit the Bucket policy and add:{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::my-login-app-2025/*"
        }
    ]
}


Save the policy.



6. Test the Application

Access the S3 website URL (e.g., http://my-login-app-2025.s3-website-ap-south-1.amazonaws.com).
Register a new user (e.g., name: Test User, username: testuser, password: testpass).
Log in with the credentials to verify redirection to welcome.html.

Usage

Open the S3 website URL in a browser.
Register:
Navigate to the registration page via the "Register" link.
Enter your full name, username, and password, then click Register.
On success, you’ll see “Registration successful” and be redirected to the login page after 2 seconds.
If the username exists, you’ll see “Username already exists”.


Login:
Enter your username and password, then click Login.
On success, you’ll see “Hey, welcome!” and be redirected to welcome.html after 2 seconds.
If the password is incorrect, you’ll see “Incorrect password”.



Security Notes

Plain Text Passwords: Passwords are stored in plain text in DynamoDB, which is insecure for production. In a real application, use AWS Cognito for authentication or hash passwords with bcrypt.
HTTP: The S3 website uses HTTP. For production, use Amazon CloudFront to enable HTTPS.
Demo Project: This is a student project for learning purposes and not intended for production use.

Challenges Faced

CORS Issues: Encountered CORS errors when the front-end made API calls to API Gateway. Resolved by configuring OPTIONS methods with proper CORS headers in API Gateway.
AWS Free Tier: Ensured all resources stayed within the Free Tier to avoid charges, such as using on-demand capacity for DynamoDB and minimizing API Gateway requests.
Debugging: Used CloudWatch Logs to troubleshoot Lambda function errors and API Gateway logs to verify CORS headers.

Technologies Used

Front-End: HTML, JavaScript, Tailwind CSS (via CDN)
Back-End: AWS Lambda (Python 3.x), API Gateway
Database: DynamoDB
Hosting: Amazon S3 (static website hosting)
Security: AWS IAM (custom role for Lambda)

Future Improvements

Add HTTPS support using Amazon CloudFront.
Implement secure password storage with AWS Cognito or password hashing.
Add user session management (e.g., using JWT tokens).
Improve error handling and UI feedback (e.g., loading spinners, better form validation).
Optimize AWS costs by using a more restrictive IAM policy (least privilege) for Lambda.

Clean Up Resources
To avoid AWS charges after completing the project:

S3 Bucket:
Go to S3 > my-login-app-2025 > Empty > Delete.

DynamoDB Table:
Go to DynamoDB > Users table > Delete.

Lambda Functions:
Go to Lambda > LoginFunction and RegisterFunction > Actions > Delete.

API Gateway:
Go to API Gateway > LoginAppAPI > Actions > Delete API.

IAM Role:
Go to IAM > Roles > LambdaDynamoDBRole > Delete.

License
This project is licensed under the MIT License.
Contact
Feel free to reach out for questions or collaboration:

GitHub: [somanaboinachakradhar]
LinkedIn: [www.linkedin.com/in/chakri-somanaboina-53b513329]

