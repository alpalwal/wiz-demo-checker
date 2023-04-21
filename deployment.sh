terraform plan
terraform apply --auto-approve

aws lambda invoke \
--function-name demo_checker \
--payload '{ "hello": "world" }' \
--cli-binary-format raw-in-base64-out \
--region us-west-1 \
--log-type Tail \
--query 'LogResult' \
response.json | sed s/\"//g  | base64 -d | egrep -vi 'botocore|Deprecation'

