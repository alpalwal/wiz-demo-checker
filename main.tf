provider "aws" {
  region =var.aws_region
}

provider "archive" {}

data "archive_file" "zip" {
  type        = "zip"
  source_dir = "code/"
  output_path = "demo_checker.zip"
}

data "aws_iam_policy_document" "policy" {
  statement {
    sid    = ""
    effect = "Allow"
    principals {
      identifiers = ["lambda.amazonaws.com"]
      type        = "Service"
    }
    actions = ["sts:AssumeRole"]
  }
}

data "aws_iam_policy_document" "sns_publish_policy_and_cloudwatch" {
    statement {
      actions   = ["sns:Publish",
                  "logs:CreateLogGroup",
                  "logs:CreateLogStream",
                  "logs:PutLogEvents"]
      resources = ["*"]
      effect = "Allow"
    }
  }

resource "aws_iam_policy" "policy" {
    name        = "lambda_sns_publish"
    description = "publish sns messages"
    policy      = data.aws_iam_policy_document.sns_publish_policy_and_cloudwatch.json
  }

resource "aws_iam_role" "demo_checker_execution_role" {
  name               = "demo_checker_execution_role"
  assume_role_policy = data.aws_iam_policy_document.policy.json
}

resource "aws_iam_role_policy_attachment" "policy_attach" {
  role       = resource.aws_iam_role.demo_checker_execution_role.name
  policy_arn = resource.aws_iam_policy.policy.arn
}

resource "aws_lambda_function" "lambda" {
  function_name = "demo_checker"
  filename         = data.archive_file.zip.output_path
  source_code_hash = data.archive_file.zip.output_base64sha256
  role    = aws_iam_role.demo_checker_execution_role.arn
  handler = "demo_checker.lambda_handler"
  runtime = "python3.7"
  layers = [var.layer_arn]
  timeout = 120
  environment {
    variables = {
      sns_arn = resource.aws_sns_topic.demo_issue_topic.arn
      client_id = var.client_id
      client_secret = var.client_secret
    }
  }
}

resource "aws_sns_topic" "demo_issue_topic" {
    name = "demo_issue_topic"
  }

resource "aws_sns_topic_subscription" "demo_issue_topic_subscription" {
  topic_arn = resource.aws_sns_topic.demo_issue_topic.arn
  protocol  = "email"
  endpoint  = "alex@wiz.io"
}

resource "aws_cloudwatch_event_rule" "demo_checker_lambda_event_rule" {
    name = "profile-generator-lambda-event-rule"
    description = "retry scheduled every 20 min"
    schedule_expression = "rate(30 minutes)"
  }
  
resource "aws_cloudwatch_event_target" "demo_checker_lambda_target" {
    arn = resource.aws_lambda_function.lambda.arn
    rule = aws_cloudwatch_event_rule.demo_checker_lambda_event_rule.name
}
  
resource "aws_lambda_permission" "allow_cloudwatch_to_call_rw_fallout_retry_step_deletion_lambda" {
    statement_id = "AllowExecutionFromCloudWatch"
    action = "lambda:InvokeFunction"
    function_name = resource.aws_lambda_function.lambda.function_name
    principal = "events.amazonaws.com"
    source_arn = aws_cloudwatch_event_rule.demo_checker_lambda_event_rule.arn
  }