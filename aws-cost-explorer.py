#!/usr/bin/env python3

import argparse
import boto3
import datetime
import calendar
import json

dt = datetime.datetime.today()
parser = argparse.ArgumentParser()
parser.add_argument('--month', type=int, default=dt.month, help='The numerical value of the month whose cost summary we would like to have (1-12)')
parser.add_argument('--export_file', type=str, default="cost.json", help='Where do you want to export the data file in JSON format. Location has to be writable by Python')
args = parser.parse_args()

if (args.month == "") :
	month = dt.month
else :
	month = args.month

start = str(dt.year)+"-"+str(month)+"-01"
end = str(dt.year)+"-"+str(month)+"-"+str(calendar.monthrange(dt.year,dt.month)[1])

cd = boto3.client('ce', 'us-east-1')

results = []

cost_summary = dict()

token = None
while True:
    if token:
        kwargs = {'NextPageToken': token}
    else:
        kwargs = {}
    data = cd.get_cost_and_usage(TimePeriod={'Start': start, 'End':  end}, Granularity='MONTHLY', Metrics=['UnblendedCost'], GroupBy=[{'Type': 'DIMENSION', 'Key': 'LINKED_ACCOUNT'}, {'Type': 'DIMENSION', 'Key': 'SERVICE'}], **kwargs)
    results += data['ResultsByTime']
    token = data.get('NextPageToken')
    if not token:
        break

for result_by_time in results:
    for group in result_by_time['Groups']:
        if group['Keys'][0] not in cost_summary:
            cost_summary[group['Keys'][0]] = dict()
            #print(group['Keys'][0])

        cost_summary[group['Keys'][0]][group['Keys'][1]] = group['Metrics']['UnblendedCost']['Amount']

        with open(args.export_file, 'w') as fp:
            json.dump(cost_summary, fp)
