from django.shortcuts import render,redirect
from shop.models import Items
from .models import Conversation, ConversationMessage
from .forms import ConversationMessageForm
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def newCoversation(request, item_pk):
    item=Items.objects.get(id=item_pk)
    if item.created_by==request.user:
        return redirect('added-items')
    conversation=Conversation.objects.filter(item=item).filter(members__in=[request.user.id])
    if conversation:
        return redirect('messaging:detail',pk=conversation.first().id)
    form=ConversationMessageForm()
    if request.method=='POST':
        form=ConversationMessageForm(request.POST)
        if form.is_valid():
            conversation=Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            conversation.save()

            conversation_message=form.save(commit=False)
            conversation_message.conversation=conversation
            conversation_message.created_by=request.user
            conversation_message.save()
            return redirect('added-items')
        else:
            form=ConversationMessageForm()
    return render(request,'messaging/new.html',{'form':form})

@login_required(login_url='login')
def inbox(request):
    conversations=Conversation.objects.filter(members__in=[request.user.id])
    return render(request,'messaging/inbox.html',{'messages':conversations})

@login_required(login_url='login')
def detail(request, pk):
    conversation=Conversation.objects.filter(members__in=[request.user.id]).get(id=pk)
    form=ConversationMessageForm()
    if request.method=="POST":
        form=ConversationMessageForm(request.POST or None)
        if form.is_valid():
            message=form.save(commit=False)
            message.conversation=conversation
            message.created_by=request.user
            message.save()
            conversation.save()
            return redirect('messaging:detail', pk=pk)
        else:
            form=ConversationMessageForm()
    return render(request,'messaging/conversation.html',{
        'conversation':conversation,
        'form':form,
})
