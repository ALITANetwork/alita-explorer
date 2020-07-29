import json

from django.db.models import Count
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from java_wallet.models import Transaction, Block
from scan.helpers import get_pending_txs
from scan.models import PeerMonitor
from scan.views.blocks import fill_data_block
from scan.views.compute import compute_pool_cloud
from scan.views.transactions import fill_data_transaction


@cache_page(5)
def index(request):
    global last_block
    txs = Transaction.objects.using('java_wallet').order_by('-height')[:5]

    for t in txs:
        fill_data_transaction(t, list_page=True)

    blocks = Block.objects.using('java_wallet').order_by('-height')[:5]

    for b in blocks:
        fill_data_block(b)

    if blocks:
        last_block = blocks.first()

    countries = PeerMonitor.objects.filter(
        state=PeerMonitor.State.ONLINE
    ).values('country_code').annotate(cnt=Count('country_code')).order_by('-cnt', 'country_code')

    online_peers_num = len(PeerMonitor.objects.filter(
        state=PeerMonitor.State.ONLINE
    ))
    online_peers_data = {}
    for country in countries:
        key = str(country['country_code']).lower()
        online_peers_data[key] = country['cnt']

    compute_data = compute_pool_cloud()

    print(json.dumps(online_peers_data))

    node_total = 0
    node_schedulable = 0
    node_percent = 0
    node_health = "Health"
    cpu_total = 0
    cpu_used = 0
    cpu_percent = 0
    cpu_health = "Health"
    memory_total = 0
    memory_used = 0
    memory_percent = 0
    memory_health = "Health"
    storage_total = 0
    storage_used = 0
    storage_percent = 0
    storage_health = "Health"

    if compute_data:
        node_total = compute_data['data']['nodeSummary']['Total']
        node_schedulable = compute_data['data']['nodeSummary']['Schedulable']
        node_percent = compute_data['data']['nodeSummary']['Percent']
        cpu_total = compute_data['data']['cpuSummary']['Total']
        cpu_used = compute_data['data']['cpuSummary']['Used']
        cpu_percent = compute_data['data']['cpuSummary']['Percent']
        memory_total = compute_data['data']['memorySummary']['Total']
        memory_used = compute_data['data']['memorySummary']['Used']
        memory_percent = compute_data['data']['memorySummary']['Percent']
        node_health = format_health(node_percent)
        cpu_health = format_health(100 - cpu_percent)
        memory_health = format_health(100 - memory_percent)
        storage_health = format_health(storage_percent)
    else:
        node_health = "UnHealth"
        cpu_health = "UnHealth"
        memory_health = "UnHealth"
        storage_health = "UnHealth"




    """计算生成区块时间"""
    forge_block_time_format = 'NaN'
    time = endingTime = startingTime = 0
    forge_blocks = Block.objects.using('java_wallet').order_by('-height')[:20]
    if forge_blocks.exists() > 0:
        testblock = forge_blocks.first()

        startingTime = forge_blocks[19].timestamp
        endingTime = forge_blocks[0].timestamp
        time = endingTime - startingTime
    else:
        startingTime = endingTime = time = 0

    if time == 0:
        forge_block_time_format = 'NaN'
    else:
        forge_block_time_format = str(time / 100)

    p_data = {"af": 16, "al": 11, "dz": 158, "ao": 85, "ag": 1, "ar": 351, "am": 8, "au": 1219, "at": 366, "az": 52,
              "bs": 7, "bh": 21, "bd": 105, "bb": 3, "by": 52, "be": 461, "bz": 1, "bj": 6, "bt": 1, "bo": 19,
              "ba": 16, "bw": 12, "br": 2023, "bn": 11, "bg": 44, "bf": 8, "bi": 1, "kh": 11, "cm": 21, "ca": 1563,
              "cv": 1, "cf": 2, "td": 7, "cl": 199, "cn": 5745, "co": 283, "km": 0, "cd": 12, "cg": 11, "cr": 35,
              "ci": 22, "hr": 59, "cy": 22, "cz": 195, "dk": 304, "dj": 1, "dm": 0, "do": 50, "ec": 61, "eg": 216,
              "sv": 21, "gq": 14, "er": 2, "ee": 19, "et": 30, "fj": 3, "fi": 231, "fr": 2555, "ga": 12, "gm": 1,
              "ge": 11, "de": 3305, "gh": 18, "gr": 305, "gd": 0, "gt": 40, "gn": 4, "gw": 0, "gy": 2, "ht": 6,
              "hn": 15, "hk": 226, "hu": 132, "is": 12, "in": 1430, "id": 695, "ir": 337, "iq": 84, "ie": 204,
              "il": 201, "it": 2036, "jm": 13, "jp": 5390, "jo": 27, "kz": 129, "ke": 32, "ki": 0, "kr": 986,
              "undefined": 5, "kw": 117, "kg": 4, "la": 6, "lv": 23, "lb": 39, "ls": 1, "lr": 0, "ly": 77, "lt": 35,
              "lu": 52, "mk": 9, "mg": 8, "mw": 5, "my": 218, "mv": 1, "ml": 9, "mt": 7, "mr": 3, "mu": 9, "mx": 1004,
              "md": 5, "mn": 5, "me": 3, "ma": 91, "mz": 10, "mm": 35, "na": 11, "np": 15, "nl": 770, "nz": 138,
              "ni": 6, "ne": 5, "ng": 206, "no": 413, "om": 53, "pk": 174, "pa": 27, "pg": 8, "py": 17, "pe": 153,
              "ph": 189, "pl": 438, "pt": 223, "qa": 126, "ro": 158, "ru": 1476, "rw": 5, "ws": 0, "st": 0, "sa": 434,
              "sn": 12, "rs": 38, "sc": 0, "sl": 1, "sg": 217, "sk": 86, "si": 46, "sb": 0, "za": 354, "es": 1374,
              "lk": 48, "kn": 0, "lc": 1, "vc": 0, "sd": 65, "sr": 3, "sz": 3, "se": 444, "ch": 522, "sy": 59,
              "tw": 426, "tj": 5, "tz": 22, "th": 312, "tl": 0, "tg": 3, "to": 0, "tt": 21, "tn": 43, "tr": 729,
              "tm": 0, "ug": 17, "ua": 136, "ae": 239, "gb": 2258, "us": 4624, "uy": 40, "uz": 37, "vu": 0, "ve": 285,
              "vn": 101, "ye": 30, "zm": 15, "zw": 5}

    context = {
        'txs': txs,
        'blocks': blocks,
        'txs_pending': get_pending_txs(),
        'last_block': last_block,
        'online_peers_num': str(online_peers_num),
        'online_peers_data': json.dumps(online_peers_data),
        'node_total': str(node_total),
        'node_schedulable': str(node_schedulable),
        'node_percent': str(node_percent),
        'node_health': node_health,
        'cpu_total': str(cpu_total),
        'cpu_used': str(cpu_used),
        'cpu_percent': str(cpu_percent),
        'cpu_health': cpu_health,
        'memory_total': str(memory_total),
        'memory_used': str(memory_used),
        'memory_percent': str(memory_percent),
        'memory_health': memory_health,
        'storage_total': str(storage_total),
        'storage_used': str(storage_used),
        'storage_percent': str(storage_percent),
        'storage_health': storage_health,
        'forge_block_time_format': forge_block_time_format,
    }

    return render(request, 'home/index.html', context)


def format_health(percent):
    if int(percent) > 70:
        return "Health"
    else:
        return "UnHealth"
