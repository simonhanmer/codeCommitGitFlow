import os
import boto3
import logging
import json


LOG_LEVEL = os.environ.get("LOG_LEVEL", logging.INFO)
root_logger = logging.getLogger()
root_logger.setLevel(LOG_LEVEL)
log = logging.getLogger(__name__)


def lambda_handler(event, context):
    log.debug(f"Event: {json.dumps(event, indent = 4)}")

    # ignore event if its not a codecommit repo change

    if (event['source'] != 'aws.codecommit' or
       event['detail-type'] != 'CodeCommit Repository State Change'):
        return

    if event['detail']['referenceType'] == 'branch':
        manageBranch(event)


def manageBranch(event):
    repo = event['resources'][0]
    if event['detail']['event'] == 'referenceCreated':
        createPipeline(repo, event['detail']['referenceName'])
    elif event['detail']['event'] == 'referenceDeleted':
        deletePipeline(repo, event['detail']['referenceName'])
    else:
        return


def createPipeline(repo, branch):
    log.info(f"Branch {branch} created on {repo}")


def deletePipeline(repo, branch):
    log.info(f"Branch {branch} deleted on {repo}")