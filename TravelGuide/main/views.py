import io

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from events.models import Event
from django.shortcuts import render, redirect
from . import forms
from .models import userProfile, HotelReview, RoomModel, HotelReservation, chat, Contact, chatForumMessages,wishlist

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader

from django.core.mail import send_mail
from . import forms


def index(request):
    events_list=Event.objects.all().exclude(date=None)
    upcoming=Event.objects.filter(date=None).all()
    return render(request,'main/index.html',{'events_list': events_list, 'upcoming': upcoming})
# Create your views here.

@login_required(login_url="/accounts/login/")
def UserProfile(request):
    primaryKey = request.POST.get('primaryKey')
    if primaryKey is None:
        primaryKey = 3
    instance = userProfile.objects.get(id=primaryKey)
    UserProfile.user_name = request.POST.get('user_name')
    UserProfile.phone = request.POST.get('phone_number')
    UserProfile.address = request.POST.get('address')
    UserProfile.bio = request.POST.get('bio')
    UserProfile.image = request.FILES.get('image')

    if UserProfile.user_name is not None and UserProfile.user_name != '':
        instance.user_name = UserProfile.user_name

    if UserProfile.phone is not None and UserProfile.phone != '':
        instance.user_phone = UserProfile.phone

    if UserProfile.address is not None and UserProfile.address != '':
        instance.user_address = UserProfile.address

    if UserProfile.bio is not None and UserProfile.bio!= '':
        instance.bio = UserProfile.bio

    if UserProfile.image is not None:
        instance.user_image = UserProfile.image
    instance.save()

    profile = userProfile.objects.all()
    profile2 = userProfile.objects.filter(user=request.user).first()
    b = ''
    if profile2 is None:
        b = 'NoData'

    context = {}
    context['profile'] = profile
    context['booli'] = b
    context['name'] = UserProfile.user_name
    context['phone'] = UserProfile.phone
    context['address'] = UserProfile.address
    context['bio'] = UserProfile.bio
    context['image'] = UserProfile.image

    userBookedHotels = HotelReservation.objects.filter(user=request.user)
    context['userBookedHotels'] = userBookedHotels

    reservation = HotelReservation.objects.filter(user=request.user)
    count = 0
    for i in reservation:
        count += 1

    context['offer'] = '0'
    if 3 <= count < 5:
        context['offer'] = '30'
    elif 5 <= count < 10:
        context['offer'] = '40'
    elif count >= 10:
        context['offer'] = '50'

    return render(request, 'main/user_profile.html', context)


@login_required(login_url="/accounts/login/")
def createProfile(request):
    form = forms.UserProfile()
    if request.method == 'POST':
        form = forms.UserProfile(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
    else:
        form = forms.UserProfile()
    return render(request, 'main/createprofile.html', {'form': form})

def about(request):
    return render(request, 'main/about.html')

@login_required(login_url="/account/login/")
def RoomShow(request):
    hotelReview = HotelReview.objects.all().order_by('date')
    roomModel = RoomModel.objects.all().order_by('slug')
    profile = userProfile.objects.all()
    context = {}
    hotel_name = request.POST.get('hotel-name')
    context['hotel_name'] = hotel_name
    context['roomModel'] = roomModel
    context['profile'] = profile

    context['hotelReview'] = hotelReview

    hotel = hotel_name.split('_')
    mylist = ' '.join(hotel)
    context['mylist'] = mylist

    return render(request, 'main/HotelRoom.html', context)

@login_required(login_url="/account/login/")
def hotel_page(request):
    return render(request, 'main/HotelPage.html')

@login_required(login_url="/account/login/")
def hotelReview(request):
    form = forms.HotelReview()
    if request.method == 'POST':
        form = forms.HotelReview(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
    else:
        form = forms.HotelReview()
    return render(request, 'main/HotelReview.html', {'form': form})


@login_required(login_url="/account/login/")
def deleteHotelReview(request, pk):
    instance = HotelReview.objects.get(id=pk)
    instance.delete()
    return redirect('main:hotel_page')

@login_required(login_url="/account/login/")
def hotel_bookingPdf(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)
    #logo = ImageReader('https://i.ibb.co/MPcBtHf/logo1.jpg')

    name = reservationnew.user_name
    mail = reservationnew.user_email
    phone = reservationnew.user_phone
    checkin = reservationnew.checkin_date
    checkout = reservationnew.checkout_date
    hotel_name = reservationnew.hotel_name
    room_number = reservationnew.room_numbers
    room_type = reservationnew.room_type

    hotel_reservation_instance = HotelReservation.objects.create(user_name=name, user_email=mail, user_phone=phone,
                                                                 checkin_date=checkin, checkout_date=checkout,
                                                                 hotelName=hotel_name, room_number=room_number,
                                                                 room_type=room_type, user=request.user)
    hotel_reservation_instance.save()

    lines = [
        " ",
        " ",
        " ",
        " ",
        " ",
        " ",

        "                                     Welcome to Travel Guide",
        " ",
        "                           Your Reservation confirmation is below",
        " ",
        " ",
        " ",
        "        Full name: " + name,
        " ",
        "        Email: " + mail,
        " ",
        "        Phone: " + phone,
        " ",
        "        Check-in date: " + checkin,
        " ",
        "        Check-out date: " + checkout,
        " ",
        "        Hotel name: " + hotel_name,
        " ",
        "        Total number of rooms: " + room_number,
        " ",
        "        Room type: " + room_type,
        " ",
        " ",
        "",
        "                               Thank you for visiting Travel Guide",
        "",
        "                              All right reserved by Travel Guide team",

    ]

    for line in lines:
        textob.textLine(line)

    #c.drawImage(logo, 170, 10, mask='auto', anchor='c')
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='room.pdf')

@login_required(login_url="/account/login/")
def reservationnew(request):
    reservationnew.user_name = request.POST.get('user-name')
    print(reservationnew.user_name)
    reservationnew.user_email = request.POST.get('user-email')
    reservationnew.user_phone = request.POST.get('user-phone')
    reservationnew.checkin_date = request.POST.get('checkin-date')
    reservationnew.checkout_date = request.POST.get('checkout-date')
    reservationnew.hotel_name = request.POST.get('hotel-name')
    reservationnew.room_numbers = request.POST.get('room-numbers')
    reservationnew.room_type = request.POST.get('room-type')

    return render(request, 'main/hotel_booking.html',
                  {'user_name': reservationnew.user_name, 'user_email': reservationnew.user_email,
                   'user_phone': reservationnew.user_phone, 'checkin_date': reservationnew.checkin_date,
                   'checkout_date': reservationnew.checkout_date, 'hotel_name': reservationnew.hotel_name,
                   'room_numbers': reservationnew.room_numbers, 'room_type': reservationnew.room_type})

@login_required(login_url="/account/login/")
def hotelsearch(request):
    if request.method == 'POST':
        search = request.POST['hotel-search']
        search1 = search.split(' ')
        search2 = ('_').join(search1)
        context = {}
        context['hotelsearch'] = search
        roomModel = RoomModel.objects.filter(slug__icontains=search2)
        context['roomModel'] = roomModel
    return render(request, 'main/hotelsearch.html', context)

@login_required(login_url="/account/login/")
def directmessage(request):
    userName = userProfile.objects.all()
    Chat = chat.objects.all().order_by('-date')
    context = {}
    context['chat'] = Chat
    context['userName'] = userName
    return render(request, 'main/directMessage.html', context)


@login_required(login_url="/account/login/")
def sentmessage(request):
    form = forms.chatForm()
    if request.method == 'POST':
        form = forms.chatForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.from_user = request.user
            instance.save()
            url = reverse('main:direct_message')
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(url)
    else:
        form = forms.chatForm()
    return render(request, 'main/messageSend.html', {'form': form})

@login_required(login_url="/account/login/")
def chatForum(request):
    form = forms.chatForumForm()
    if request.method == 'POST':
        form = forms.chatForumForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.message_user = request.user
            instance.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = forms.chatForumForm()

    forum = chatForumMessages.objects.all().order_by('-date')
    context = {}
    context['forum'] = forum
    context['form'] = form
    return render(request, 'main/chatForum.html', context)

@login_required(login_url="/account/login/")
def wishList(request):
    form = forms.wishlistForm()
    if request.method == 'POST':
        form = forms.wishlistForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            url = reverse('main:user_profile')
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(url)
    else:
        form = forms.wishlistForm()

    WishList = wishlist.objects.all().order_by('-date')
    context = {}
    context['WishList'] = WishList
    context['form'] = form
    return render(request, 'main/wishlist.html', context)

@login_required(login_url="/account/login/")
def deletewishlist(request, pk):
    instance = wishlist.objects.get(id=pk)
    instance.delete()
    return redirect('main:wishlist')


@login_required(login_url="/account/login/")
def usersearch(request):
    return render(request, 'main/usersearch.html')

@login_required(login_url="/account/login/")
def searcheduser(request):
    if request.method == 'POST':
        search = request.POST['user-search']
        context = {}
        context['usersearch'] = search
        userprofile = userProfile.objects.filter(user_name__icontains=search)
        context['userprofile'] = userprofile
    return render(request, 'main/searcheduser.html', context)


@login_required(login_url="/account/login/")
def searchedUserProfile(request, pk):
    if pk is None:
        profile = userProfile.objects.filter(id=1)
    else:
        profile = userProfile.objects.filter(id=pk)
    context = {}
    context['profile'] = profile
    return render(request, 'main/searchedUserProfile.html', context)

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        contact = request.POST['contact']
        message = request.POST['message']
        data_dict = {
            'name': name,
            'email': email,
            'contact': contact,
            'message': message,
        }
        Contact.objects.create(**data_dict)
        # messages.success(request, 'Message has been sent successfully ')
        return HttpResponseRedirect(reverse('main:contact'))
    return render(request, 'main/contact.html')