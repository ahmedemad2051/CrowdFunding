from django import template

register = template.Library()


@register.filter(name='total_amount')
def total_amount(donations):
    all = 0
    for donate in donations:
        all += donate.amount
    return all


@register.filter(name='total_amount_percent')
def total_amount(donations, target):
    return (donations * 100) / target
