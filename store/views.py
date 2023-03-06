from django.shortcuts import render, HttpResponse,redirect
from store.forms.authforms import CustomerCreationForm, CustomerLoginForm
# from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login as loginUser,logout as lgout
from store.models import Tshirt
from django.db.models import Min
from math import floor

 
# Create your views here.

def show_product(request, slug):
    tshirt = Tshirt.objects.get(slug=slug)
    size = request.GET.get('size')

    if size is None:
        size  = tshirt.sizevarient_set.all().order_by('price').first()
    else:
        size  = tshirt.sizevarient_set.get(size = size)

    size_price  = floor(size.price)
    sell_price  = size_price - (size_price * (tshirt.discount / 100))
    sell_price = floor(sell_price)
    
    context={'tshirt':tshirt, 'price':size_price, 'sell_price':sell_price, 'active_size': size }

    return render(request, template_name='store/product_details.html', context=context )
   


def home(request):
    tshirts = Tshirt.objects.all()
        
    context={
        "tshirts":tshirts
    }
    return render(request, template_name='store/home.html', context=context)


def cart(request):
    return render(request,template_name='store/cart.html')


def orders(request):
    return render(request, template_name='store/orders.html')


def login(request):
    if request.method=='GET':
        form = CustomerLoginForm()
        return render(request, template_name='store/login.html',  context={"form":form})
    
    else:
        form=CustomerLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=username, password=password)

            if user:
                loginUser(request,user)
                return redirect('homepage')
        else:
           return render(request, template_name='store/login.html', context={"form":form})



def signup(request):
    if(request.method =='GET'):
        form=CustomerCreationForm()
        context={
            "form":form
        }
        return render(request, template_name='store/signup.html',context=context)

    else:
        form=CustomerCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            print(user)
            user.email = user.username
            user.save()
            return render(request, template_name='store/login.html')
        context = {
            "form":form
        }
        return render(request, template_name='store/signup.html',context=context)


def logout(request):
    # request.session.clear()
    lgout(request)
    return render(request, template_name='store/home.html')
    


def add_to_cart(request, slug, size):
    cart = request.session.get('cart')
    if cart is None:
        cart = []

    tshirt = Tshirt.objects.get(slug = slug)

    flag = True
    for cart_obj in cart:
        t_id = cart_obj.get('tshirt')
        size_temp = cart_obj.get('size')
        if t_id == tshirt.id and size == size_temp:
            cart_obj['quantity'] = cart_obj['quantity']+1

    if flag:
        cart_obj = {
            'tshirt': tshirt.id,
            'size': size,
            'quantity': 1
        }
        cart.append(cart_obj)
    request.session['cart'] = cart
    # print(cart)
    return_url = request.GET.get('return_url')

    return redirect(return_url)