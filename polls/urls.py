from django.urls import path
from .views import PollListView, create_poll, poll_detail, vote, poll_results

app_name = 'polls'

urlpatterns = [
    path('', PollListView.as_view(), name='poll_list'),
    path('create/', create_poll, name='create_poll'),
    path('<int:poll_id>/', poll_detail, name='poll_detail'),
    path('<int:poll_id>/vote/', vote, name='vote'),
    path('<int:poll_id>/results/', poll_results, name='poll_results'),
]