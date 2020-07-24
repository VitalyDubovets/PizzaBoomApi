# **Backend project `PizzaBoom`**

### Tutorial for launching the project

_1. You need to install `npm` if you don't have it yet. Also you need have an account in `AWS`_

_2. After the first step install all packages with help of command:_

`npm install`

_3. Install all python packages by entering:_

`pip install -r requirements.txt`'

_4. You need to created `.env` and fill it. You may use an example `.env_example`, which located at the root directory_

_5. After created `.env` you may deploy the project. Use a bash script `./deploy.sh`_
_First parameter is `stage`. It may be `dev`, `prod` or `<your_name>` for example._
_Second parameter is `aws_profile`. You have to specify your credentials profile._

_Final view of command:_

`./deploy.sh <your_stage> <your_aws_profile_credentials>`

### AWS CloudFormation Stacks

_The project include 3 stacks of Amazon CloudFormation:_

_1. serverless-auth.yml_

_2. serverless-api.yml_

_3. serverless-order-state-machine.yml - Stack of StepFunctions service, which include describing of state machines_

#### Detailed description serverless-auth.yml

_serverless-auth.yml - Stack of authentication, authorization and registration in Amazon Cognito User Pool_

_The Stack contains:_

_1. Describing CognitoUserPool allows your user to sign up, sign in. Also allows you to control access parameters
for users_

_2. Describing IAM Role allows to configure accesses for CognitoUserPool, DynamoDB and Lambda services_

_3. Lambda Triggers include `Pre Sign Up Trigger`, `Post Confirmation Trigger`, `Post Authentication Trigger`
and `Custom Message Trigger`. You read more about lambda triggers on [AWS docs of lambda triggers]_

#### Detailed description serverless-api.yml

_serverless-api.yml - Stack of api and DynamoDB tables_

_The stack contains:_

_1. Describing JWT Authorizer for Cognito User Pool_

_2. Describing API of Flask application_

_3. Describing API of Amazon APIGateway_

_4. Describing IAM Role_

_5. Describing two table of DynamoDB: `UsersTable` and `PizzaOrdersTable`_ 

#### Detailed description serverless-order-state-machine.yml

_serverless-order-state-machine.yml - Stack of StepFunctions service, which include describing of state machines_

_The stack contains:_

_1. Describing lambda functions, which used in step functions_

_2. Describing state machines. The project has two state machine: СookingStateMachine, which is responsible
for the pizza cooking process, and PrepareFillingStateMachine, which is responsible for the pizza filling process_

_3. Describing two IAM role: base `ExecutionRole` and additional for step functions `StepFunctionsExecutionRole`_

#### Documentation of modules in the form of diagrams

_[Documentation of modules]_


[AWS docs of lambda triggers]: https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools-working-with-aws-lambda-triggers.html

[Documentation of modules]: https://miro.com/app/board/o9J_ko6HDaM=/