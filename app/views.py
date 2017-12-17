"""
Definition of views.
"""

from django.shortcuts import render, redirect
from django.template import RequestContext
from datetime import datetime, timedelta
from django.contrib.auth import login, authenticate
from app.forms import SignUpForm, TempThingForm, EmailForm, QuoteForm, ScaleForm
from app.models import Tempthings, ThingOrders, Quote
from app.genratehtml import accepthtml, rejecthtml
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.http import Http404, HttpResponse, HttpRequest
from django.core.mail import EmailMessage, send_mail
import os
from sys import platform

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact Us',
            'message':'We\'d love to be of any assistance we can. You can get to us by writing to:',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(request,'app/about.html',
        {
            'title':'About',
            'message':'Cubic3D is your hobbyist paradise.',
            'year':datetime.now().year,
        }
    )

def materials(request):
    """Renders the materials page."""
    assert isinstance(request, HttpRequest)
    return render(request,'app/materials.html',
        {
            'title':'Materials and Options',
            'message':'Which material should you choose?',
            'year':datetime.now().year,
        }
    )

def def_quote(request):
    """Renders page for part upload to get quote"""
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        form = QuoteForm(request.POST, request.FILES)
        if form.is_valid():
            temp = form.save()
            request.session['quotename']=form.cleaned_data['thing'].name
            request.session['quoteid']=temp.id
            return redirect('quote_review')
    else:
        form = QuoteForm()
    return render(request, 'app/def_quote.html',
        {
            'form':form,
            'title':'Upload & Options.',
            'year':datetime.now().year,
        }
    )

@login_required
def upload(request):
    """Renders part upload page"""
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        form = TempThingForm(request.POST, request.FILES)
        if form.is_valid():
            temp = form.save(commit=False)
            temp.user = request.user
            request.session['file_name']=form.cleaned_data['thing'].name
            temp.save()
            request.session['thing_id']=temp.id
            return redirect('review_n_info')
    else:
        form = TempThingForm()
    return render(request,'app/upload.html',
        {
            'form':form,
            'title':'Upload & Options.',
            'year':datetime.now().year,
        }
    )

@staff_member_required
def download(request, path):
    if platform != 'win32':
        path = r'/{0}'.format(path)
    with open(path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/vnd.stl")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(path)
        return response

@staff_member_required
def set_printed(request, id):
    part=ThingOrders.objects.get(upload_id=id)
    part.printed=True
    part.save()
    return redirect('orders')
        
def quote_review(request):
    """Renders the review page of a quote"""
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        form = ScaleForm(request.POST)
        if form.is_valid():
            from app.stlprocessing import setscale
            quoteid=request.session.get('quoteid')
            quote = Quote.objects.get(id=quoteid)
            requiredscale=form.cleaned_data['scale']
            if requiredscale is None:
                requiredscale = 100
            setscale(quote.thing.path,quote.scale,requiredscale)
            quote.scale = requiredscale
            quote.save()
            return redirect('quote_review')
    else:
        quoteid = request.session.get('quoteid')
        quotename = request.session.get('quotename')
        quote = Quote.objects.get(id=quoteid)
        formdata = {'scale':quote.scale}
        form = ScaleForm(initial=formdata)
        mass,price = quote.thing_price()
    return render(request, 'app/quote_review.html',
        {
            'form':form,
            'filename':quotename,
            'slicemass':mass,
            'purpose':quote.purpose,
            'material':quote.material,
            'color':quote.color,
            'price':price,
            'priceupper':price*1.2,
            'stlpath':quote.thing.url,
            'year':datetime.now().year,
            'title':'Quote Review and info',
        }
    )

def review_n_info(request):
    """Renders the confirmation and info view"""
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        form = ScaleForm(request.POST)
        if form.is_valid():
            from app.stlprocessing import setscale
            thing_id=request.session.get('thing_id')
            part=Tempthings.objects.get(id=thing_id)
            requiredscale=form.cleaned_data['scale']
            if requiredscale is None:
                requiredscale = 100
            setscale(part.thing.path,part.scale,requiredscale)
            part.scale = requiredscale
            part.save()
            return redirect('review_n_info')
    else:
        thing_id=request.session.get('thing_id')
        file_name=request.session.get('file_name')
        part=Tempthings.objects.get(id=thing_id)
        formdata = {'scale':part.scale}
        form = ScaleForm(initial=formdata)
        mass,price=part.thing_price()
    return render(request,'app/review_n_info.html',
        {
            'form':form,
            'slicemass':mass,
            'description':part.description,
            'filename':file_name,
            'purpose':part.purpose,
            'material':part.material,
            'color':part.color,
            'colorinfo':part.color_combo,
            'further_requests':part.further_requests,
            'title':'Review and final info',
            'year':datetime.now().year,
            'price':price,
            'priceupper':price*1.2,
            'stlpath':part.thing.url,
        }
    )

def cancel (request):
    """perofrms the cancel action"""
    assert isinstance(request, HttpRequest)
    thing_id=request.session.get('thing_id')
    part=Tempthings.objects.get(id=thing_id)
    os.remove(part.thing.path)
    part.delete()
    return redirect('home')

def delquote(request):
    """cleans up the quote from storage"""
    assert isinstance(request, HttpRequest)
    quoteid = request.session.get('quoteid')
    quote=Quote.objects.get(id=quoteid)
    os.remove(quote.thing.path)
    quote.delete()
    return redirect('home')

def delete_file(request, requestid):
    """delete the actual file from storage"""
    assert isinstance(request, HttpRequest)
    part=Tempthings.objects.get(id=requestid)
    try:
        os.remove(part.thing.path)
    except:
        pass
    part.delete()
    return redirect('abandoned')

def thanks(request):
    """thank you and quick links page"""
    assert isinstance(request, HttpRequest)
    send_mail('new print request', 'There\'s a new print request for you. Check it out', 'orders@cubic3d.co.ke', ['abbrowna@cubic3d.co.ke','noelkimwatan@cubic3d.co.ke'])
    return render(request,'app/thanks.html',
        {
            'title':'Thanks for the request',
            'year':datetime.now().year,
        }
    )

def confirm_print(request,thing_id):
    """this view transfers a tempthing to the orders model"""
    assert isinstance(request, HttpRequest)
    try:
        part=Tempthings.objects.get(id=thing_id)
        order=ThingOrders()
        order.upload_id=thing_id
        order.description=part.description
        order.user=part.user
        order.thing=part.thing
        order.material=part.material
        order.purpose=part.purpose
        order.color=part.color
        order.color_combo=part.color_combo
        order.scale=part.scale
        order.further_requests=part.further_requests
        order.save()
        part.delete()
        order=ThingOrders.objects.get(upload_id=thing_id)
        send_mail('new print request', 'A request has just been confirmed. Check it out', 'orders@cubic3d.co.ke', ['abbrowna@cubic3d.co.ke','noelkimwatan@cubic3d.co.ke'])
    except Tempthings.DoesNotExist:
        raise Http404("Print request Does not exist. It may have been deleted or you are trying to confirm a request the second time.")
    return render(request, 'app/printconfirmed.html',
        {
            'title':'Print request Confirmed',
            'year':datetime.now().year,
            'description':order.description,
            'purpose':order.purpose,
            'material':order.material,
            'color':order.color,
            'colorinfo':order.color_combo,
            'scale':order.scale,
            'further_requests':order.further_requests,
        }
    )

def myadmin(request):
    """Renders the custom administration page"""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/myadmin.html',
        {
            'title':'Administration panel',
            'year':datetime.now().year,
        }
    )

@staff_member_required
def printrequests(request):
    """Viewer for print requests"""
    assert isinstance(request, HttpRequest)
    requestqueue=Tempthings.objects.filter(confirmation_sent=False).order_by('uploaded_at')
    return render(request,'app/printrequests.html',
        {
            'title':'Print requests that haven\'t been attended to.',
            'year':datetime.now().year,
            'requestqueue':requestqueue,
        }
    )

@staff_member_required
def abandoned(request):
    """Viewer for abandoned print requests"""
    assert isinstance(request, HttpRequest)
    abandoned=Tempthings.objects.filter(confirmation_sent=True).filter(uploaded_at__lt=datetime.now()-timedelta(days=14)).order_by('uploaded_at')
    return render(request,'app/abandoned.html',
        {
            'title':'Print requests that have been abandoned.',
            'year':datetime.now().year,
            'abandoned':abandoned,
        }
    )

@staff_member_required
def accept_or_reject(request, requestid):
    """Provides for sending an acceptance or rejected email"""
    assert isinstance(request, HttpRequest)
    printrequest=Tempthings.objects.get(id=requestid)
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            viable = form.data['viablebool']
            if viable == 'true':
                subject = 'Print Confirmation'
                finalprice = form.cleaned_data['price']
                html_content = accepthtml(printrequest,finalprice)
            else:
                subject = 'Print Request Error'
                html_content = rejecthtml(printrequest,form.cleaned_data['rejectmessage'])
            from_email = 'orders@Cubic3D.co.ke'
            to = printrequest.user.email

            msg = EmailMessage(subject, html_content, from_email, [to])
            msg.content_subtype = "html"  # Main content is now text/html
            msg.send()
            if viable == 'true':
                printrequest.confirmation_sent=True
                printrequest.save()
            else:
                #delete the request and the uploaded file
                os.remove(printrequest.thing.path)
                printrequest.delete()
            return redirect('printrequests')
    else:
        form = EmailForm()
    return render(request,'app/accept_or_reject.html',
        {
            'printrequest':printrequest,
            'form':form,
            'title':'Print requests that havent been attended to.',
            'year':datetime.now().year,
        }
    )


@staff_member_required
def orders(request):
    """View confirmed orders"""
    assert isinstance(request, HttpRequest)
    orderqueue=ThingOrders.objects.order_by('-confirmed_on')
    return render(request,'app/orders.html',
        {
            'title':'View Orders',
            'year':datetime.now().year,
            'orderqueue':orderqueue,
        }
    )

def thingiverse(request):
    """select a file from thingyverse and print it"""
    assert isinstance(request,HttpRequest)
    return render(request, 'app/thingiverse.html',
        {
            'title':'Browse Thingiverse',
            'year':datetime.now().year,
        }
    )

def gallery(request):
    """renders the gallery page"""
    assert isinstance(request, HttpRequest)
    return render(request,'app/gallery.html',
        {
            'title':'Thanks for the request',
            'year':datetime.now().year,
        }
    )

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.mobile = form.cleaned_data.get('mobile')
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request,'app/signup.html',
        {
            'form': form,
            'title':'SignUp',
            'year':datetime.now().year,                            
        }
    )




