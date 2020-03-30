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
def total_amount(donations, target):
    return int((donations * 100) / target)
