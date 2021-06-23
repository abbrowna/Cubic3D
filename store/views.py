"""
Definition of views for the store application.
"""

from datetime import datetime, timedelta, timezone
from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse
from .forms import FilterForm, OrderForm, SignUpForm, ProfileForm, UserForm
from verify_email.email_handler import send_verification_email
from store.models import Material, Filament, Order, OrderDetail
from app.models import Region
from django.contrib.auth.decorators import login_required 
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.conf import settings
import os
import urllib
import requests
import base64

#lifespan for preorders and timezone
lifespan = timedelta(hours=1)
tz = timedelta(hours=3)

def link_callback(uri, rel):
    sUrl = settings.STATIC_URL
    mUrl = settings.MEDIA_URL
    sRoot = settings.STATIC_ROOT
    if uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
        path = urllib.parse.unquote(path)
    else:
       return uri

    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path

def home(request):
    """Renders the store home page"""
    assert isinstance(request, HttpRequest)
    
    return render(request, 'app/index.html',{
        'title':'Cubic3D Store',
        'message': 'The shop that keeps you 3D printing',
        'year':datetime.now().year,
    })


def filamentLanding(request):
    """Renders the filament landing page."""
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        form = FilterForm(request.POST)
        if form.is_valid():
            dia = form.data['diameter']
            matl = form.data['material']
            return redirect('filament',diameter = dia, material = matl)
    else:
        if not 'cart_items' in request.session:
            request.session['cart_items'] = []
        
        num_cart_items = len(request.session['cart_items'])

        form = FilterForm()
        class Matl:
            def __init__(self, name, stock):
                self.name = name
                self.stock = stock
        materials = []
        mats = Material.objects.all()
        for m in mats:
            matl_stock = Filament.objects.filter(material = m).filter(stock__gt = 0)
            M = Matl(m.name, len(matl_stock))
            materials.append(M)
        return render(
            request,
            'app/fil_landing.html',
            {
                'materials':materials,
                'title':'Cubic3D Store - Buy 3D printing filament with Local delivery',
                'year':datetime.now().year,
                'form':form,
                'num_cart_items': num_cart_items,
                'description': 'Cubic3D store confidently offers a selection of high quality 3D printing filament because we use the same in our print farm all day.'
            }
    )


def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Cubic3D - Contact Us',
            'message':'Your contact page.',
            'year':datetime.now().year,
            'description':'You can easily reach the Cubic3D team and talk to us through these channels.',
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'Cubic3D - About us',
            'message':'About us',
            'year':datetime.now().year,
            'description':'Learn more about us, how we came to be and why you can trust our products.',
        }
    )

def howTo(request):
    """renders the how to assemble page"""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/howto.html',
        {
            'title':'Cubic3D - How to refill reusable spools',
            'message':'A simple guide on how to use Esun re-usable spools',
            'year':datetime.now().year,
            'description':'Learn the easy steps to refill a re-usable spool and reduce plastic waste created by used up spools.',
        }
    )

def filament(request, diameter, material):
    """renders available filament after filtering"""
    assert isinstance(request, HttpRequest)
    filtered_filament = Filament.objects.filter(diameter = diameter).filter(material__name = material).order_by('price')
    instock = Filament.objects.filter(stock__gt = 0)
    try:
        num_cart_items = len(request.session['cart_items'])
    except:
        num_cart_items = 0
    return render(
        request,
        'app/filament.html',
        {
            'title': 'Cubic3D - '+str(diameter)+'mm '+material,
            'description': 'Our selection of '+str(diameter)+'mm '+material+' that we know you will love.',
            'message':'Filament available for you',
            'year':datetime.now().year,
            'material':material,
            'diameter':diameter,
            'filtered':filtered_filament,
            'num_cart_items': num_cart_items,
            'instock':len(instock) > 0
            }
        )

def addToCart(request):
    """Adds an item to the cart using an Ajax request"""
    assert isinstance(request, HttpRequest)
    product_id = request.GET['product_id']
    cart_items = request.session['cart_items']

    stock = Filament.objects.get(pk=product_id).stock
    current_quantity = cart_items.count(product_id)

    if current_quantity < stock:
        cart_items.append(product_id)
        request.session['cart_items'] = cart_items
        success = True
    else:
        success = False
    data = {
        'numOfItems': len(cart_items),
        'added': success
    }
    return JsonResponse(data)

def updateCart(request):
    """Updates the cart with the correct current value"""
    assert isinstance(request, HttpRequest)
    try:
        if 'cart_items' in request.session:
            cart_items = request.session['cart_items']
        else:
            cart_items = []
            request.session['cart_items'] = cart_items
    except:
        cart_items = []
    data = {
        'numOfItems': len(cart_items),
    }
    return JsonResponse(data)

def removeFromCart(request):
    """Removes an item from the cart using Ajax request"""
    assert isinstance(request, HttpRequest)
    product_id = request.GET['product_id']
    cart_items = request.session['cart_items']
    cart_items.remove(product_id)
    request.session['cart_items'] = cart_items
    data = {
        'numOfItems': len(cart_items)
    }
    return JsonResponse(data)

def cart(request):
    """Shows items in the shopping cart"""
    assert isinstance(request, HttpRequest)

    cleaned_cart_items = []
    cart_quantity = []
    
    cart_items = request.session['cart_items']
    for item in cart_items:
        if item in cleaned_cart_items:
            index = cleaned_cart_items.index(item)
            cart_quantity[index] = cart_quantity[index] + 1
        else:
            cleaned_cart_items.append(item)
            cart_quantity.append(1)
            
    cart_filaments = []
    for id in cleaned_cart_items:
        cart_filaments.append(Filament.objects.get(pk=id))

    class CartFilament:
        def __init__(self, filament, quantity):
            self.filament = filament
            self.quantity = quantity

    
    classed_filament = []
    subtotal = 0
    
    for idx, filament in enumerate(cart_filaments):
        subtotal = subtotal + (filament.price * cart_quantity[idx])
        fil = CartFilament(filament, cart_quantity[idx])
        classed_filament.append(fil)

    request.session['cleaned_cart_items'] = cleaned_cart_items
    request.session['cart_quantity'] = cart_quantity

    return render(
        request,
        'app/cart.html',
        {
            'title': 'Cart',
            'message':'Your shopping cart',
            'year':datetime.now().year, 
            'items': classed_filament,
            'subtotal': subtotal
        }
    )


def checkout(request):
    """present the checkout page"""
    assert isinstance(request, HttpRequest)
    
    cleaned_cart_items = request.session['cleaned_cart_items']
    cart_quantity = request.session['cart_quantity']

    class CartFilament:
        def __init__(self, filament, quantity):
            self.filament = filament
            self.quantity = quantity
        
    classed_filament = []
    subtotal = 0
    for idx, id in enumerate(cleaned_cart_items):
        filament = Filament.objects.get(pk=id)
        classed_filament.append(CartFilament(filament, cart_quantity[idx]))
        subtotal = subtotal + filament.price * cart_quantity[idx] 

    usr = request.user
    
      
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            new_order = form.save()
            if usr.is_authenticated:
                new_order.user = usr
                if form.cleaned_data["set_default"]:
                    usr.profile.address = form.cleaned_data["address"]
                    usr.profile.region = form.cleaned_data["region"]
                    usr.save()
            
            item_total = 0
            for item in classed_filament:
                order_detail = OrderDetail(
                    order = new_order,
                    filament = item.filament,
                    quantity = item.quantity
                )
                order_detail.save()
                item_total = item_total + item.filament.price * item.quantity
            new_order.item_total = item_total
            new_order.delivery_fee = new_order.region.cost
            new_order.save()

            for item in classed_filament:
                item.filament.stock = item.filament.stock - item.quantity
                item.filament.save()

            del request.session['cleaned_cart_items']
            del request.session['cart_quantity']
            request.session['cart_items'] = []
            request.session['order_id'] = new_order.pk

            subject = '3D filament Order # ' + new_order.num()
            to = new_order.email
            from_email = 'Cubic3D Store<orders@Cubic3D.co.ke>'
            body =  render_to_string('email/preorder.html',
                    {
                        'name':new_order.first_name,
                        'order':new_order,
                        'details':classed_filament,
                        'date':new_order.time.strftime("%d %b %Y")
                    })
            msg = EmailMessage(subject, body, from_email, [to])
            msg.content_subtype = "html"
            msg.send()

            return(redirect('orderReview'))

    else:
        form = OrderForm()
    

    return render(
        request,
        'app/checkout.html',
        {
            'title':'Checkout',
            'message':'Checkout',
            'year':datetime.now().year,
            'filaments':classed_filament,
            'subtotal':subtotal,
            'form':form,
            'user':usr,
            'auth':usr.is_authenticated
        }
    )

@staff_member_required
def releaseStock(request):
    """Release stock that was held by old orders"""
    tz = timedelta(hours=3)
    now = datetime.now(timezone(tz))

    potential = Order.objects.filter(paid=False)
    for p in potential:
        if (now - p.time > lifespan):
            items = OrderDetail.objects.filter(order=p.pk)
            for i in items:
                filament = Filament.objects.get(pk=i.filament.pk)
                filament.stock = filament.stock + i.quantity
                filament.save()
            p.delete()
    
    data = {
        'success': True
    }
    return JsonResponse(data)




def updateDelivery(request):
    """Auto update the delivery cost via ajax"""
    assert isinstance(request, HttpRequest)
    region_id = request.GET['region_id']
    cost = Region.objects.get(pk=region_id).cost
    data = {
        'cost': cost
    }
    return JsonResponse(data)

def mpesaExpress(request):
#    """Send an stk push for payment to the user and process it"""
#    #get authorization​
#    response = requests.request(
#        "GET", 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials', 
#        headers = { 'Authorization': 'Basic cFJZcjZ6anEwaThMMXp6d1FETUxwWkIzeVBDa2hNc2M6UmYyMkJmWm9nMHFRR2xWOQ==' }
#    )
#    print(response.status_code)
#    token = response.json()["access_token"]
#    print(token)
    
    #perform push   ​
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic '+token
    }
    timestamp = datetime.now(timezone(tz)).strftime("%Y%m%d%H%M%S")
    shortcode = 174379
    b64_pass = base64.b64encode(str(shortcode).encode("ascii")+token.encode("ascii")+timestamp.encode("ascii"))
    payload = {
        "BusinessShortCode": shortcode,
        "Password": b64_pass,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": 254700888557,
        "PartyB": shortcode,
        "PhoneNumber": 254700888557,
        "CallBackURL": "https://mydomain.com/path",
        "AccountReference": "CompanyXLTD",
        "TransactionDesc": "Payment of X" 
    }
    
    response = requests.request("POST", 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v2/processrequest', headers = headers, data = payload)
    print(response.text.encode('utf8'))

    return redirect('filamentHome')

def apiCallback(request):
    if request.method == 'POST':
        pass #toDo process the callback Json response
    else:
        pass #just checking if the method is GET
    return True

def orderReview(request):
    """Order review and payment information"""
    assert isinstance(request, HttpRequest)
    order_id = int(request.session['order_id'])
    order = Order.objects.get(pk = order_id)
    details = OrderDetail.objects.filter(order = order_id)

    return render(
        request,
        'app/order_review.html',
        {
            'title':'Pre-Order',
            'message':'Your order has been placed',
            'year':datetime.now().year,
            'order':order,
        }
    )

@staff_member_required
def myadmin(request):
    """Renders the main administration page"""
    assert isinstance(request, HttpRequest)
    filament = Filament.objects.order_by('diameter','material','color')
    
    #materials = Material.objects.all()
    #oos = []
    #for matl in materials:
    #    per_matl = Filament.objects.filter(material=matl)
    
    
    return render(
        request,
        'admin/myadmin.html',
        {
            'title':'Administration',
            'message':'Filament store Admin',
            'year':datetime.now().year,
            'filament':filament,
        }
    )

@staff_member_required
def preOrders(request):
    """Renders the page to view preorders"""
    assert isinstance(request, HttpRequest)
    details = [] 
    preorders = Order.objects.filter(paid=False)

    for preorder in preorders:
        order_details = OrderDetail.objects.filter(order = preorder.pk)
        details.append([preorder,order_details])
    
    now = datetime.now(timezone(tz))
    expired = []
    potential = Order.objects.filter(paid=False)
    for p in potential:
        if now - p.time > lifespan:
            expired.append(p)


    return render(
        request,
        'admin/preorders.html',
        {
            'title':'Pre-Orders',
            'message':'View pre-orders',
            'year':datetime.now().year,
            'details':details,
            'num_exp':len(expired),
            'expired':expired
        }
    )

@staff_member_required
def pendingOrders(request):
    """Renders the page to view Orders that have been paid for but not delivered"""
    assert isinstance(request, HttpRequest)
    details = [] 
    orders = Order.objects.filter(paid=True).filter(delivered=False)

    for o in orders:
        order_details = OrderDetail.objects.filter(order = o.pk)
        details.append([o,order_details])


    return render(
        request,
        'admin/pending.html',
        {
            'title':'Pre-Orders',
            'message':'View pending orders',
            'year':datetime.now().year,
            'details':details,
        }
    )

@staff_member_required
def completedOrders(request):
    """Renders the page to view Completed orders"""
    assert isinstance(request, HttpRequest)
    details = [] 
    completed = Order.objects.filter(paid=True).filter(delivered=True)

    for c in completed:
        order_details = OrderDetail.objects.filter(order = c.pk)
        details.append([c,order_details])


    return render(
        request,
        'admin/completed.html',
        {
            'title':'Pre-Orders',
            'message':'View completed orders',
            'year':datetime.now().year,
            'details':details,
        }
    )

@staff_member_required
def setPaid(request):
    """set the paid field of a specific order"""
    assert isinstance(request, HttpRequest)
    order_id = int(request.GET['order_id'])
    order = Order.objects.get(pk=order_id)
    details = OrderDetail.objects.filter(order = order_id)

    subject = '3D filament Order # ' + order.num()
    to = order.email
    from_email = 'Cubic3D store<orders@Cubic3D.co.ke>'
    body =  render_to_string('email/order_confirm.html',
            {
                'name':order.first_name,
                'details':details,
                'order':order,
            },request)
    pdf_content = render_to_string('email/pdf_receipt.html',
            {
                'paid_date':datetime.now().strftime("%d %b %Y"),
                'order_date': order.time.strftime("%d %b %Y"),
                'order':order,
                'details':details,
            },request)

    receipt_path = "receipts/RCPT-F" + order.num() + ".pdf"
    pdf_receipt = open(receipt_path,"w+b")
    pisastatus = pisa.CreatePDF(pdf_content,dest=pdf_receipt,link_callback=link_callback)
    pdf_receipt.close()

    msg = EmailMessage(subject, body, from_email, [to])
    msg.content_subtype = "html"
    msg.attach_file(receipt_path)
    msg.send()

    order.paid = True
    order.save()

    data = {
        'success': True
    }
    return JsonResponse(data)

@staff_member_required
def setDelievered(request):
    """set the delievered field of a specific order"""
    assert isinstance(request, HttpRequest)
    order_id = request.GET['order_id']
    order = Order.objects.get(pk=order_id)
    order.delivered = True
    order.save()

    data = {
        'success': True
    }
    return JsonResponse(data)

@staff_member_required
def emailViewer(request):
    """temporary view for email development"""
    assert isinstance(request, HttpRequest)
    
    order_id = 5
    #order_id = request.session['order_id']
    order = Order.objects.get(pk = order_id)
    details = OrderDetail.objects.filter(order = order_id)
    request.session['order_id'] = 5

    return render(
        request,
        'email/order_confirm.html',
        {
            'paid_date':datetime.now().strftime("%d %b %Y"),
            'order_date': order.time.strftime("%d %b %Y"),
            'order':order,
            'details':details,
        }
    )

def signup(request):
    if request.method == 'POST':
        user_form = SignUpForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            inactive_user = send_verification_email(request, user_form)
            inactive_user.refresh_from_db()
            profile_form = ProfileForm(request.POST, instance=inactive_user.profile)
            profile_form.full_clean()
            profile_form.save()
            
            email = user_form.cleaned_data.get('email')

            return redirect('pending_verification', user_email=email)

    else:
        user_form = SignUpForm()
        profile_form = ProfileForm()
    return render(request,'registration/signup.html',
        {
            'user_form': user_form,
            'profile_form': profile_form,
            'title':'SignUp',
            'description':'Create an account with Cubic3D 3D printing service.',
            'year':datetime.now().year,                            
        }
    )

def pending_verification(request, user_email):
    """A page directing new users to verify their email"""
    assert isinstance(request, HttpRequest)
    return render(request, 'registration/pending_verification.html',
        {
            'title':'Verify your email',
            'year':datetime.now().year, 
            'user_email':user_email,
        }
    )

@login_required
def accountOverview(request):
    """Show the user an overview of their account"""
    assert isinstance(request, HttpRequest)
    if request.user.is_authenticated:
        u = request.user
        user_orders = Order.objects.filter(user=u.pk)
        details = []
        for o in user_orders:
            order_details = OrderDetail.objects.filter(order = o.pk)
            details.append([o,order_details])
    else:
        return redirect('login')
    return render(request, 'registration/acc_overview.html',
        {
            'title': 'Account overview',
            'year':datetime.now().year,
            'user': u,
            'details':details,
        }     
    )

@login_required
def editProfile(request):
    """Allow user to update profile details"""
    assert isinstance(request,HttpRequest)
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        user_form = UserForm(request.POST, instance=request.user)
        profile_form.save()
        user_form.save()
        return redirect('acc_overview')
    else:
        profile_form = ProfileForm(instance = request.user.profile)
        user_form = UserForm(instance = request.user)
        username = request.user.username
    return render(request, 'registration/edit_profile.html', 
        {
            'profile_form':profile_form,
            'user_form':user_form,
            'title':'Edit Profile',
            'username':'username'
        }
    )

