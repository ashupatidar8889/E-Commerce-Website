from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Product, Order, OrderItem


# HOME PAGE
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


# PRODUCT LIST + SEARCH
def products(request):
    q = request.GET.get('q')
    if q:
        items = Product.objects.filter(name__icontains=q)
    else:
        items = Product.objects.all()

    return render(request, 'product_list.html', {'products': items})


# ADD TO CART
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    request.session['cart'] = cart
    return redirect('cart')


# CART PAGE
def cart(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity
        total += subtotal

        items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    return render(request, 'cart.html', {
        'items': items,
        'total': total
    })


# REMOVE ITEM
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        del cart[str(product_id)]

    request.session['cart'] = cart
    return redirect('cart')


# INCREASE QUANTITY
def increase_quantity(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)] += 1

    request.session['cart'] = cart
    return redirect('cart')


# DECREASE QUANTITY
def decrease_quantity(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        if cart[str(product_id)] > 1:
            cart[str(product_id)] -= 1
        else:
            del cart[str(product_id)]

    request.session['cart'] = cart
    return redirect('cart')


# CHECKOUT
def checkout(request):
    if not request.user.is_authenticated:
        return redirect('login')

    cart = request.session.get('cart', {})
    total = 0

    order = Order.objects.create(user=request.user, total=0)

    for product_id, qty in cart.items():
        product = Product.objects.get(id=product_id)
        total += product.price * qty

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=qty
        )

    order.total = total
    order.save()

    request.session['cart'] = {}

    return render(request, 'checkout.html', {'order': order})


# LOGIN
def user_login(request):
    if request.method == "POST":
        u = request.POST['username']
        p = request.POST['password']

        user = authenticate(request, username=u, password=p)

        if user:
            login(request, user)
            return redirect('home')

    return render(request, 'login.html')


# REGISTER
def register(request):
    if request.method == "POST":
        User.objects.create_user(
            username=request.POST['username'],
            password=request.POST['password']
        )
        return redirect('login')

    return render(request, 'register.html')


# LOGOUT
def user_logout(request):
    logout(request)
    return redirect('home')


# PROFILE
def profile(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'profile.html', {'orders': orders})