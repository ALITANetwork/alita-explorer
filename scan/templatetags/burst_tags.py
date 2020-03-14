from datetime import timedelta

from django import template

from burst.libs.reed_solomon import ReedSolomon
from burst.constants import MAX_BASE_TARGET
from burst.libs.transactions import get_message
from java_wallet.fields import get_desc_tx_type
from java_wallet.models import Block, Transaction
from scan.helpers import get_exchange_info
from decimal import Decimal
import math

register = template.Library()


def get_vary_rule(once: float, slow: int, month: int) -> float:
    ONE_RAPTOR = 100000000
    return float(Decimal(once) * Decimal(ONE_RAPTOR) * Decimal(math.pow(Decimal(slow), month)) / Decimal(
        math.pow(Decimal(100), month)) / Decimal(ONE_RAPTOR))


def middle_rule(once: float, slow: int, month: int) -> float:
    return (Decimal(once) * Decimal(math.pow(Decimal(slow), month))) / (Decimal(math.pow(Decimal(100), month)))


def get_block_reward(block: Block) -> int:
    if block.height == 0 or block.height > 2759400:
        return 0
    month = int((block.height - 1) / 13140)
    slow = 100
    if 0 < block.height <= 13140 * 2:
        month = 0
    elif 2 <= month <= 104:
        month -= 1
        slow = 98
    else:
        month = month - 104
        slow = 99
        return int(get_vary_rule(middle_rule(1293.8, 98, 103), slow, month))

    return int(get_vary_rule(1293.8, slow, month))


@register.filter
def block_reward(block: Block) -> int:
    return get_block_reward(block)


@register.filter
def block_reward_fee(block: Block) -> float:
    return get_block_reward(block) + block.total_fee / 10 ** 8


@register.filter
def burst_amount(value: int) -> float:
    return value / 10 ** 8


@register.filter
def in_usd(value: float) -> float:
    info = get_exchange_info()
    return value * info['price_usd']


@register.filter
def rounding(value: float, accuracy: int) -> float:
    return round(value, accuracy)


@register.filter
def bin2hex(value: bytes) -> str:
    if not value:
        return ''
    return value.hex().upper()


@register.filter
def tx_message(tx: Transaction) -> str:
    if not tx.has_message:
        return ''
    return get_message(tx.attachment_bytes)


@register.filter
def tx_type(tx: Transaction) -> str:
    return get_desc_tx_type(tx.type, tx.subtype)


@register.filter
def num2rs(value: str or int) -> str:
    return ReedSolomon().encode(str(value))


@register.simple_tag()
def block_generation_time(block: Block) -> timedelta:
    if block.previous_block:
        return block.timestamp - block.previous_block.timestamp
    else:
        # first block
        return timedelta(0)


@register.filter
def sub(a: int or float, b: int or float) -> int or float:
    return a - b


@register.filter
def div(a: int or float, b: int or float) -> float:
    return a / b


@register.filter
def mul(a: int or float, b: int or float) -> int or float:
    return a * b


@register.filter
def div_decimals(a: int or float, b: int) -> float:
    return a / 10 ** b


@register.filter
def mul_decimals(a: int or float, b: int) -> float:
    return a * 10 ** b


@register.filter
def percent(value: int or float, total: int or float) -> int or float:
    return value / total * 100


@register.filter
def net_diff(base_target: int) -> float:
    return MAX_BASE_TARGET / base_target


@register.simple_tag(takes_context=True)
def rank_row(context: dict, number: int) -> int:
    start = 0
    if context['page_obj'].number > 0:
        start = context['paginator'].per_page * (context['page_obj'].number - 1)

    return number + start
