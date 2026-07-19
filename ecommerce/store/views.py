from django.shortcuts import render, redirect
from .models import Customer, Product, Order
def search(request):

    query = request.GET.get('q', '').lower().strip()

    if 'shoe' in query:

        return redirect('/product/shoes/')

    elif 'headphone' in query:

        return redirect('/product/headphones/')

    elif 'watch' in query:

        return redirect('/product/watch/')

    elif 'backpack' in query:

        return redirect('/product/backpack/')

    return redirect('/')
def home(request):
    return render(request, 'home.html')

def product_detail(request):
    return render(request, 'product_detail.html')

def register(request):

    if request.method == 'POST':

        name = request.POST['name']

        email = request.POST['email']

        password = request.POST['password']

        Customer.objects.create(

            name=name,

            email=email,

            password=password

        )

        return redirect('/')

    return render(request, 'register.html')

def login(request):

    message = ""

    if request.method == 'POST':

        email = request.POST['email']

        password = request.POST['password']

        try:

            customer = Customer.objects.get(

                email=email,

                password=password

            )

            message = f"Welcome {customer.name}"

        except Customer.DoesNotExist:

            message = "Invalid email or password"

    return render(

        request,

        'login.html',

        {'message': message}

    )
def cart(request):
    return render(request, 'cart.html')

def order(request):

    message = ""

    if request.method == 'POST':

        customer_email = request.POST['email']

        product_name = request.POST['product']

        try:

            customer = Customer.objects.get(

                email=customer_email

            )

            product = Product.objects.get(

                name=product_name

            )

            Order.objects.create(

                customer=customer,

                product=product,

                quantity=1

            )

            message = "Order placed successfully 🎉"

        except:

            message = "Customer or Product not found"

    return render(

        request,

        'order.html',

        {'message': message}

    )

def shoes(request):
    return render(request, 'shoes.html')

def headphones(request):
    return render(request, 'headphones.html')

def watch(request):
    return render(request, 'watch.html')

def backpack(request):
    return render(request, 'backpack.html')

def order_history(request):

    orders = Order.objects.all().order_by('-ordered_at')

    return render(

        request,

        'order_history.html',

        {'orders': orders}

    )

def logout(request):
    return render(request, 'logout.html')