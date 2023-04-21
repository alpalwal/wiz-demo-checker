# wiz-demo-checker

## What it does

This is a function that runs to help keep an eye on the demo environment. We can load multiple different test cases in and report back when things aren't looking "normal" in the env. 

## What it creates
The terraform creates:
- Lambda function
- IAM role for the function
- SNS topic + subscription (currently just to me)
- Cloudwatch event rule for triggering Lambda

