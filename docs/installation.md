# cNote Installation

cNote is written in Python and uses AWS DynamoDB as a back-end to store and manage the notes. Further details about configuring DynamoDB are described [below](#config_dynamodb)

## Dependencies

* Python3 (>=3.6)
* AWS DynamoDB

## Installation

The latest stable release of cNote can be installed with [pip](https://pip.pypa.io/en/stable/) (recommended).
 
```bash
python -m pip install cnote
```

Alternatively, cNote can be installed from source:
```bash
git clone "https://github.com/yetisir/cnote"
python -m pip install -e .
```

## <a name='config_dynamodb'></a>Configuring DynamoDB  
Two options exists to configure DynamoDB. We can either use AWS hosted DynamoDB (reccomended) or host an instance of DynamoDB locally.

### AWS
Create a free AWS account and create a user with access to DynamoDB (recommended) and set up your AWS credentials for the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)

### Local
You may also host an instance of DynamoDB yourself with Docker (useful for development and testing).

```
docker run -p 8000:8000 amazon/dynamodb-local
```
 
By default, cNote tries to connect to AWS servers, but you can specify the location of your local instance in ~/.cnote.yml

```yaml
aws_endpoint: 'http://localhost:8000'
```
 
