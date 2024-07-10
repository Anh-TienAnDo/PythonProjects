from django import template
from django.http import HttpResponse
from product.services.loudspeaker import *
from product.services.usb import *
from product.services.memory_stick import *

register = template.Library()

@register.inclusion_tag('templatetags/banner_box.html')
def banner_box(request):
    loudspeaker_service = LoudspeakerService()
    usb_service = USBService()
    memory_stick_service = MemoryStickService()
    
    loudspeakers = loudspeaker_service.get_all_loudspeaker(start=0, limit=6)
    usbs = usb_service.get_all_usb(start=0, limit=6)
    memory_sticks = memory_stick_service.get_all_memory_stick(start=0, limit=6)
    
    return {
        'loudspeakers': loudspeakers,
        'usbs': usbs,
        'memory_sticks': memory_sticks
    }

