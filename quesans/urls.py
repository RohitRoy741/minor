from django.contrib import admin
from django.urls import path,include
from . import views
app_name='quesans'

urlpatterns = [
    path('list/',views.YourQuestionListView.as_view(),name='qlist'),
    path('',views.QuestionListView.as_view(),name='clist'),
    path('postanswer/<int:pk>/new/',views.AnswerPostView.as_view(),name='postans'),
    path('post/new/',views.PostQuestionView.as_view(),name='postq'),
    path('searchquestion/',views.SearchView.as_view(),name='qsearch'),
    path('<slug:slug>/',views.QuestionAnswerView.as_view(),name='qthread'),
    path('answer/<int:pk>/',views.AnswerDetail,name='ans-detail'),
    path('answer/reply/', views.reply_page, name="reply"),
    path('Answered/<slug:slug>/',views.QuestionAnswered,name='ques-flag'),
    path('upvote/<slug:slug>/',views.UpvoteView,name='upvote-ans'),
    path('downvote/<slug:slug>/',views.DownvoteView,name='downvote-ans'),
    path('post/<int:pk>/update/',views.QuestionUpdateView.as_view(),name='qupdate'),
    path('postanswer/<int:pk>/delete/',views.AnswerDeleteView.as_view(),name='delanswer'),
]
