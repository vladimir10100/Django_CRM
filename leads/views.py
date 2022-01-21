from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse

from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin

from agents.mixins import OrganizerAndLoginRequiredMixin
from .models import Lead, Agent, User
from .forms import Lead_Form, Lead_Edit_Form, CustomUser

class SignUpView(CreateView):
    template_name = 'registration/signup.html'
    form_class = CustomUser

    def get_success_url(self):
        return reverse('leads:login_view')



class Home(LoginRequiredMixin, ListView):
    template_name = 'leads/home.html'
    context_object_name = 'leads'

    def get_queryset(self):
        user = self.request.user 
        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.userprofile)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            # Filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)

        return queryset



class LandingPageView(TemplateView):
    template_name = 'leads/landingpage.html'


class LeadListView(LoginRequiredMixin, ListView):
    template_name = 'leads/retrieve.html'
    context_object_name = 'lead'


    def get_queryset(self):
        user = self.request.user 
        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.userprofile)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            # Filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)

        return queryset
    

class LeadDetailView(OrganizerAndLoginRequiredMixin, DetailView):
    template_name = 'leads/detail.html'
    queryset = Lead.objects.all()
    context_object_name = 'lead'

class LeadCreateView(OrganizerAndLoginRequiredMixin, CreateView):
    template_name = 'leads/create.html'
    form_class = Lead_Form
    
    def get_success_url(self):
        return reverse("leads:home")

    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.organization = self.request.user.userprofile
        lead.save()
        # Send an E-mail
        send_mail(
            subject = "A lead has been created.",
            message = "Go to the site to see the new lead.",
            from_email = "admin@admin.com",
            recipient_list = ['test@test.com']
        )
        return super(LeadCreateView, self).form_valid(form)


class LeadUpdateView(OrganizerAndLoginRequiredMixin, UpdateView):
    template_name = 'leads/edit.html'
    form_class = Lead_Edit_Form

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organization=user.userprofile)
    
    def get_success_url(self):
        return reverse("leads:home")

class LeadDeleteView(OrganizerAndLoginRequiredMixin, DeleteView):
    template_name = 'leads/delete.html'
    context_object_name = 'lead'

    def get_success_url(self):
        return reverse("leads:home")

    def get_queryset(self):
        user = self.request.user 
        return Lead.objects.filter(organization=user.userprofile)


# def home(request):
#     lead = Lead.objects.all()
#     context = {'leads':lead}
#     return render(request, 'leads/home.html', context)

# def retrieve(request):
#     lead = Lead.objects.all() 
#     context = {
#         'lead': lead,
#     }
#     return render(request, 'leads/retrieve.html', context)

# def detail(request, pk):
#     x = Lead.objects.get(id=pk)
#     print(x)
#     context = {'lead': x}
#     return render(request, 'leads/detail.html', context)


# def create(request):
#     form = Lead_Form()
#     context = {'form':form}
#     if request.method == 'POST':
#         form = Lead_Form(request.POST)
#         if form.is_valid():
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
#             agent = form.cleaned_data['agent']
#             agent = User.objects.get(username=agent)
#             print(agent)
#             agent = form.cleaned_data['agent']
#             Lead.objects.create(first_name=first_name, last_name=last_name,
#                                 age=age, agent=agent)
#             print('Successfully created')
#     return render(request, 'leads/create.html', context)


# def edit(request, pk):
#     lead = Lead.objects.get(id=pk)
#     form = Lead_Edit_Form()
#     context = {'form':form}
#     if request.method == 'POST':
#         form = Lead_Edit_Form(request.POST)
#         if form.is_valid():
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
#             lead.first_name = first_name
#             lead.last_name = last_name
#             lead.age = age 
#             lead.save()
#             return retrieve(request)

#     return render(request, 'leads/edit.html', context)



