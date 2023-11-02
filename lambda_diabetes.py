#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import io
import boto3
import json
import csv

runtime = boto3.client('runtime.sagemaker')
ses = boto3.client('ses')

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    
    data = json.loads(json.dumps(event))
    payload = data['data']
    email = data['email']
    
    response = runtime.invoke_endpoint(EndpointName='diabetes-12',
                                       ContentType='text/csv',
                                       Body=payload)
                                       
    result = json.loads(response['Body'].read().decode())

    pred = float(result)
    predicted_label = f"Prediction of {data} is : "

    if pred >= 0.5:
        predicted_label = 'high risk of diabetes'
        email_response = ses.send_templated_email(
            Source='Liyeng <leeliyeng.lily@gmail.com>',
            Destination={
                'ToAddresses': [
                    email,
                ]
            },
            ConfigurationSetName='diabetes',
            Template='MyTemplate',
            TemplateData='{ "name":"' + data['firstName'] + '", "lastName": "' + data['lastName'] + '", "email": "' + data['email'] + '" }'    
        )
    else:
        predicted_label = 'low risk of diabetes'

    print("Predicted Label : ", predicted_label)

    return predicted_label

