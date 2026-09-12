from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import ProductForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Order,OrderItem

# Create your views here.

@login_required(login_url="/login/")
def product_list(request):
    products = Product.objects.all()
    return render(request,"products.html",{"products": products})
@login_required(login_url="/login/")
def product_details(request,id):
    product = get_object_or_404(Product,id = id)
    return render(request,"product_detail.html",{"product":product})

@login_required(login_url="/login/")
def add_product(request):
    if request.method =="POST":
        product = ProductForm(request.POST, request.FILES)
        if product.is_valid():
            product.save()
            messages.success(request,"Product added successfully")
            return redirect("product_list")
    else:
        product = ProductForm()
    return render(request,"add_product.html",{"form": product})
@login_required(login_url="/login/")
def edit_product(request,id):
    product = get_object_or_404(Product, id = id)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request,"Product updated successfully")
            return redirect("product_details", id=product.id)

    else:
        form = ProductForm(instance=product)
    return render(request,"edit_product.html",{"form":form, "product":product})
@login_required(login_url="/login/")
def delete_product(request,id):
    product = get_object_or_404(Product, id = id)
    if request.method == "POST":
        product.delete()
        messages.success(request,"Product deleted successfully")
        return redirect("product_list")
    return render(request,"delete_product.html",{"product":product})

def session_test(request):
    request.session["name"] = "Dharshini S"
    name = request.session.get("name")
    return render(request, "session_test.html",{"name":name})

def session_view(request):
    name = request.session.get("name", "Guest")

    return render(
        request,
        "session_view.html",
        {"name": name}
    )

def delete_session(request):
    request.session.pop("name", None)

    return render(
        request,
        "session_view.html",
        {"name": request.session.get("name", "Guest")}
    )

@login_required(login_url="/login/")
def cart(request):
    cart = request.session.get("cart", {})

    products = Product.objects.filter(id__in=cart.keys())

    cart_items = []
    total = 0

    for product in products:
        quantity = cart[str(product.id)]
        subtotal = product.price * quantity

        cart_items.append({
            "product": product,
            "quantity": quantity,
            "subtotal": subtotal
        })

        total += subtotal

    return render(
        request,
        "cart.html",
        {
            "cart_items": cart_items,
            "total": total
        }
    )
@login_required(login_url="/login/")
def add_to_cart(request,id):
    cart = request.session.get("cart",{})
    product_id = str(id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    request.session["cart"] = cart

    return redirect("cart")
@login_required(login_url="/login/")
def remove_from_cart(request,id):
    cart = request.session.get("cart",{})
    product_id = str(id)

    if product_id in cart:
        del cart[product_id]
    request.session["cart"] = cart
    return redirect("cart")
@login_required(login_url="/login/")
def increase_quantity(request,id):
    cart = request.session.get("cart",{})
    product_id = str(id)

    if product_id in cart:
        cart[product_id] += 1

    request.session["cart"] = cart
    return redirect("cart")

@login_required(login_url="/login/")
def decrease_quantity(request, id):
    cart = request.session.get("cart", {})
    product_id = str(id)

    if product_id in cart:
        cart[product_id] -= 1
        if cart[product_id] == 0:
            del cart[product_id]
    request.session["cart"] = cart
    return redirect("cart")


@login_required(login_url="/login/")
def checkout(request):
    cart = request.session.get("cart", {})

    if not cart:
        return redirect("product_list")  # or a "cart is empty" page

    products = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity
        total += subtotal
        products.append({
            "product": product,
            "quantity": quantity,
            "subtotal": subtotal,
        })

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")

        order = Order.objects.create(
            user=request.user,
            name=name,
            email=email,
            phone=phone,
            address=address,
            total=total,
        )

        for item in products:
            OrderItem.objects.create(
                order=order,
                product=item["product"],
                quantity=item["quantity"],
                price=item["product"].price,   # snapshot price at purchase time
            )

        request.session["cart"] = {}
        request.session.modified = True

        return redirect("order_confirmation", order_id=order.id)

    return render(request, "checkout.html", {
        "products": products,
        "total": total,
    })

@login_required(login_url="/login/")
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "order_confirmation.html", {"order": order})

@login_required(login_url="/login/")
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "my_order.html", {"orders": orders})

def user_login(request):
    if request.method == "POST":
        name = request.POST.get("name")
        password = request.POST.get("password")
        user = authenticate(request, username=name, password=password)
        if user is not None:
            login(request, user)
            return redirect("product_list")
        return render(request, "login.html", {
            "error": "Invalid username or password"
        })
    return render(request, "login.html")

def user_logout(request):
    logout(request)
    return redirect("login")


