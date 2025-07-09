from django.db.models import Avg
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Event, Enrollment, Review

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

events_list = Event.objects.all()


def ticket_pdf(request, slug=None):
    template_path = 'ticket_pdf.html'
    user = request.user
    event = Event.objects.get(slug=slug)
    name = user.first_name + user.last_name
    enrollment = Enrollment.objects.get(traveller=user, event=event)
    members = enrollment.adult+enrollment.child
    payment = event.price*members-enrollment.get_discount
    context = {'enrollment': enrollment,'members': members, 'event': event,'name': name, 'payment': payment}
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


def all_events(request):
    return render(request, 'events.html', {'events_list': events_list})


def enroll(request, event, slug):
    traveller = request.user
    mobile = '10165658599'
    Enrollment.objects.create(event=event, traveller=traveller, mobile=mobile)


def event_detail(request, slug=None):
    event = Event.objects.get(slug=slug)
    review = Review.objects.filter(event=event).count()
    rating = Review.objects.filter(event=event).aggregate(Avg('star'))
    if not request.user.is_authenticated:
        if request.method == 'POST':
            return redirect('/accounts/login/')
        if slug is not None:
            return render(request, 'event_single.html', {'event': event, 'slug': slug, 'event': event, 'review': review, 'rating': rating['star__avg'],'enrolled': False, 'events_list': events_list})
    else:
        enrolled = Enrollment.objects.filter(traveller=request.user, event=event).exists()
        if slug is not None:
            if request.method == 'POST':
                if enrolled:
                    return redirect('/events/'+slug)
                enroll(request, event, slug)
                return redirect('/events/' + slug)
            return render(request, 'event_single.html', {'event': event, 'slug': slug, 'event': event, 'review': review, 'rating': rating['star__avg'], 'enrolled': enrolled, 'events_list': events_list})