from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from xhtml2pdf import pisa

from .models import Schedule,Book
# Create your views here.

def ticket_pdf(request, slug=None):
    template_path = 'ticket_pdf.html'
    user = request.user
    bus = Schedule.objects.get(slug=slug)
    name = user.first_name + user.last_name
    book = Book.objects.filter(booker=user, bus=bus)
    for book1 in book:
        passenger1= book1.passenger
        fair1 = book1.fair
    members = passenger1
    fair = fair1
    print(members)
    print(fair)
    context = {'bus':bus,'name':name,'book':book,'members':members,'fair':fair}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="token.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def view_bus(request,slug=None):
    #huhijkhlhlhhlhj
    bus=Schedule.objects.get(slug=slug)
    booked=Book.objects.filter(booker=request.user,bus=bus).exists()
    if request.method == "POST":
        passenger = request.POST['passenger']
        fair=float(passenger)*bus.fair
        Book.objects.create(bus=bus,booker=request.user,passenger=passenger,fair=fair,date=bus.date)
    return render(request,'book_bus.html',{'bus':bus,'booked':booked})


def bus_search(request):
    if request.method == "POST":
        date = request.POST["dept"]
        buses = Schedule.objects.filter(date=date)
        return render(request, 'bus_search.html', {'buses': buses})
    else:
        buses = Schedule.objects.all()
        return render(request,'bus_search.html',{'buses':buses})