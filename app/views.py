"""
Definition of views.
"""

from django.shortcuts import render, redirect
#from django.template import RequestContext
from django.urls import reverse
from django.template.loader import render_to_string
from datetime import datetime, timedelta
from django.contrib.auth import login, authenticate
from app.forms import SignUpForm, TempThingForm, EmailForm, QuoteForm, ScaleForm, GroupInvoiceForm, ProfileForm
from app.models import PrintRequest, Quote, Material, GroupedPrintRequest, GroupRecord, Invoice, ThingOrders
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.http import Http404, HttpResponse, HttpRequest
from django.core.mail import EmailMessage, send_mail
import os
import urllib
from sys import platform
from xhtml2pdf import pisa

def link_callback(uri, rel):
    sUrl = settings.STATIC_URL
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
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Cubic3D - 3D printing service',
            'description':'Professional 3D printing service based in Juja, Kenya producing clean, crisp objects reliably, with pricing that works for everyone',
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
            'description':'Contact channels for our services.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(request,'app/about.html',
        {
            'title':'About our 3D printing services',
            'description':'Simply put, we 3D print your designs and ship the resulting objet to you charging per gram of material used.',
            'year':datetime.now().year,
        }
    )

def materials(request):
    """Renders the materials page."""
    assert isinstance(request, HttpRequest)
    return render(request,'app/materials.html',
        {
            'title':'Materials and Options',
            'description':'A brief explanation of our available 3D printing materials and which one would best suit your application.',
            'year':datetime.now().year,
        }
    )

def gallery(request):
    """Renders the gallery page."""
    assert isinstance(request, HttpRequest)
    rootdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    photo_names = os.listdir(os.path.join(rootdir, 'app/static/app/images/gallery/'))
    photos = []
    for photo_name in photo_names:
        photo = '/static/app/images/gallery/{0}'.format(photo_name)
        photos.append(photo)
    return render(request,'app/gallery.html',
        {
            'photos':photos,
            'title':'Gallery',
            'description':'A photo collection showing some objects printed by us that will prove we\'re the right team for the job.',
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
            'title':'Upload model & select options to be quoted',
            'description':'Your CAD design can be uploaded here and our trusty online webapp will give you an estimate on the cost of 3D printing it. ',
            'year':datetime.now().year,
        }
    )

def load_colors(request):
    material = request.GET.get('material')
    material_object = Material.objects.get(acronym=material)
    colors = material_object.available_colors()
    combo = len(colors)>1
    return render(request, 'app/color_dropdown.html', {'colors': colors,'combo': combo})

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
            'title':'Upload model & select options.',
            'description':'To get a 3D print, upload your CAD design here, and select the options that best suit your needs.',
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

@staff_member_required
def set_printed(request, id):
    part=PrintRequest.objects.get(pk=id)
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
            'material':quote.material.acronym,
            'color':quote.color,
            'price':price,
            'stlpath':quote.thing.url,
            'year':datetime.now().year,
            'title':'Scale and review 3D print quote request',
            'description':'Here\'s your estimate on the cost of 3D printing the submited model.',
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
            part=PrintRequest.objects.get(id=thing_id)
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
        part=PrintRequest.objects.get(id=thing_id)
        formdata = {'scale':part.scale}
        form = ScaleForm(initial=formdata)
        mass,price=part.thing_price()
    return render(request,'app/review_n_info.html',
        {
            'part':part,
            'form':form,
            'slicemass':mass,
            'filename':file_name,
            'title':'Scale and review 3D print request',
            'description':'See your 3D print request the way we will receive it and change the scale of the model if needed. On submission we will process it manually to give you a final price.',
            'year':datetime.now().year,
            'price':price,
        }
    )

def cancel (request):
    """performs the cancel action"""
    assert isinstance(request, HttpRequest)
    thing_id=request.session.get('thing_id')
    part=PrintRequest.objects.get(id=thing_id)
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

@staff_member_required
def delete_file(request, requestid):
    """delete the actual file from storage"""
    assert isinstance(request, HttpRequest)
    part=PrintRequest.objects.get(id=requestid)
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
            'title':'Request submitted, Thank you!',
            'description':'We have successfully received yor 3D print request, give us some time and we will get back to you on the same.',
            'year':datetime.now().year,
        }
    )

def confirm_print(request,thing_id):
    """Confirm print request to make it an order"""
    assert isinstance(request, HttpRequest)
    try:
        thing_id = int(thing_id)
        printrequest = PrintRequest.objects.get(pk=thing_id)
        if not printrequest.confirmed:
            send_mail('new order', 'Order confirmed', 'orders@cubic3d.co.ke', ['abbrowna@cubic3d.co.ke','noelkimwatan@cubic3d.co.ke'])
        printrequest.confirmed = True
        printrequest.confirmation_date = datetime.now()
        printrequest.save()
        items = [printrequest,]
        return render(request, 'app/printconfirmed.html',
            {
                'printrequests':items,
                'title':'Print confirmed',
                'description':'We will now start 3D printing your model.',
                'year':datetime.now().year,
            }
        )
    except:
        request_IDs = thing_id[1:len(thing_id)-1].split(", ")
        items=[]
        for ID in request_IDs:
            printrequest = PrintRequest.objects.get(id=int(ID))
            printrequest.confirmed = True
            printrequest.confirmation_date = datetime.now()
            printrequest.save()
            items.append(printrequest)

        return render(request, 'app/printconfirmed.html',
            {
                'printrequests':items,
                'title':'Prints confirmed',
                'year':datetime.now().year,
            })

def old_sys_orders(request):
    """ enables viewing if prints from the old system """
    assert isinstance (request , HttpRequest)
    orders = ThingOrders.objects.all()
    return render(request,'myadmin/old_orders.html',
        {
            'orders':orders,
            'title':'Orders from the old system',
            'year':datetime.now().year,
        }
    )
    
@staff_member_required
def myadmin(request):
    """Renders the custom administration page"""
    assert isinstance(request, HttpRequest)
    return render(request,'myadmin/myadmin.html',
        {
            'title':'Administration panel',
            'year':datetime.now().year,
        }
    )

@staff_member_required
def printrequests(request):
    """Viewer for print requests"""
    assert isinstance(request, HttpRequest)
    requestqueue=PrintRequest.objects.filter(confirmation_sent=False).filter(grouped=False).order_by('uploaded_at')
    return render(request,'myadmin/printrequests.html',
        {
            'title':'Print request records',
            'year':datetime.now().year,
            'requestqueue':requestqueue,
        }
    )

@staff_member_required
def accept_or_reject(request, requestid):
    """Provides for sending an acceptance or rejected email"""
    assert isinstance(request, HttpRequest)
    printrequest = PrintRequest.objects.get(id=requestid)
    
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            add_to_group = form.cleaned_data['add_to_group']
            finalprice = form.cleaned_data['price']
            printrequest.final_price = finalprice
            if form.cleaned_data['delivery_fee']:
                delivery_fee = form.cleaned_data['delivery_fee']
            else:
                delivery_fee = 0
            if add_to_group:
                groupedprintrequest = GroupedPrintRequest()
                groupedprintrequest.printrequest = printrequest
                groupedprintrequest.save()
                printrequest.grouped = True
                printrequest.save()
            else:
                if finalprice:
                    printrequest.final_price = finalprice
                    subject = '3D printing invoice'
                    today = datetime.today()
                    #html_content = accepthtml(printrequest,finalprice)
                    html_content = render_to_string('email/accept_request_email.html',
                        {
                            'printrequest':printrequest,
                            'subtotal':(printrequest.subtotal() + delivery_fee),
                            'date':today.strftime("%d-%m-%y"),
                            'bill_to':form.cleaned_data['bill_to'],
                            'confirmation_link':request.build_absolute_uri(reverse('confirm', args=[printrequest.id])),
                            'delivery_fee':delivery_fee,
                        },request
                    )
                    pdf_content = render_to_string('email/pdf_invoice.html',
                        {
                            'printrequest':printrequest,
                            'date':today.strftime("%d-%m-%y"),
                            'subtotal': (printrequest.subtotal() + delivery_fee),
                            'bill_to':form.cleaned_data['bill_to'],
                            'delivery_fee':delivery_fee,
                        },request)
                    
                    invoice_path = "invoices/INV-{}.pdf".format(printrequest.id)
                    pdf_invoice = open(invoice_path,"w+b")
                    pisastatus = pisa.CreatePDF(pdf_content,dest=pdf_invoice,link_callback=link_callback)
                    pdf_invoice.close()
                    from_email = 'orders@Cubic3D.co.ke'
                    to = printrequest.user.email
                    msg = EmailMessage(subject, html_content, from_email, [to])
                    msg.content_subtype = "html"  # Main content is now text/html
                    msg.attach_file(invoice_path)
                    msg.send()
                    printrequest.confirmation_sent=True
                    printrequest.final_price = finalprice
                    printrequest.save()
                    invoice = Invoice()
                    invoice.number = printrequest.id
                    invoice.amount = printrequest.subtotal() + delivery_fee
                    invoice.user = printrequest.user
                    if form.cleaned_data['bill_to']:
                        invoice.bill_to = form.cleaned_data['bill_to']
                    invoice.save()
                
                else:
                    reject_message = form.cleaned_data['rejectmessage']
                    if reject_message:
                        subject = 'Print request error'
                        #html_content = rejecthtml(printrequest,reject_message)
                        html_content = render_to_string('email/reject_request_email.html',
                            {
                                'printrequest':printrequest,
                                'subtotal':printrequest.subtotal(),
                                'date':today.strftime("%d-%m-%y"),
                                'bill_to':form.cleaned_data['bill_to'],
                                'confirmation_link':request.build_absolute_uri(reverse('confirm', args=[printrequest.id])),
                            },request)              
                        from_email = 'orders@Cubic3D.co.ke'
                        to = printrequest.user.email
                        msg = EmailMessage(subject, html_content, from_email, [to])
                        msg.content_subtype = "html"  # Main content is now text/html
                        msg.send()
                    os.remove(printrequest.thing.path)
                    printrequest.delete()

            return redirect('printrequests')
    else:
        form = EmailForm()
    return render(request,'myadmin/accept_or_reject.html',
        {
            'printrequest':printrequest,
            'form':form,
            'title':'Print request actions',
            'year':datetime.now().year,
        }
    )

@staff_member_required
def grouped_requests(request):
    """ Sends 1 invoice for a group of prints"""
    group = GroupedPrintRequest.objects.all()
    if request.method == 'POST':
        form = GroupInvoiceForm(request.POST)
        if form.is_valid():
            grandtotal = 0
            delivery_fee = form.cleaned_data['delivery_fee']
            id_list= []
            for item in group:
                grandtotal += item.printrequest.subtotal()
                id_list.append(item.printrequest.id)
            grandtotal += delivery_fee
            html_content = render_to_string('email/accept_group_email.html',
                {
                    'group':group,
                    'grandtotal':grandtotal,
                    'date':datetime.today().strftime("%d-%m-%y"),
                    'bill_to':form.cleaned_data['bill_to'],
                    'confirmation_link':request.build_absolute_uri(reverse('confirm', args=[str(id_list)])),
                    'delivery_fee':delivery_fee
                },request
            )
            pdf_content = render_to_string('email/group_pdf_invoice.html',
                {
                    'group':group,
                    'grandtotal':grandtotal,
                    'date':datetime.today().strftime("%d-%m-%y"),
                    'bill_to':form.cleaned_data['bill_to'],
                    'delivery_fee':delivery_fee
                },request)
            invoice_path = "invoices/INV-{}.pdf".format(group[0].printrequest.id)
            pdf_invoice = open(invoice_path,"w+b")
            pisastatus = pisa.CreatePDF(pdf_content,dest=pdf_invoice,link_callback=link_callback)
            pdf_invoice.close()
            subject = '3D printing invoice'
            today = datetime.today()
            from_email = 'orders@Cubic3D.co.ke'
            to = group[0].printrequest.user.email
            msg = EmailMessage(subject, html_content, from_email, [to])
            msg.content_subtype = "html"  # Main content is now text/html
            if os.path.isfile(invoice_path):
                msg.attach_file(invoice_path)
            msg.send()
            for item in group:
                printrequest = PrintRequest.objects.get(pk=item.printrequest.id)
                printrequest.confirmation_sent = True
                printrequest.save()
            invoice = Invoice()
            invoice.number = group.first().printrequest.id
            invoice.user = group.first().printrequest.user
            invoice.amount = grandtotal
            if form.cleaned_data['bill_to']:
                invoice.bill_to = form.cleaned_data['bill_to']
            invoice.save()
            group_record = GroupRecord()
            group_record.id_string = str(id_list)
            group_record.save()
            group.delete()
            return redirect('printrequests')
    else:
        form = GroupInvoiceForm()
    return render(request, 'myadmin/grouped_requests.html' ,{
            'group': group,
            'form': form,
            'title':'Grouped request records'
        })

@staff_member_required
def remove_from_group(request, requestid):
    grouped_request = GroupedPrintRequest.objects.get(printrequest__id=requestid)
    grouped_request.delete()
    printrequest = PrintRequest.objects.get(id=requestid)
    printrequest.grouped = False
    printrequest.save()
    return redirect('grouped_requests')

def pdf(request):
    """temporary view for development of pdf"""
    invoice = Invoice.objects.get(number=1)
    today = datetime.today()
    return render(request, 'email/pdf_receipt.html',{
            'invoice':invoice,
            'date':today.strftime("%d-%m-%y"),
        })

@staff_member_required
def orders(request):
    """View confirmed print requests"""
    assert isinstance(request, HttpRequest)
    orderqueue = PrintRequest.objects.filter(confirmed=True).filter(printed=False).order_by('confirmation_date')

    return render(request,'myadmin/orders.html',
        {
            'title':'Pending orders',
            'year':datetime.now().year,
            'orderqueue':orderqueue,
        }
    )

def pending_confirmation(request):
    """View print requests that are pending confirmation"""
    assert isinstance(request, HttpRequest)
    pending_queue = PrintRequest.objects.filter(confirmed=False).filter(confirmation_sent=True).order_by('uploaded_at')
    return render(request, 'myadmin/pending_requests.html',
        {
            'title':'Requests pending confirmation',
            'pending_queue':pending_queue,
            'year': datetime.now().year,
        })

def printed(request):
    """View printed orders"""
    assert isinstance(request, HttpRequest)
    
    class InvoiceForPrinted():
        def __init__(self,invoice,orders,id_list):
            self.invoice=invoice
            self.orders=orders
            self.id_list = id_list
    
    def get_orders(id_list):
        order_list = []
        for id in id_list:
            order = PrintRequest.objects.get(pk=int(id))
            order_list.append(order)
        return order_list
           
    invoices_for_printed = []
    
    printed_objects_ungrouped = PrintRequest.objects.filter(printed=True).filter(receipted=False).filter(grouped=False)    
    for item in printed_objects_ungrouped:
        i = Invoice.objects.get(number=item.id)
        invoices_for_printed.append(InvoiceForPrinted(i,[item,],[item.id,]))

    printed_objects_grouped = PrintRequest.objects.filter(printed=True).filter(receipted=False).filter(grouped=True)
    grouprecords = GroupRecord.objects.all();
    for item in printed_objects_grouped:
        for record in grouprecords:
            if int(record.id_list()[0]) == item.id:
                i = Invoice.objects.get(number=item.id)
                invoices_for_printed.append(InvoiceForPrinted(i,get_orders(record.id_list()),record.id_list()))
    
    return render(request, 'myadmin/printed.html',
        {
            'title':'Invoices of Printed objects',
            'invoices':invoices_for_printed,
            'year': datetime.now().year,
        })

def send_receipt(request, invoice_id, orderlist):
    """sends a receipt for the given invoice to the invoice user"""
    assert isinstance(request, HttpRequest)
    invoice = Invoice.objects.get(number=invoice_id)
    html_content = render_to_string('email/receipt_email.html',
        {
            'invoice':invoice,
            'date':datetime.today().strftime("%d-%m-%y"),
        },request)
    pdf_content = render_to_string('email/pdf_receipt.html',
        {
            'invoice':invoice,
            'date':datetime.today().strftime("%d-%m-%y"),
        },request)
    receipt_path = "receipts/RCPT-{}.pdf".format(invoice.number)
    pdf_receipt = open(receipt_path,"w+b")
    pisastatus = pisa.CreatePDF(pdf_content,dest=pdf_receipt,link_callback=link_callback)
    pdf_receipt.close()
    from_email = 'orders@Cubic3D.co.ke'
    to = invoice.user.email
    subject = "3D print service receipt"
    msg = EmailMessage(subject, html_content, from_email, [to])
    msg.content_subtype = "html"  # Main content is now text/html
    msg.attach_file(receipt_path)
    msg.send()
    invoice.paid = True
    invoice.save()

    cleaned_list = orderlist[1:len(orderlist)-1].split(", ")
    for id in cleaned_list:
        order = PrintRequest.objects.get(pk=int(id))
        order.receipted = True
        order.save()
    return redirect('myadmin')

def completed_orders(request):
    """View Completed orders"""
    assert isinstance(request, HttpRequest)
    class CompletedOrder:
        def __init__(self,printrequest,bill_to):
            self.printrequest = printrequest
            self.bill_to = bill_to

    completed_orders = []
    ungrouped = PrintRequest.objects.filter(grouped=False).filter(receipted=True)
    for item in ungrouped:
        invoice = Invoice.objects.get(number=item.id)
        completed_orders.append(CompletedOrder(item,invoice.bill_to))
    
    grouped = PrintRequest.objects.filter(receipted=True).filter(grouped=True)
    grouprecords = GroupRecord.objects.all()
    for item in grouped:
        found = False;
        for record in grouprecords:
            for id in record.id_list():
                if int(id) == item.id:
                    invoice = Invoice.objects.get(number=int(record.id_list()[0]))
                    completed_orders.append(CompletedOrder(item,invoice.bill_to))
                    found = True;
                    break;
        if found: continue

    return render(request, 'myadmin/completed_orders.html',
        {
            'title':'Completed orders',
            'completed':completed_orders,
            'year': datetime.now().year,
        })    

def user_profiles(request):
    """view your users"""
    assert isinstance(request, HttpRequest)
    users = User.objects.all()
    return render(request, 'myadmin/user_profiles.html' , {
            'title': 'User profiles',
            'users': users,
            'year': datetime.now().year,
        })

def thingiverse(request):
    """select a file from thingyverse and print it"""
    assert isinstance(request,HttpRequest)
    return render(request, 'app/thingiverse.html',
        {
            'title':'A collection of 3D models',
            'year':datetime.now().year,
        }
    )

@login_required
def change_profile(request):
    """allow the user to change their profile data"""
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.mobile = form.cleaned_data.get('mobile')
            user.save()
            return redirect('home')
    else:
        user = User.objects.get(id=request.user.id)
        form_data = {
            'email':user.username,
            'username':user.email,
            'first_name':user.first_name,
            'last_name':user.last_name,
            'mobile':user.profile.mobile,
            }
        form = ProfileForm(initial=form_data)
    return render(request, 'registration/edit_profile.html',
        {
            'form':form,
            'title':'My account',
            'description':'View and/or change your account information. Your privacy is our great concern.',
            'year': datetime.now().year,
        })



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
    return render(request,'registration/signup.html',
        {
            'form': form,
            'title':'SignUp',
            'description':'Create an account with Cubic3D 3D printing service.',
            'year':datetime.now().year,                            
        }
    )




