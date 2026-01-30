from django.contrib import messages
from home.models import DeliveryPartner

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import DeliveryPartner

def creat_partner(request):

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        username = request.POST.get('username', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        if not all([name, username, phone, email, password]):
            return render(request, 'creat.html', {'error': 'All fields are required.'})

        if DeliveryPartner.objects.filter(username=username).exists():
            return render(request, 'creat.html', {'error': 'Username already taken.'})

        if DeliveryPartner.objects.filter(email=email).exists():
            return render(request, 'creat.html', {'error': 'Email already registered.'})

        if DeliveryPartner.objects.filter(phone=phone).exists():
            return render(request, 'creat.html', {'error': 'Phone already registered.'})

        partner = DeliveryPartner.objects.create(
            name=name,
            username=username,
            phone=phone,
            email=email,
            password=make_password(password),
        )

        messages.success(request, 'Account created successfully. You can now log in.')
        return render(request, 'creat.html', {
            'created': True,
            'email': email
        })

    return render(request, 'creat.html')
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from datetime import datetime
from home.models import Contact
from django.views.decorators.csrf import ensure_csrf_cookie
# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def services(request):
   return render(request, 'services.html')

from home.models import Restaurant

def resturent(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        address = request.POST.get('address', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        description = request.POST.get('description', '').strip()
        # Only save if required fields are present
        if name and address and phone:
            Restaurant.objects.create(
                name=name,
                address=address,
                phone=phone,
                email=email,
                description=description
            )
            return render(request, 'resturent.html', {'success': True})
        else:
            return render(request, 'resturent.html', {'error': 'Name, address, and phone are required.'})
    return render(request, 'resturent.html')

def delivery(request):
    return render(request, 'delivery.html')

def cart(request):
    # Require login to view cart
    if not request.session.get('user_id'):
        from django.contrib import messages as _messages
        _messages.info(request, 'Please log in to view your cart.')
        return redirect('login')

    cart = request.session.get('cart', [])
    # A simple menu mapping (id -> details). In a real app, use a database.
    menu = {
        1: {'name': 'Burger', 'price': 120},
        2: {'name': 'Chicken Burger', 'price': 120},
        3: {'name': 'Chicken Roll', 'price': 60},
        4: {'name': 'Butter Chicken', 'price': 80},
        5: {'name': 'Egg Fried Rice', 'price': 120},
        6: {'name': 'Chicken Biryani', 'price': 160},
        7: {'name': 'Butter Chicken (Large)', 'price': 280},
        8: {'name': 'Chicken Shawarma', 'price': 120},
        9: {'name': 'Chicken Nuggets', 'price': 90},
        10: {'name': 'Tandoori Chicken', 'price': 80},
        11: {'name': 'Prawn Fry', 'price': 100},
        12: {'name': 'Egg Curry', 'price': 60},
        13: {'name': 'Butter Chicken (Special)', 'price': 160},
        14: {'name': 'Veg Sandwich', 'price': 90},
        15: {'name': 'White Sauce Pasta', 'price': 60},
        16: {'name': 'French Fries', 'price': 70},
        17: {'name': 'Veg Hakka Noodles', 'price': 70},
        18: {'name': 'Paneer Tikka', 'price': 90},
        19: {'name': 'Veg Biryani', 'price': 180},
        20: {'name': 'Veg Manchurian', 'price': 150},
        21: {'name': 'Chole Bhature', 'price': 50},
        22: {'name': 'Masala Dosa', 'price': 55},
        23: {'name': 'Idli Sambar', 'price': 40},
    }
    cart_items = []
    total = 0
    for entry in cart:
        item = menu.get(entry['item_id'])
        if item:
            subtotal = item['price'] * entry['quantity']
            total += subtotal
            cart_items.append({
                'item_id': entry['item_id'],
                'name': item['name'],
                'price': item['price'],
                'quantity': entry['quantity'],
                'subtotal': subtotal,
            })
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})

def add_to_cart(request, item_id):
    if request.method == 'POST':
        # require login to add to cart
        if not request.session.get('user_id'):
            # if AJAX request, return JSON error; otherwise redirect to login
            if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.META.get('HTTP_ACCEPT', '').find('application/json') != -1:
                return JsonResponse({'success': False, 'error': 'login_required'}, status=401)
            from django.contrib import messages as _messages
            _messages.info(request, 'Please log in to add items to your cart.')
            return redirect('login')

        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', [])
        # Check if item already in cart
        for item in cart:
            if item['item_id'] == item_id:
                item['quantity'] += quantity
                break
        else:
            cart.append({'item_id': item_id, 'quantity': quantity})
        request.session['cart'] = cart
        # If AJAX, return JSON success; otherwise redirect to cart page
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.META.get('HTTP_ACCEPT', '').find('application/json') != -1:
            return JsonResponse({'success': True})
        return redirect('cart')
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('contact', '').strip()  # Match form field name
        message = request.POST.get('message', '').strip()
        if name and email and phone and message:
            contact = Contact(name=name, email=email, phone=phone, message=message, date=datetime.today())
            contact.save()
            return render(request, 'contact.html', {'success': True})
        else:
            return render(request, 'contact.html', {'error': 'All fields are required.'})
    return render(request, 'contact.html')

@ensure_csrf_cookie
def login(request):
    # handle login POST
    if request.method == 'POST':
        identifier = request.POST.get('username', '').strip()
        raw_password = request.POST.get('password', '').strip()
        user = None
        if identifier and raw_password:
            # try to find user by username, then email, then phone
            user = DeliveryPartner.objects.filter(username=identifier).first()
            if not user:
                user = DeliveryPartner.objects.filter(email=identifier).first()
            if not user:
                user = DeliveryPartner.objects.filter(phone=identifier).first()

        if user and check_password(raw_password, user.password):
            # set session
            request.session['user_id'] = user.id
            request.session['user_name'] = user.name
            messages.success(request, 'Successfully logged in')
            return redirect('index')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')

def logout(request):
    request.session.pop('user_id', None)
    request.session.pop('user_name', None)
    messages.info(request, 'You have been logged out')
    return redirect('index')

def add_to_cart_view(request, item_id):
    # Logic to add the item with item_id to the cart
    return HttpResponse(f"Item {item_id} added to cart.")

def remove_from_cart(request, item_id):
    cart = request.session.get('cart', [])
    cart = [item for item in cart if item['item_id'] != item_id]
    request.session['cart'] = cart
    return redirect('cart')

def remove_from_cart_view(request, item_id):
    cart = request.session.get('cart', [])
    cart = [item for item in cart if item['item_id'] != item_id]
    request.session['cart'] = cart
    return HttpResponse(f"Item {item_id} removed from cart.")

def buy(request):
    # Render checkout page on GET, process payment on POST
    cart = request.session.get('cart', [])
    # menu mapping (same as cart())
    menu = {
        1: {'name': 'Burger', 'price': 120},
        2: {'name': 'Chicken Burger', 'price': 120},
        3: {'name': 'Chicken Roll', 'price': 60},
        4: {'name': 'Butter Chicken', 'price': 80},
        5: {'name': 'Egg Fried Rice', 'price': 120},
        6: {'name': 'Chicken Biryani', 'price': 160},
        7: {'name': 'Butter Chicken (Large)', 'price': 280},
        8: {'name': 'Chicken Shawarma', 'price': 120},
        9: {'name': 'Chicken Nuggets', 'price': 90},
        10: {'name': 'Tandoori Chicken', 'price': 80},
        11: {'name': 'Prawn Fry', 'price': 100},
        12: {'name': 'Egg Curry', 'price': 60},
        13: {'name': 'Butter Chicken (Special)', 'price': 160},
        14: {'name': 'Veg Sandwich', 'price': 90},
        15: {'name': 'White Sauce Pasta', 'price': 60},
        16: {'name': 'French Fries', 'price': 70},
        17: {'name': 'Veg Hakka Noodles', 'price': 70},
        18: {'name': 'Paneer Tikka', 'price': 90},
        19: {'name': 'Veg Biryani', 'price': 180},
        20: {'name': 'Veg Manchurian', 'price': 150},
        21: {'name': 'Chole Bhature', 'price': 50},
        22: {'name': 'Masala Dosa', 'price': 55},
        23: {'name': 'Idli Sambar', 'price': 40},
    }
    cart_items = []
    total = 0
    for entry in cart:
        item = menu.get(entry['item_id'])
        if item:
            subtotal = item['price'] * entry['quantity']
            total += subtotal
            cart_items.append({
                'item_id': entry['item_id'],
                'name': item['name'],
                'price': item['price'],
                'quantity': entry['quantity'],
                'subtotal': subtotal,
            })

    if request.method == 'POST':
        # process payment selection (this example simulates processing)
        payment_method = request.POST.get('payment_method')
        # simple validation: ensure cart not empty
        if not cart_items:
            messages.info(request, 'Your cart is empty.')
            return redirect('cart')

        # In a real app you would integrate with a payment gateway here.
        # For now: clear cart and thank the user.
        request.session['cart'] = []
        messages.success(request, f'Payment method: {payment_method}. Purchase completed. Thank you!')
        return redirect('index')

    # GET: show checkout page
    if not cart_items:
        messages.info(request, 'Your cart is empty.')
        return redirect('cart')
    return render(request, 'buy.html', {'cart_items': cart_items, 'total': total})
