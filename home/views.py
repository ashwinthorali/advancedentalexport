import json
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import JsonResponse, FileResponse, Http404
from blog.models import *
from enquiry.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from enquiry.forms import STLForm, STLFileForm, LoginForm
from django.contrib import messages
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string, get_template
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
import requests

# from enquiry.models import InstaPost
# Create your views here.
def home(request):
    # data = InstaPost.objects.all().order_by('-id')
    main3 = Blog.objects.filter(main3=True).order_by('-id')[:3]
    data = Testimonials.objects.all().order_by('-id')[:6]
    data2 = Blog.objects.all().order_by('-id')[:3]
    client = Client.objects.all().order_by('-id')
    gallery = Gallery.objects.all().order_by('-id')[:7]
    video      =VideoTestimonals.objects.all().order_by('-id')[:4]
    context = {
        # 'data':data,
        'main3':main3,
        'data':data,
        'data2':data2,
        'client':client,
        'gallery':gallery,
        'video':video,
        
    }
    return render(request, 'index.html', context)

def testimonals(request):
    data = VideoTestimonals.objects.all()
    context = { 
        'data':data,
    }
    return render(request, 'testimonals.html', context)


def contact(request):
    context = {

    }
    return render(request, 'contact.html', context)

def career(request):
    context = {

    }
    return render(request, 'career.html', context)

def stl(request):
            
    if request.method == 'POST':
        
        documents = request.FILES.getlist('files')
        
        nam = request.POST.get('name')
        phone = request.POST.get('contact')
        message = request.POST.get('message')
        name = STLFile.objects.create(name=nam, contact=phone, message=message)

        name.save()
        name = STLFile.objects.all().last()
        
        
        print(documents, '========================')
        
        for f in documents:
            pp = STLFileData.objects.create(stl_data=name, files=f)
            pp.save()

        html_content = render_to_string ('stlmail.html',{ 
            'name':nam, 'phone':phone, 'message':message
        })
        email_from = settings.EMAIL_HOST_USER
        subject = 'New Data In STL Form'
        message = "You have a new data in STL form."
        recipient_list = ['stl@advancedentalexport.com']
        # send_mail( subject, message, email_from, recipient_list, html_message=html_content, fail_silently=False )

        messages.success(request, 'Your STL File Is Uploaded Successfully')
        # return redirect('home:home')  
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))  




    d = STLFileForm()
    context = {
    'd':d
    }
    return render(request, 'stl.html', context)



def file_upload(request):
    if request.method == 'POST':
        my_file=request.FILES.getlist('files')
        print(my_file)
        for f in my_file:
            print('a')

        return HttpResponse('')
    return JsonResponse({'post':'fasle'})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('home:dashboard')
    else:
        if request.method == "POST":
            # your sign in logic goes here
            form = LoginForm(request.POST)
            if form.is_valid():
                username=form.cleaned_data['username']
                password=form.cleaned_data['password']
                #authenticate checks if credentials exists in db
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return redirect('home:dashboard')

                    else:
                        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

                        
                else:
                    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

    context = {
    
    }
    return render(request, 'login.html', context)
    


@login_required(login_url = 'home:user_login')
def dashboard(request):
    if request.user.is_staff:
        data = STLFile.objects.all().order_by('-id')
        context = {
            'data':data,
        }
        return render(request, 'dashboard.html', context)
    else:
        return redirect('home:home')

def singUser(request):
    context = {

    }
    return render(request, 'singup.html', context)


def eventgallery(request, pk):
    
    data1 =  EventsGallery.objects.filter(category__slug=pk).order_by('-id')
    cat = Events.objects.get(slug=pk)
    page = request.GET.get('page', 1)
    paginator = Paginator(data1, 12)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    context = {
        'data':data,
        'cat':cat,
    }
    return render(request, 'eventgallery.html', context)

def about(request):
    team = Team.objects.all()
    imagez = AboutImage.objects.all()
    context = {
        'team':team,
        'imagez':imagez,
    }
    return render(request, 'about.html', context)



def sitemap(request):
    return render(request, 'sitemap.xml', content_type='text/xml')

#end
def robots(request):
    return render(request, 'robot.txt', content_type='text')




def categories(request):
    data1 =  Category.objects.all().order_by('-id')
    page = request.GET.get('page', 1)

    
    paginator = Paginator(data1, 12)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    context = {
        'data':data,
    }
    return render(request, 'categories.html', context)


def categoriesd(request, pk):
    data3 =  Category.objects.get(slug=pk)
    data1 =  Blog.objects.filter(category=data3).order_by('-id')
    data2 =  Blog.objects.filter(most_visited=True).order_by('-id')[:4]
    page = request.GET.get('page', 1)


    
    paginator = Paginator(data1, 12)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    context = {
        'data':data,
        'data3':data3,
        'data2':data2,
    }
    return render(request, 'categories_blog.html', context)

def blogd(request, pk):
    data =  Blog.objects.get(slug=pk)
    data2 =  Blog.objects.all().order_by('-id')[:2]
    for ie in data.category.all():
        cat = ie.category
        print(cat)
    data3 =  Category.objects.get(category=cat)
    context = {
        'data':data,
        'data2':data2,
        'data3':data3,
    
    }
    return render(request, 'blogd.html', context)

def blogs(request):
    return redirect('blog:blog')

def gallery(request):
    data1 =  Gallery.objects.all().order_by('-id')
    data2 =  Blog.objects.filter(most_visited=True).order_by('-id')[:4]
    page = request.GET.get('page', 1)


    
    paginator = Paginator(data1, 12)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    context = {
        'data':data,
        'data2':data2,
    }
    return render(request, 'gallery.html', context)



def search(request):
    if request.method == 'GET':
        q = request.GET.get('q')
        data1 =  Blog.objects.filter(Q(h1__contains=q)| Q(content__contains=q)).order_by('-id')
        data2 =  Blog.objects.filter(most_visited=True).order_by('-id')[:4]
        page = request.GET.get('page', 1)


        
        paginator = Paginator(data1, 12)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        if data:
            pass
        else:
            data =  Blog.objects.all().order_by('-id')      
        context = {
            'data':data,
            'data1':data1,
            'data2':data2,
        }

    return render(request, 'all_blog.html', context)


def faq(request):
    
    
    context = {
    }
    return render(request, 'faq.html', context)


def privacy(request):
    context = {

    }
    return render(request, 'privacy.html', context)


def cookie(request):
    context = {

    }
    return render(request, 'cookie.html', context)

def gp(request):
    context = {

    }
    return render(request, 'guest.html', context)


def checkup(request):
    if request.method =='GET':
        name = request.GET.get('name')
        name =str(name)
        data = User.objects.filter(username=name).count()
        if data > 0:
            test = 0
        else:
            test = 1    
        
        context = {
            'test':test
        }
    return JsonResponse({'test':test})


def api_user_login(request):
    if request.method == "POST":
        # your sign in logic goes here
        form = LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            #authenticate checks if credentials exists in db
            print(username, password)
            apiurl = 'https://adesurat.com/API.php?call=login'
            apiurl = str(apiurl)
            data = {
                "username": username,
                "password": password
            }
            
            print(apiurl)
            res = requests.post(apiurl, data=data)
            dict_data = res.json()
            login_success = (dict_data['status'])
            login_success = str(login_success)
            if login_success == "True":
                token = (dict_data['token'])
                token = str(token)
                
                print(dict_data['user'])
                user = dict_data['user']
                ids = user['userid']
                ids = str(ids)
                
                pk = token
                fk = ids
                #order
                order_apiurl = 'https://adesurat.com/API.php?call=order_list_get_dr'
                order_apiurl = str(order_apiurl)

                headers = { 
                            'Accept-Language' : 'content-copied-from-myhttpheader',
                            'User-Agent':'content-copied-from-myhttpheader',
                            'Token': pk
                        }

                data = {
                    "ids": fk
                }


                
                res = requests.post(order_apiurl, headers=headers, data=data)
                dict_data = res.json()
                order_data = (dict_data['data'])
                order_key = []
                for i in order_data:
                    for key in i:
                        order_key.append(key)
                    break    

                
                #invoice
                payment_apiurl = 'https://adesurat.com/API.php?call=paymentloadData'
                payment_apiurl = str(payment_apiurl)
                res = requests.post(payment_apiurl, headers=headers, data=data)
                dict_data = res.json()
                
                payment_data = (dict_data['data'])
                
                payment_key = []
                for i in payment_data:
                    for key in i:
                        payment_key.append(key)
                    break    


                #invoice
                invoice_apiurl = 'https://adesurat.com/API.php?call=invoiceloadData'
                invoice_apiurl = str(invoice_apiurl)
                res = requests.post(invoice_apiurl, headers=headers, data=data)
                dict_data = res.json()
                
                invoice_data = (dict_data['data'])
                
                invoice_key = []
                for i in invoice_data:
                    for key in i:
                        invoice_key.append(key)
                    break    

                #statement
                statement_apiurl = 'https://adesurat.com/API.php?call=statementData'
                statement_apiurl = str(statement_apiurl)
                res = requests.post(statement_apiurl, headers=headers, data=data)
                dict_data = res.json()
                
                statement_data = (dict_data['data'])
                print(statement_data)
                statement_key = []
                for i in statement_data:
                    for key in i:
                        statement_key.append(key)
                    break    
            
                stb = dict_data['TotalBalance']

                context = {
                    'order_data':order_data,
                    'order_key':order_key,
                    'payment_data':payment_data,
                    'payment_key':payment_key,
                    'invoice_data':invoice_data,
                    'invoice_key':invoice_key,
                    'statement_data':statement_data,
                    'statement_key':statement_key,
                    'pk':pk,
                    'did':fk,
                    'user':user,
                    'stb':stb,
                }
                return render(request, 'ext_api.html', context)

                # return redirect('home:ext_api',  pk=token, fk=ids)
            else:
                messages.error(request, 'Login Failed!')
                return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

            # user = authenticate(username=username, password=password)
            # if user is not None:
            #     if user.is_active:
            #         login(request, user)
            #         return redirect('home:dashboard')

            #     else:
            #         return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

                    
            # else:
            #     return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        
    context = {
    
    }
    return render(request, 'api_login.html', context)
    


def ext_api(request, pk, fk):
    
    #order
    order_apiurl = 'https://adesurat.com/API.php?call=order_list_get_dr'
    order_apiurl = str(order_apiurl)

    headers = { 
                'Accept-Language' : 'content-copied-from-myhttpheader',
                'User-Agent':'content-copied-from-myhttpheader',
                'Token': pk
            }

    data = {
        "ids": fk
    }


    
    res = requests.post(order_apiurl, headers=headers, data=data)
    dict_data = res.json()
    order_data = (dict_data['data'])
    order_key = []
    for i in order_data:
        for key in i:
            order_key.append(key)
        break    

    
    #invoice
    payment_apiurl = 'https://adesurat.com/API.php?call=paymentloadData'
    payment_apiurl = str(payment_apiurl)
    res = requests.post(payment_apiurl, headers=headers, data=data)
    dict_data = res.json()
    
    payment_data = (dict_data['data'])
    
    payment_key = []
    for i in payment_data:
        for key in i:
            payment_key.append(key)
        break    


    #invoice
    invoice_apiurl = 'https://adesurat.com/API.php?call=invoiceloadData'
    invoice_apiurl = str(invoice_apiurl)
    res = requests.post(invoice_apiurl, headers=headers, data=data)
    dict_data = res.json()
    
    invoice_data = (dict_data['data'])
    
    invoice_key = []
    for i in invoice_data:
        for key in i:
            invoice_key.append(key)
        break    

    #statement
    statement_apiurl = 'https://adesurat.com/API.php?call=statementData'
    statement_apiurl = str(statement_apiurl)
    res = requests.post(statement_apiurl, headers=headers, data=data)
    dict_data = res.json()
    
    statement_data = (dict_data['data'])
    print(statement_data)
    statement_key = []
    for i in statement_data:
        for key in i:
            statement_key.append(key)
        break    
    
    stb = dict_data['TotalBalance']
    

    context = {
        'order_data':order_data,
        'order_key':order_key,
        'payment_data':payment_data,
        'payment_key':payment_key,
        'invoice_data':invoice_data,
        'invoice_key':invoice_key,
        'statement_data':statement_data,
        'statement_key':statement_key,
        'pk':pk,
        'did':fk,
        'stb':stb,
    }
    return render(request, 'ext_api.html', context)


def api_logout(request, pk, did):
    order_apiurl = 'https://adesurat.com/API.php?call=logout'
    order_apiurl = str(order_apiurl)
    headers = { 
                'Accept-Language' : 'content-copied-from-myhttpheader',
                'User-Agent':'content-copied-from-myhttpheader',
                'Token': pk
            }

    data = {
        "did": did
    }
    return redirect('home:home')


def print_order(request):
    if request.method == 'GET':
        #order
        fk = request.GET.get('token')
        order_no = request.GET.get('orderNo')
        order_apiurl = 'https://adesurat.com/API.php?call=orderprint'
        order_apiurl = str(order_apiurl)
       
        headers = { 
                    'Accept-Language' : 'content-copied-from-myhttpheader',
                    'User-Agent':'content-copied-from-myhttpheader',
                    'Token': fk
                }

        data = {
            "order_no": order_no
        }
    
        res = requests.post(order_apiurl, headers=headers, data=data)
        dict_data = res.json()
        
        link= str(dict_data['pdf_link'])
        context ={
            'link':link
        }
        return render(request, 'pdfview.html', context)
        # return redirect('home:home')

def print_payment(request):
    if request.method=='GET':
        doctor_id = request.GET.get('doctor_id')
        if doctor_id:
            pass
        else:
            doctor_id = ""    

        receipt_no = request.GET.get('receipt_no')
        if receipt_no:
            pass
        else:
            receipt_no = ""    
        
        amount = request.GET.get('amount')
        if amount:
            pass
        else:
            amount = ""   
        
        payment_mode = request.GET.get('payment_mode')
        if payment_mode:
            pass
        else:
            payment_mode = ""   
        
        
        chq_no = request.GET.get('chq_no')
        if chq_no:
            pass
        else:
            chq_no = "" 

        date = request.GET.get('date')
        if date:
            pass
        else:
            date = "" 

        fk = request.GET.get('token')
        if fk:
            pass
        else:
            fk = "" 
        print(fk)

        #order
        apiurl = 'https://adesurat.com/API.php?call=printpayment'
        apiurl = str(apiurl)
        
        headers = { 
                    'Accept-Language' : 'content-copied-from-myhttpheader',
                    'User-Agent':'content-copied-from-myhttpheader',
                    'Token': fk
                }

        data = {
            "doctor_id": doctor_id,
            "receipt_no":receipt_no,
            "amount":amount,
            "payment_mode":payment_mode,
            "chq_no":chq_no,
            'date':date
            
        }
        print(data)
        res = requests.post(apiurl, headers=headers, data=data)
        dict_data = res.json()
        print(dict_data)
        link= str(dict_data['pdf_link'])
        context ={
            'link':link
        }
        return render(request, 'pdfview.html', context)
    
    # return redirect('home:home')

def print_statment(request, pk, did):
    #order
    apiurl = 'https://adesurat.com/API.php?call=printstatement'
    apiurl = str(apiurl)
    
    headers = { 
                'Accept-Language' : 'content-copied-from-myhttpheader',
                'User-Agent':'content-copied-from-myhttpheader',
                'Token': pk
            }

    data = {
        "doctor_id": did,
        
        
    }
    res = requests.post(apiurl, headers=headers, data=data)
    dict_data = res.json()
    
    link= str(dict_data['pdf_link'])
    context ={
        'link':link
    }
    return render(request, 'pdfview.html', context)
    
    # return redirect('home:home')

def print_invoice(request, pk, did):
    #order
    apiurl = 'https://adesurat.com/API.php?call=printinvoice'
    apiurl = str(apiurl)
    
    headers = { 
                'Accept-Language' : 'content-copied-from-myhttpheader',
                'User-Agent':'content-copied-from-myhttpheader',
                'Token': pk
            }

    data = {
        "invoice_ids": did,
        
        
    }
    res = requests.post(apiurl, headers=headers, data=data)
    dict_data = res.json()
    
    link= str(dict_data['pdf_link'])
    context ={
        'link':link
    }
    return render(request, 'pdfview.html', context)
    
    # return redirect('home:home')


