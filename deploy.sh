#!/bin/bash

stage=$1
awsProfile=$2
export STAGE=$stage
sls deploy -s "$stage" --aws-profile "$awsProfile" --config serverless-auth.yml && \
sls deploy -s "$stage" --aws-profile "$awsProfile" --config serverless-api.yml && \
sls deploy -s "$stage" --aws-profile "$awsProfile" --config serverless-order-state-machine.yml