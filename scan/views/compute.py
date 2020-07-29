import json

import requests


def compute_pool_cloud():
    gedge_url = "http://gedge.gravity.top:8083/api/v1/kubernetes/nodes/clusters/raptorgedge"
    login_url = "http://gedge.gravity.top:8083/login/db?username=dashboard&password=view.Dashboard1"
    data = {}
    try:
        r_t = requests.get(login_url, timeout=3000)
        r_data = json.loads(r_t.text)
        if r_t:
            token = r_data['data']['token']
            bearer_token = "Bearer " + token
            headers = {"Access-Control-Allow-Origin": "*", "Content-Type": "application/json;charset=UTF-8",
                       "Authorization": bearer_token}
            r = requests.get(gedge_url, timeout=3000, headers=headers)

            if r:
                data = json.loads(r.text)
    except Exception as e:
        data = {}

    if data:
        node_percent = '0%'
        cpu_percent = '0%'
        memory_percent = '0%'
        node_total = data['data']['nodeSummary']['Total']
        node_schedulable = data['data']['nodeSummary']['Schedulable']
        cpu_total = data['data']['cpuSummary']['Total']
        cpu_used = data['data']['cpuSummary']['Used']
        memory_total = data['data']['memorySummary']['Total']
        memory_used = data['data']['memorySummary']['Used']
        if node_total == 0:
            node_percent = '0%'
        elif cpu_total == 0:
            cpu_percent = '0%'
        elif memory_total == 0:
            memory_percent = '0%'
        else:
            node_percent = '{:.0%}'.format(node_schedulable / node_total)
            cpu_percent = '{:.0%}'.format(cpu_used / cpu_total)
            memory_percent = '{:.0%}'.format(memory_used / memory_total)
        data['data']['nodeSummary']['Percent'] = int(node_percent.replace('%', ''))
        data['data']['cpuSummary']['Percent'] = int(cpu_percent.replace('%', ''))
        data['data']['memorySummary']['Percent'] = int(memory_percent.replace('%', ''))
    else:
        data = {}

        """return JsonResponse(data, safe=False)"""
    return data
