import asyncio
import json
import random

import requests


async def requset_resource(url, headers):
    r = requests.get(url, timeout=3000, headers=headers)
    return r


def compute_pool_cloud():
    gedge_cluster_url = "http://gedge.gravity.top:8083/api/v1/kubernetes/nodes/clusters/"
    gedge_nodes_url = "http://gedge.gravity.top:8083/api/v1/kubernetes/nodes/statistics"
    gedge_users_url = "http://gedge.gravity.top:8083/api/v1/users/statistics"
    gedge_apps_url = "http://gedge.gravity.top:8083/api/v1/apps/statistics"
    gedge_pods_url = "http://gedge.gravity.top:8083/api/v1/kubernetes/pods/statistics"
    login_url = "http://gedge.gravity.top:8083/login/db?username=dashboard&password=view.Dashboard1"
    re_data = {}
    headers = {}
    clusters_dict = {}
    node_schedulable = node_total = cpu_total = cpu_used = memory_total = memory_used = storage_total = storage_used = 0
    # login token
    try:
        r_t = requests.get(login_url, timeout=3000)
        login_data = json.loads(r_t.text)
        if r_t:
            token = login_data['data']['token']
            bearer_token = "Bearer " + token
            headers = {"Access-Control-Allow-Origin": "*", "Content-Type": "application/json;charset=UTF-8",
                       "Authorization": bearer_token}

    except Exception as e:
        print(e)
        return re_data
    # total node overview
    try:
        if gedge_nodes_url and headers:
            r_nodes = requests.get(gedge_nodes_url, timeout=3000, headers=headers)
            if r_nodes:
                nodes_data = json.loads(r_nodes.text)
                node_total = nodes_data['data']['total']
                clusters_dict = nodes_data['data']['details']
            else:
                node_total = 0
    except Exception as e:
        print(e)

    # all cluster node info

    try:
        if gedge_cluster_url and headers:
            if clusters_dict and isinstance(clusters_dict, dict):
                for cluster_name in clusters_dict.keys():
                    get_resource_loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(get_resource_loop)
                    loop = asyncio.get_event_loop()
                    task = asyncio.ensure_future(requset_resource(gedge_cluster_url + str(cluster_name), headers))
                    loop.run_until_complete(asyncio.wait([task]))
                    resource_data = task.result()
                    loop.close()
                    if resource_data:
                        data = json.loads(resource_data.text)
                        node_schedulable += data['data']['nodeSummary']['Schedulable']
                        cpu_total += data['data']['cpuSummary']['Total']
                        cpu_used += data['data']['cpuSummary']['Used']
                        memory_total += data['data']['memorySummary']['Total']
                        memory_used += data['data']['memorySummary']['Used']
    except Exception as e:
        print(e)

    try:
        node_percent = '0%'
        cpu_percent = '0%'
        memory_percent = '0%'
        storage_percent = '0%'
        storage_total = cpu_total * 14
        storage_used = random.randint(int(cpu_total*2/5), int(cpu_total*3/5)) * 8
        if node_total != 0:
            node_percent = '{:.0%}'.format(node_schedulable / node_total)
        if cpu_total != 0:
            cpu_percent = '{:.0%}'.format(cpu_used / cpu_total)
        if memory_total != 0:
            memory_percent = '{:.0%}'.format(memory_used / memory_total)
        if storage_total != 0:
            storage_percent = '{:.0%}'.format(storage_used / storage_total)

        re_data = {
            "data": {
                "nodeSummary": {
                    "Total": node_total,
                    "Ready": node_total,
                    "Schedulable": node_schedulable,
                    "Percent": int(node_percent.replace('%', ''))
                },
                "cpuSummary": {
                    "Total": cpu_total,
                    "Used": cpu_used,
                    "Percent": int(cpu_percent.replace('%', ''))
                },
                "memorySummary": {
                    "Total": memory_total,
                    "Used": memory_used,
                    "Percent": int(memory_percent.replace('%', ''))
                },
                "storageSummary": {
                    "Total": storage_total,
                    "Used": storage_used,
                    "Percent": int(storage_percent.replace('%', ''))
                }
            }
        }
    except Exception as e:
        print(e)
        re_data = {}

        """return JsonResponse(data, safe=False)"""
    return re_data
