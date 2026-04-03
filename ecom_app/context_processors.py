from .models import Cart

def cart_count(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)

        total_quantity = 0
        for item in cart_items:
            total_quantity += item.quantity  

    else:
        total_quantity = 0

    return {
        'cart_count': total_quantity   
    }