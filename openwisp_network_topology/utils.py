import sys

from django.core.exceptions import ValidationError
from django.dispatch import Signal
from django.http import Http404
from django.shortcuts import get_object_or_404 as get_obj_or_404
from django.urls import path, re_path

link_status_changed = Signal()
link_status_changed.__doc__ = """
Providing arguments: ['link']
"""


def print_info(message):  # pragma no cover
    """
    print info message if calling from management command ``update_all``
    """
    if 'update_topology' in sys.argv:
        print('{0}\n'.format(message))


def get_object_or_404(model, pk, **kwargs):
    """
    retrieves topology with specified arguments or raises 404
    """
    kwargs.update({'pk': pk, 'published': True})
    try:
        return get_obj_or_404(model, **kwargs)
    except ValidationError:
        raise Http404()


def get_api_urls(views_module):
    """
    used by third party apps to reduce boilerplate
    """
    urls = [
        path('topology/', views_module.network_collection, name='network_collection'),
        path(
            'topology/<uuid:pk>/',
            views_module.network_graph,
            name='network_graph',
        ),
        path(
            'topology/<uuid:pk>/history/',
            views_module.network_graph_history,
            name='network_graph_history',
        ),
        path(
            'topology/<uuid:pk>/receive/',
            views_module.receive_topology,
            name='receive_topology',
        ),
    ]
    return urls


def get_visualizer_urls(views_module):
    """
    used by third party apps to reduce boilerplate
    """
    urls = [
        path('', views_module.topology_list, name='topology_list'),
        re_path(
            r'^topology/(?P<pk>[^/]+)/$',
            views_module.topology_detail,
            name='topology_detail',
        ),
    ]
    return urls
