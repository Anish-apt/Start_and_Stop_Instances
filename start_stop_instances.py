import json
import boto3
from datetime import datetime

client = boto3.client('ec2')
client_s3 = boto3.client('s3')

bucket = "mycloudbuilders-instacnes-log"
ec2Group_Bucket = "mycloudbuilders-url"
key_id_group = 'EC2_group.txt'

def start_instances(instance_id, username, Ip):
    name = []
    response = client.start_instances(
    InstanceIds=instance_id,
    )
    all_instances = client.describe_instances(InstanceIds=instance_id)
    for reservation in all_instances['Reservations']:
        for instance in reservation['Instances']:
            if 'Tags' in instance:
                for tag in instance['Tags']:
                    if tag['Key'] == 'Name':
                        name.append(tag['Value'])
                        
    date = datetime.now()
    log = \
        f"""
    [
        ["date-time", "{date.strftime("%d-%m-%yT%H:%M:%S")}"],
        ["username", "{username}"],
        ["instanceids", "{instance_id}"],
        ["instancenames", "{name}"],
        ["ip", "{Ip}"],
        ["operation", "Started"]
    ]
        """
    log = dict(json.loads(log))
    log = json.dumps(log)
    key = "year=" + str(date.year) + "/" + "month=" + date.strftime("%m") + "/" + "date=" + date.strftime("%d") + "/" + date.strftime("%H:%M:%S") + "_auditLog.json"
    
    res = client_s3.put_object(Bucket=bucket, Body=log, Key=key)
    return response
    
def stop_instances(instance_id, username, Ip):
    name = []
    response = client.stop_instances(
    InstanceIds=instance_id,
    )
    all_instances = client.describe_instances(InstanceIds=instance_id)
    for reservation in all_instances['Reservations']:
        for instance in reservation['Instances']:
            if 'Tags' in instance:
                for tag in instance['Tags']:
                    if tag['Key'] == 'Name':
                        name.append(tag['Value'])
                        
    date = datetime.now()
    log = \
        f"""
    [
        ["date-time", "{date.strftime("%d-%m-%yT%H:%M:%S")}"],
        ["username", "{username}"],
        ["instanceids", "{instance_id}"],
        ["instancenames", "{name}"],
        ["ip", "{Ip}"],
        ["operation", "Stopped"]
    ]
        """
    log = dict(json.loads(log))
    log = json.dumps(log)
    key = "year=" + str(date.year) + "/" + "month=" + date.strftime("%m") + "/" + "date=" + date.strftime("%d") + "/" + date.strftime("%H:%M:%S") + "_auditLog.json"
    
    res = client_s3.put_object(Bucket=bucket, Body=log, Key=key)
    return response
    
def start_instances_group(instance_group, username, Ip):
    name = []
    respone = client_s3.get_object(
        Bucket = ec2Group_Bucket,
        Key = key_id_group)
    data = respone['Body'].read().decode('utf-8')
    json_data = json.loads(data)
    instance_id = json_data[instance_group]
    response = client.start_instances(
    InstanceIds=instance_id,
    )
    all_instances = client.describe_instances(InstanceIds=instance_id)
    for reservation in all_instances['Reservations']:
        for instance in reservation['Instances']:
            if 'Tags' in instance:
                for tag in instance['Tags']:
                    if tag['Key'] == 'Name':
                        name.append(tag['Value'])
                        
    date = datetime.now()
    log = \
        f"""
    [
        ["date-time", "{date.strftime("%d-%m-%yT%H:%M:%S")}"],
        ["username", "{username}"],
        ["instanceids", "{instance_id}"],
        ["instancenames", "{name}"],
        ["ip", "{Ip}"],
        ["operation", "Started"]
    ]
        """
    log = dict(json.loads(log))
    log = json.dumps(log)
    key = "year=" + str(date.year) + "/" + "month=" + date.strftime("%m") + "/" + "date=" + date.strftime("%d") + "/" + date.strftime("%H:%M:%S") + "_auditLog.json"
    
    res = client_s3.put_object(Bucket=bucket, Body=log, Key=key)
    return response
    
def stop_instances_group(instance_group, username, Ip):
    name = []
    respone = client_s3.get_object(
        Bucket = ec2Group_Bucket,
        Key = key_id_group)
    data = respone['Body'].read().decode('utf-8')
    json_data = json.loads(data)
    instance_id = json_data[instance_group]
    response = client.stop_instances(
    InstanceIds=instance_id,
    )
    all_instances = client.describe_instances(InstanceIds=instance_id)
    for reservation in all_instances['Reservations']:
        for instance in reservation['Instances']:
            if 'Tags' in instance:
                for tag in instance['Tags']:
                    if tag['Key'] == 'Name':
                        name.append(tag['Value'])
                        
    date = datetime.now()
    log = \
        f"""
    [
        ["date-time", "{date.strftime("%d-%m-%yT%H:%M:%S")}"],
        ["username", "{username}"],
        ["instanceids", "{instance_id}"],
        ["instancenames", "{name}"],
        ["ip", "{Ip}"],
        ["operation", "Stopped"]
    ]
        """
    log = dict(json.loads(log))
    log = json.dumps(log)
    key = "year=" + str(date.year) + "/" + "month=" + date.strftime("%m") + "/" + "date=" + date.strftime("%d") + "/" + date.strftime("%H:%M:%S") + "_auditLog.json"
    
    res = client_s3.put_object(Bucket=bucket, Body=log, Key=key)
    return response

def lambda_handler(event, context):
    # TODO implement
    
    body = event["body"]
    header = event["headers"]
    
    op = json.loads(body)['op']
    try:
        instance_id = json.loads(body)['instance_id']
        instance_group = "null"
        
    except KeyError:
        instance_group = json.loads(body)['instance_group']
        
    username = json.loads(body)['username']
    Ip = header['X-Forwarded-For']
    
    if instance_group != "null":
        if op == "start":
            response = start_instances_group(instance_group, username, Ip)
        
        elif op == "stop":
            response = stop_instances_group(instance_group, username, Ip)
    else:
        if op == "start":
            response = start_instances(instance_id, username, Ip)
        
        elif op == "stop":
            response = stop_instances(instance_id, username, Ip)
        
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(response)
    }