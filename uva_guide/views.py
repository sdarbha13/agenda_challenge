from django.urls import reverse
from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
import datetime
from django.utils.safestring import mark_safe

from .models import *
from .utils import Calendar

from .forms import orgCreationForm, EventForm, ProfileForm

class IndexView(generic.TemplateView):
    template_name = 'uva_guide/index.html'




class CalendarView(generic.ListView):
    model = Event
    template_name = 'uva_guide/cal.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # use today's date
        # d = get_date(self.request.GET.get('day', None))
        d = get_date(self.request.GET.get('month', None))
        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)

        # next and prev months

        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return datetime.date(year, month, day=1)
    return datetime.date.today()


def prev_month(d):
    first = d.replace(day=1)
    p_month = first - datetime.timedelta(days=1)
    month = 'month=' + str(p_month.year) + '-' + str(p_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    n_month = last + datetime.timedelta(days=1)
    month = 'month=' + str(n_month.year) + '-' + str(n_month.month)
    return month


def event(request, event_id=None):
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()

    form = EventForm(request.POST or None, instance=instance)

    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('uva_guide:cal'))
    return render(request, 'uva_guide/event.html', {'form': form, 'mapurl': instance.get_maps_url()})


def cale(request, year, month):
    name = "Kev"
    month = month.title()
    # convert month from name to number
    month_number = int(list(calendar.month_name).index(month))

    # the actual calendar
    cal = HTMLCalendar().formatmonth(year, month_number)

    return render(
        request,
        "uva_guide/cale.html",
        {"name": name,
         "year": year,
         "month": month,
         "month_number": month_number,
         "cal": cal,

         })
    # model = schedule
    # template_name = 'uva_guide/schedule'


def sched(request):
    return HttpResponse('hello')
# Create your views here.
def orgCreation(request):
    if request.method == "POST":
        form = orgCreationForm(request.POST)
        form.save()
    else:
        form = orgCreationForm()
    return render(request, "index.html", {"form": form })   #Change index.html to go to whatever club they created


def login_user(request):
    if not request.user.profile.firstTime:
        return HttpResponseRedirect('/')
    else:
        return get_profile_setup(request)


def get_profile_setup(request):
    # if this is a POST request we need to process the form data

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ProfileForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            request.user.profile.type = form.data['type']
            request.user.profile.firstTime = False
            request.user.profile.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ProfileForm()

    return render(request, 'uva_guide/profile_setup.html', {'form': form})