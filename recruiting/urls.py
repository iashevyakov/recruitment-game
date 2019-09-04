from django.conf.urls import url

from recruiting import views

app_name = 'recruiting'

urlpatterns = [
    url('^$', views.main, name='main'),
    url('^recruit$', views.recruit, name='recruit'),
    url('^sith$', views.sith, name='sith'),
    url('^test$', views.pass_test, name='pass_test'),
    url('^recruits_list$', views.recruits_list, name='recruits_list'),
    url('^answers/(?P<recruit_id>\d+)$', views.recruit_answers, name='recruit_answers'),
    url('^answers/additional$', views.additional, name='additional')

]
