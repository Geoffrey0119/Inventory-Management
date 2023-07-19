from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Product, Order
from django.shortcuts import render
from django.contrib.auth import authenticate, login
import statistics
from django.shortcuts import render
from .models import Product

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if validate_user(username, password):
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('main_menu')
        else:
            messages.error(request, 'Invalid username or password. Login failed.')
            return redirect('login')

    return render(request, 'login.html')

def inventory_view(request):
    products = Product.objects.all()
    return render(request, 'inventory.html', {'products': products})

def validate_user(username, password):
    user = authenticate(username=username, password=password)
    return user is not None


def main_menu(request):
    return render(request, 'main_menu.html')


def add_item_menu(request):
    if request.method == 'POST':
        item_name = request.POST.get('item_name')
        item_price = request.POST.get('item_price')
        item_stock = request.POST.get('item_stock')

        if item_name and item_price and item_stock:
            try:
                item_price = float(item_price)
                item_stock = int(item_stock)
                new_item = Product(name=item_name, price=item_price, stock=item_stock)
                new_item.save()
                messages.success(request, 'Item added to the menu.')
                return redirect('main_menu')
            except ValueError:
                messages.error(request, 'Invalid item price or stock. Please enter valid numbers.')
                return redirect('add_item_menu')
        else:
            messages.error(request, 'Item name, price, and stock are required.')
            return redirect('add_item_menu')

    return render(request, 'add_item_menu.html')


def view_menu(request):
    products = Product.objects.all()
    return render(request, 'view_menu.html', {'products': products})


def remove_item_menu(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')

        if item_id:
            try:
                item = Product.objects.get(pk=item_id)
                item.delete()
                messages.success(request, f"Item '{item.name}' removed from the menu.")
                return redirect('main_menu')
            except Product.DoesNotExist:
                messages.error(request, 'Invalid item ID. Please select a valid item.')
                return redirect('remove_item_menu')
        else:
            messages.error(request, 'Item ID is required.')
            return redirect('remove_item_menu')

    products = Product.objects.all()
    return render(request, 'remove_item_menu.html', {'products': products})


def menu_and_order(request):
    if request.method == 'POST':
        choice = request.POST.get('choice')
        quantity = request.POST.get('quantity')

        if choice == 'q':
            cart = request.session.get('cart', [])
            total = calculate_total(cart)
            request.session['total'] = total
            return redirect('generate_receipt')

        try:
            product = Product.objects.get(pk=choice)
            quantity = int(quantity)

            if quantity > 0 and quantity <= product.stock:
                cart = request.session.get('cart', [])
                cart.append((product.id, product.name, product.price, quantity))  # Store only necessary information
                product.stock -= quantity
                product.save()
                request.session['cart'] = cart
                messages.success(request, f"{quantity} {product.name}(s) added to the cart.")
            else:
                messages.error(request, 'Invalid quantity. Please select a valid quantity.')
        except Product.DoesNotExist:
            messages.error(request, 'Invalid choice. Please select a valid product.')

        return redirect('menu_and_order')

    products = Product.objects.all()
    cart = request.session.get('cart', [])
    total = request.session.get('total', 0)
    return render(request, 'menu_and_order.html', {'products': products, 'cart': cart, 'total': total})


def calculate_total(cart):
    total = 0

    for product_id, _, price, quantity in cart:
        total += price * quantity

    return total


def home(request):
    return render(request, 'home.html')


def generate_receipt(request):
    cart = request.session.get('cart', [])
    total = request.session.get('total', 0)
    request.session['cart'] = []
    request.session['total'] = 0
    return render(request, 'generate_receipt.html', {'cart': cart, 'total': total})

def inventory_view(request):
    return render(request, 'inventory.html')

def inventory_management(request):
    products = Product.objects.all()
    return render(request, 'inventory_management.html', {'products': products})


def sales_order_analytics(request):
    orders = Order.objects.all()
    order_values = [order.total_amount for order in orders]
    total_sales = sum(order_values)
    avg_order_value = statistics.mean(order_values) if order_values else 0
    max_order_value = max(order_values) if order_values else 0
    min_order_value = min(order_values) if order_values else 0

    context = {
        'total_sales': total_sales,
        'avg_order_value': avg_order_value,
        'max_order_value': max_order_value,
        'min_order_value': min_order_value,
    }

    return render(request, 'sales_order_analytics.html', context)
