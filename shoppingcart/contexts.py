from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from shoppingapp.models import Macrame


def cart_contents(request):

    cart_items = []
    total = 0
    macrame_count = 0
    shoppingcart = request.session.get('shoppingcart', {})

    for item_id, quantity in shoppingcart.items():
        macrame = get_object_or_404(Macrame, pk=item_id)
        total += quantity * macrame.price
        macrame_count += quantity
        cart_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'macrame': macrame,
        })

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0
    
    grand_total = delivery + total
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'macrame_count': macrame_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context