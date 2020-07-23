# **Backend project `PizzaBoom`**

## Tutorial for launching the project

_1. You need to install `npm` if you don't have it yet. Also you need have an account in `AWS`_

_2. After the first step install all packages with help of command:_

`npm install`

_3. Install all python packages by entering:_

`pip install -r requirements.txt`'

_4. You need to created `.env` and fill it. You may use an example in the file `.env_example`_

_5. After created `.env` you may deploy the project. Use a bash script `./deploy.sh`_
_First parameter is `stage`. It may be `dev`, `prod` or `<your_name>` for example._
_Second parameter is `aws_profile`. You have to specify your credentials profile._

_Final view of command:_

`./deploy.sh <your_stage> <your_aws_profile_credentials>`



