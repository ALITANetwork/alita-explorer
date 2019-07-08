from django.db.models import Count
from django.views.generic import ListView, DetailView

from scan.models import PeerMonitor


class PeerMonitorListView(ListView):
    model = PeerMonitor
    queryset = PeerMonitor.objects.all()
    template_name = 'peers/list.html'
    context_object_name = 'peers'
    paginate_by = 25
    ordering = ('-height', 'ip')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['online_now'] = PeerMonitor.objects.filter(state=PeerMonitor.State.ONLINE).count()
        context['versions'] = PeerMonitor.objects.filter(
            state=PeerMonitor.State.ONLINE
        ).values('version').annotate(cnt=Count('version')).order_by('-cnt')

        context['countries'] = PeerMonitor.objects.filter(
            state=PeerMonitor.State.ONLINE
        ).values('country_code').annotate(cnt=Count('country_code')).order_by('-cnt', 'country_code')

        context['last_check'] = PeerMonitor.objects.values('modified_at').order_by('-modified_at').first()

        return context


class PeerMonitorDetailView(DetailView):
    model = PeerMonitor
    queryset = PeerMonitor.objects.all()
    template_name = 'peers/detail.html'
    context_object_name = 'peer'
    slug_field = 'ip'
    slug_url_kwarg = 'ip'