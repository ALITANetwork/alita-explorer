import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import requests


def compute_pool_cloud():
    #gedge_url = "http://app2.gravity.top:8083/api/v1/kubernetes/nodes/clusters/PoolCloud"
    #bearer_token = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJhZG1pbiIsImV4cCI6MTU5NTU2MDQ3NSwiaWF0IjoxNTk1NDc0MDc1LCJpc3MiOiJ3YXluZSJ9.XydtpeK8nC4eiPkYKcoHK9xmWoLrdQ2Dgmeo0odXGksnEnQg8XCSj3uZ7zSznrptUm0tyGiPh_Oci0JBPMIXJg"
    gedge_url = "http://111.6.79.62:8083/api/v1/kubernetes/nodes/clusters/raptorgedge"
    bearer_token = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJhZG1pbiIsImV4cCI6MTU5NTY0NDMyMCwiaWF0IjoxNTk1NTU3OTIwLCJpc3MiOiJ3YXluZSJ9.SjW67DWqgT56Pf-lYBR-_pnJUeCCajU0WSuqtrMWcPoCtTQFCs7frbGOwI5ylX-3RzxREVvmdZ2DVR1JI0LU7w"
    headers = {"Access-Control-Allow-Origin": "*", "Content-Type": "application/json;charset=UTF-8",
               "Authorization": bearer_token}
    try:
        r = requests.get(gedge_url, timeout=3000, headers=headers)
        data = {}
        if r:
            data = json.loads(r.text)
    except Exception as e:
        data = {}

    if data:
        print(data)
        print(data['data']['nodeSummary']['Total'])
        print(data['data']['nodeSummary']['Schedulable'])
        print(data['data']['cpuSummary']['Total'])
        print(data['data']['cpuSummary']['Used'])
        print(data['data']['memorySummary']['Total'])
        print(data['data']['memorySummary']['Used'])

        node_total = data['data']['nodeSummary']['Total']
        node_schedulable = data['data']['nodeSummary']['Schedulable']
        cpu_total = data['data']['cpuSummary']['Total']
        cpu_used = data['data']['cpuSummary']['Used']
        memory_total = data['data']['memorySummary']['Total']
        memory_used = data['data']['memorySummary']['Used']

        print('percent: {:.0%}'.format(node_schedulable / node_total))
        print('percent: {:.0%}'.format(cpu_used / cpu_total))
        print('percent: {:.0%}'.format(memory_used / memory_total))
        node_percent = '{:.0%}'.format(node_schedulable / node_total)
        print(type(node_percent))
        cpu_percent = '{:.0%}'.format(cpu_used / cpu_total)
        memory_percent = '{:.0%}'.format(memory_used / memory_total)
        print(node_percent.replace('%', ''))
        print(cpu_percent.replace('%', ''))
        print(memory_percent.replace('%', ''))
        data['data']['nodeSummary']['Percent'] = int(node_percent.replace('%', ''))
        data['data']['cpuSummary']['Percent'] = int(cpu_percent.replace('%', ''))
        data['data']['memorySummary']['Percent'] = int(memory_percent.replace('%', ''))
        print("Test K3S Info")
        print(data)
    else:
        data = {}

        """return JsonResponse(data, safe=False)"""
    return data
