variable "aws_region" {
  default     = "us-west-1"
}

# Create a SA in Wiz with read.all creds and export them before running plan
#export TF_VAR_client_id=password_123
#export TF_VAR_client_secret=password_abc

variable "client_id" {
  type        = string
  sensitive   = true
}

variable "client_secret" {
  type        = string
  sensitive   = true
}

# https://aws.amazon.com/blogs/compute/upcoming-changes-to-the-python-sdk-in-aws-lambda/
variable "layer_arn" {
    default = "arn:aws:lambda:us-west-1:325793726646:layer:AWSLambda-Python-AWS-SDK:4"
}