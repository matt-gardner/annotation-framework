from django.conf.urls import patterns, url

import annotate.views

method_id = '(?P<method_id>\d+)'
pool_id = '(?P<pool_id>\d+)'
task_id = '(?P<task_id>\d+)'

urlpatterns = [
    url(r'^$',
        annotate.views.home, name='annotate-home'),
    url(r'^method/' + method_id + '$',
        annotate.views.method, name='annotate-method'),
    url(r'^method/' + method_id + '/task/' + task_id + '$',
        annotate.views.method_task, name='annotate-method-task'),
    url(r'^task/' + task_id + '$',
        annotate.views.task, name='annotate-task'),
    url(r'^pool/' + pool_id + '$',
        annotate.views.pool_edit_annotations, name='annotate-pool-view-mine'),
    url(r'^pool-unannotated/' + pool_id + '$',
        annotate.views.pool_unannotated, name='annotate-pool-unannotated'),
    url(r'^pool-view-annotations/' + pool_id + '$',
        annotate.views.pool_view_all_annotations, name='annotate-pool-view-annotations'),
    url(r'^pool-results/' + pool_id + '$',
        annotate.views.pool_results, name='annotate-pool-view-results'),
    url(r'^ajax/annotate-instance$',
        annotate.views.annotate, name='annotate-ajax-annotate-instance'),
]
