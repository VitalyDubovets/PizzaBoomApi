import json
from typing import Optional

import boto3
from botocore.client import Config


sfn_client = boto3.client("stepfunctions", config=Config(read_timeout=65))


def start_execution(
    *, state_machine_arn: str, name: Optional[str] = None, input_: dict = None
):
    input_ = input_ or {}
    params = dict(stateMachineArn=state_machine_arn, input=json.dumps(input_))
    if name:
        params["name"] = name
    return sfn_client.start_execution(**params)


def stop_execution(execution_arn, error, cause, *args, **kwargs):
    return sfn_client.stop_execution(
        executionArn=execution_arn, error=error, cause=cause, *args, **kwargs
    )


def describe_execution(execution_arn, *args, **kwargs):
    return sfn_client.describe_execution(
        executionArn=execution_arn, *args, **kwargs
    )


def send_task_success(task_token: str, output: dict = None):
    output = output or {}
    return sfn_client.send_task_success(
        taskToken=task_token, output=json.dumps(output)
    )


def send_task_failure(task_token, error="", cause=""):
    return sfn_client.send_task_failure(
        taskToken=task_token, error=error, cause=cause
    )
