from django import template
from babel.numbers import format_currency
register = template.Library()

@register.filter(name='currency')
def currency(value):
    try:
        # Thiết lập ngôn ngữ là tiếng Việt và định dạng tiền tệ là VND
        formatted_currency = format_currency(value, 'VND', locale='vi_VN')
        return formatted_currency
    except Exception as e:
        # Xử lý nếu có lỗi
        print(f"Error formatting currency: {e}")
        return str(value)
