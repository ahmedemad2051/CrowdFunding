from django import template

register = template.Library()


@register.filter(name='total_amount')
@register.simple_tag
def total_amount(donations):
    all = 0
    for donate in donations:
        all += donate.amount
    return all


@register.filter(name='total_amount_percent')
@register.simple_tag
def total_amount_percent(donations, target):
    return int((donations * 100) / target)
