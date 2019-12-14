'''
 * Copyright (c) 2019 Cahit Oez -- https://www.cahitoz.com
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; version 2 of the License.
 *
 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
 * or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
 * for more details.
'''
import argparse
import boto3
import datetime
import calendar
import json

dt = datetime.datetime.today()
parser = argparse.ArgumentParser()
parser.add_argument('--month', type=int, default=dt.month, help='The numerical value of the month whose cost summary we would like to have (1-12)')
parser.add_argument('--year', type=int, default=dt.year, help='The numerical value of the year whose cost summary we would like to have (2019, 2020)')
parser.add_argument('--export_file', type=str, help='Where do you want to export the data file in JSON format. Location has to be writable by Python')
args = parser.parse_args()

if (args.month == "") :
	month = dt.month
else :
	month = args.month

if (month < 10) :
    month = "0"+str(month)  

if (args.year == "") :
	year = dt.year
else :
	year = args.year
year = args.year

start = str(year)+"-"+str(month)+"-01"
end = str(year)+"-"+str(month)+"-"+str(calendar.monthrange(int(year),int(month))[1])
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

        cost_summary[group['Keys'][0]][group['Keys'][1]] = group['Metrics']['UnblendedCost']['Amount']

    if args.export_file is not None:
        with open(args.export_file, 'w') as fp:
            json.dump(cost_summary, fp)
    else:
        print(cost_summary)
