## Configuring the DynamoDB Back-End
 ******more details to come 
  
Two options exists for accessing DynamoDB
1) Create a free AWS account and create a user with access to DynamoDB (recommended).
2) Host an instance of DynamoDB yourself with Docker (useful for  development and testing).
 
By default, dNote tries to connect to AWS servers, but you can specify the location of your local instance as an environment variable:
```bash
DNOTE_DYNAMODB_ENDPOINT = 'http://localhost:8000'
```

or in ~/.dnote.yml

```yaml
dynamodb_endpoint: 'http://localhost:8000'
```
 
