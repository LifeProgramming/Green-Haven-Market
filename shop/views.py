from django.db.models.query import QuerySet
from django.shortcuts import render, HttpResponse
from django.http import HttpResponseForbidden
from django.views.generic import ListView, DetailView, DeleteView, FormView, CreateView, UpdateView
from .models import Items
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from .forms import addItem
from django.contrib.auth.decorators import login_required

class itemsList(ListView):
    model= Items
    template_name='shop/items_list'

    def get_queryset(self):
         queryset = super().get_queryset()
         query = self.request.GET.get('query')
         if query:
             queryset = queryset.filter(name__icontains=query)
         return queryset

class itemDetail(DetailView):
    model=Items
    context_object_name='item'

class LoginUserView(FormView):
    form_class = AuthenticationForm
    template_name = 'shop/login.html' 

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.info(self.request, "This user does not exist!")
        return super().form_invalid(form)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponse('Sorry! You have already logged in!')
        return super().get(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('items')

def logoutUser(request):
    logout(request)
    return redirect('items')

class RegisterUserView(CreateView):
    form_class = UserCreationForm
    template_name = 'shop/auth.html'  
    success_url = reverse_lazy('items')  

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

    def form_invalid(self, form):
        messages.info(self.request, "Sorry! Something went wrong!!!")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        kwargs['form'] = self.form_class()
        return super().get_context_data(**kwargs)

class addedItems(LoginRequiredMixin,ListView):
    model=Items
    template_name='shop/addedItems.html'
    context_object_name='addedItems'

    def get_queryset(self):
        user=self.request.user
        return Items.objects.filter(created_by=user)

class itemForm(LoginRequiredMixin,CreateView):
    form_class=addItem
    template_name='shop/itemForm.html'
    success_url=reverse_lazy('added-items')

    def form_valid(self, form):
        form.instance.created_by=self.request.user
        response = super().form_valid(form)
        return response

    def form_invalid(self, form):
        messages.info(self.request, "Sorry! Something went wrong!!!")
        return super().form_invalid(form)

@login_required(login_url='login')
def updateItem(request, pk):
    item= Items.objects.get(id=pk)
    form=addItem(request.POST or None, request.FILES or None, instance=item)
    user=request.user
    if item.created_by!=user:
        return HttpResponseForbidden('Sorry! You are not allowed to change this job!')
    if request.method=='POST':
        form=addItem(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('added-items')
        
    return render(request,'shop/itemForm.html',{'form':form})

@login_required(login_url='login')   
def deleteItem(request, pk):
    item=Items.objects.get(id=pk)
    item.delete()
    return redirect('added-items')