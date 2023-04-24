# wiz-demo-checker

## What it does

This is a function that runs to help keep an eye on the demo environment. We can load multiple different test cases in and report back when things aren't looking "normal" in the env. 

## What it creates
The terraform creates:
- Lambda function
- IAM role for the function
- SNS topic + subscription (currently just to me)
- Cloudwatch event rule for triggering Lambda

## Why not put this on the demo team?
- There are things we care about that they don't (like custom saved queries)
- The back end team is working to keep things up to date. SEs though need to know proactively before our demos.


## What's next? 
- More tests
- Cleaning up the code to make it friendlier for others to use
- Better integrations (Slack?)