check_aws_status_feed
=====================

Checks http://status.aws.amazon.com/ RSS feeds for outage and performance information.
```
usage: check_aws_status.py [-h] [--region {us-east-1,us-west-1,us-west-2}]
                           {cloudwatch,ec2,elb,rds,route53,vpc,iam,all}

Check current status information from the AWS Service Health Dashboard
(status.aws.amazon.com).

positional arguments:
  {cloudwatch,ec2,elb,rds,route53,vpc,iam,all}

optional arguments:
  -h, --help            show this help message and exit
  --region {us-east-1,us-west-1,us-west-2}
```
