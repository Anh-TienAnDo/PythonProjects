from django import template
from django.http import HttpResponse
from product.services.loudspeaker import *
from product.services.usb import *
from product.services.memory_stick import *
from django.core.cache import cache

register = template.Library()

@register.inclusion_tag('templatetags/banner_box.html')
def banner_box(request):
    cache_key = 'product_cache'  # Tạo cache key
    cached_data = cache.get(cache_key)

    if cached_data:
        data = {
            'loudspeakers': cached_data.get('loudspeakers')[0:6],
            'usbs': cached_data.get('usbs')[0:6],
            'memory_sticks': cached_data.get('memory_sticks')[0:6]
        }
        print("----------------------------")
        print("banner_box, cached_data")
        return data
    
    loudspeaker_service = LoudspeakerService(request=request)
    usb_service = USBService(request=request)
    memory_stick_service = MemoryStickService(request=request)
    
    loudspeakers_data = loudspeaker_service.get_all_loudspeaker()
    usbs_data = usb_service.get_all_usb()
    memory_sticks_data = memory_stick_service.get_all_memory_stick()

    loudspeakers = loudspeakers_data.get('loudspeakers')
    usbs = usbs_data.get('usbs')
    memory_sticks = memory_sticks_data.get('memory_sticks')

    data = {
        'loudspeakers': loudspeakers,
        'usbs': usbs,
        'memory_sticks': memory_sticks
    }

    cache.set(cache_key, data, timeout=60*5)  # Cache trong 5 phút

    return {
        'loudspeakers': loudspeakers[0:6],
        'usbs': usbs[0:6],
        'memory_sticks': memory_sticks[0:6]
    }

