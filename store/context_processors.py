def cart_count(request):
    cart = request.session.get("cart",{})

    quantity = 0
    for key, value in cart.items():
        quantity += value
    return {"cart_count":quantity}