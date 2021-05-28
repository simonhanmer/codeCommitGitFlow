import pytest
import boto3
import json
import re
from gitflow import (
    lambda_handler
)


# Test receiving an event from ec2
def test_lambda_handler_bad_event():
    with open('events/ec2Event.json') as jsonFile:
        event = json.load(jsonFile)

    with pytest.raises(Exception) as e:
        lambda_response = lambda_handler(event, {})

    assert str(e.value) == 'event is not from codeCommit'


# Test receiving an unexpected codecommit event
def test_lambda_handler_unexpected_codecommit():
    with open('events/unexpectedCodeCommit.json') as jsonFile:
        event = json.load(jsonFile)

    lambda_response = lambda_handler(event, {})
    assert re.match(r'^Unexpected event.*', lambda_response['message'])


# Test receiving an event from creating a branch
def test_lambda_handler_create_branch():
    with open('events/createBranch.json') as jsonFile:
        event = json.load(jsonFile)

    lambda_response = lambda_handler(event, {})
    assert lambda_response == {
        'message': 'Branch feature/test created on arn:aws:codecommit:eu-west-2:639512877143:testLambdaStack'
    }


# Test receiving an event from deleting a branch
def test_lambda_handler_delete_branch():
    with open('events/deleteBranch.json') as jsonFile:
        event = json.load(jsonFile)

    lambda_response = lambda_handler(event, {})
    assert lambda_response == {
        'message': 'Branch feature/test deleted from arn:aws:codecommit:eu-west-2:639512877143:testLambdaStack'
    }
