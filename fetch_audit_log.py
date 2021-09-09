import json
import csv
import boto3
import codecs
import time

client = boto3.client('athena')
client_s3 = boto3.client('s3')


def lambda_handler(event, context):
    # TODO implement
    
    logs = []
    
    para = event["queryStringParameters"]
    para = json.dumps(para)
    start = json.loads(para)['start']
    end = json.loads(para)['end']
    
    start_year = start[0:4]
    start_month = start[5:7]
    start_date = start[8:]
    
    end_year = end[0:4]
    end_month = end[5:7]
    end_date = end[8:]
    
    query = "SELECT * FROM logs where date >= '{0}' and date <= '{1}' and month >= '{2}' and month <= '{3}' and year >= '{4}' and year <= '{5}';".format(start_date, end_date, start_month, end_month, start_year, end_year)
    res = client.start_query_execution(
    QueryString=query,
    QueryExecutionContext={
        'Database': 'part_log',
    },
    ResultConfiguration={
        'OutputLocation': 's3://mycloudbuilders-url/Athena/',}
    )
    QueryId = res['QueryExecutionId']
    
    time.sleep(2)
    

    response = client_s3.get_object(Bucket="mycloudbuilders-url", Key="Athena/" + QueryId + ".csv")
    
    for row in csv.DictReader(codecs.getreader('utf-8')(response[u'Body'])):
        logs.append(row)
        
    output_dict = json.loads(json.dumps(logs))
    
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(output_dict)
    }
