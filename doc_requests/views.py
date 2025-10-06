from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import DocumentRequest, DocumentSubmission
from .forms import RequestDocumentForm, SubmitDocumentForm

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('user_requests')
    
    if request.method == 'POST':
        form = RequestDocumentForm(request.POST)
        if form.is_valid():
            request_obj = form.save(commit=False)
            request_obj.admin = request.user
            request_obj.save()
            return redirect('dashboard')
    else:
        form = RequestDocumentForm()
    
    # Updated to prefetch related submissions
    sent_requests = DocumentRequest.objects.filter(
    admin=request.user
).prefetch_related('documentsubmission')

    
    return render(request, 'doc_requests/admin.html', {
        'form': form,
        'sent_requests': sent_requests
    })

@login_required
def user_requests(request):
    if request.user.is_staff:
        return redirect('dashboard')
    
    requests = DocumentRequest.objects.filter(user=request.user)
    return render(request, 'doc_requests/user_requests.html', {'requests': requests})

@login_required
def submit_document(request, request_id):
    doc_request = DocumentRequest.objects.get(id=request_id, user=request.user)
    
    if request.method == 'POST':
        form = SubmitDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.request = doc_request
            submission.save()
            doc_request.is_completed = True
            doc_request.save()
            return redirect('dashboard')
    else:
        form = SubmitDocumentForm()
    
    return render(request, 'doc_requests/submit.html', {
        'form': form,
        'request': doc_request
    })