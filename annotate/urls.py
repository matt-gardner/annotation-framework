from django.conf.urls import patterns, url

method_id = '(?P<method_id>\d+)'
pool_id = '(?P<pool_id>\d+)'
task_id = '(?P<task_id>\d+)'

urlpatterns = patterns('annotate.views',
    url(r'^$',
        'home', name='annotate-home'),
    url(r'^method/' + method_id + '$',
        'method', name='annotate-method'),
    url(r'^method/' + method_id + '/task/' + task_id + '$',
        'method_task', name='annotate-method-task'),
    url(r'^task/' + task_id + '$',
        'task', name='annotate-task'),
    url(r'^pool/' + pool_id + '$',
        'pool_edit_annotations', name='annotate-pool-view-mine'),
    url(r'^pool-unannotated/' + pool_id + '$',
        'pool_unannotated', name='annotate-pool-unannotated'),
    url(r'^pool-view-annotations/' + pool_id + '$',
        'pool_view_all_annotations', name='annotate-pool-view-annotations'),
    url(r'^pool-results/' + pool_id + '$',
        'pool_results', name='annotate-pool-view-results'),
    url(r'^ajax/annotate-instance$',
        'annotate', name='annotate-ajax-annotate-instance'),
)
