from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from .models import Poll, Choice, Vote
from .forms import PollForm, ChoiceFormSet

class PollListView(ListView):
    model = Poll
    template_name = 'polls/poll_list.html'
    context_object_name = 'polls'
    
    def get_queryset(self):
        return Poll.objects.filter(active=True)

@login_required
def create_poll(request):
    if not request.user.is_staff:
        messages.error(request, "Only staff can create polls.")
        return redirect('polls:poll_list')
    
    if request.method == 'POST':
        form = PollForm(request.POST)
        formset = ChoiceFormSet(request.POST, instance=Poll())
        
        if form.is_valid() and formset.is_valid():
            poll = form.save(commit=False)
            poll.created_by = request.user
            poll.save()
            formset.instance = poll
            formset.save()
            messages.success(request, "Poll created successfully!")
            return redirect('polls:poll_list')
    else:
        form = PollForm()
        formset = ChoiceFormSet(instance=Poll())
    
    return render(request, 'polls/create_poll.html', {
        'form': form,
        'formset': formset,
    })

@login_required
def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    user_vote = None
    
    if request.user.is_authenticated:
        try:
            user_vote = Vote.objects.get(user=request.user, poll=poll)
        except Vote.DoesNotExist:
            pass
    
    return render(request, 'polls/poll_detail.html', {
        'poll': poll,
        'user_vote': user_vote,
    })

@login_required
def vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    
    if not poll.active:
        messages.error(request, "This poll is not active.")
        return redirect('polls:poll_list')
    
    try:
        selected_choice = poll.choices.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        messages.error(request, "You didn't select a choice.")
        return redirect('polls:poll_detail', poll_id=poll.id)
    
    if Vote.objects.filter(user=request.user, poll=poll).exists():
        messages.error(request, "You have already voted in this poll.")
        return redirect('polls:poll_detail', poll_id=poll.id)
    
    Vote.objects.create(
        user=request.user,
        choice=selected_choice,
        poll=poll
    )
    messages.success(request, "Your vote has been recorded!")
    return redirect('polls:poll_detail', poll_id=poll.id)

@login_required
def poll_results(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    
    if not poll.show_results:
        messages.error(request, "Results for this poll are not available.")
        return redirect('polls:poll_list')
    
    return render(request, 'polls/poll_results.html', {
        'poll': poll,
    })