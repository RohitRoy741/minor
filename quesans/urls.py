from django.contrib import admin
from django.urls import path,include
from . import views
app_name='quesans'

urlpatterns = [
    path('your-list/<str:filter>',views.YourQuestionListView.as_view(),name='qlist'),
    path('',views.QuestionListView.as_view(),name='clist'),
    path('postanswer/<int:pk>/new/',views.AnswerPostView.as_view(),name='postans'),
    path('post/new/',views.PostQuestionView.as_view(),name='postq'),
    path('searchquestion/',views.SearchView.as_view(),name='qsearch'),
    path('voteup/',views.QuesVoteup,name='ques-voteup'),
    path('votedown/',views.QuesVotedown,name='ques-votedown'),
    path('<slug:slug>/',views.QuestionAnswerView.as_view(),name='qthread'),
    path('answer/<int:pk>/',views.AnswerDetail,name='ans-detail'),
    path('answer/reply/', views.reply_page, name="reply"),
    path('Answered/<slug:slug>/',views.QuestionAnswered,name='ques-flag'),
    path('Bookmark/<slug:slug>/',views.BookmarkView,name='ques-bookmark'),
    path('upvote/<slug:slug>/',views.UpvoteView,name='upvote-ans'),
    path('downvote/<slug:slug>/',views.DownvoteView,name='downvote-ans'),
    path('post/<int:pk>/update/',views.QuestionUpdateView.as_view(),name='qupdate'),
    path('post/<int:pk>/delete/',views.QuestionDeleteView.as_view(),name='delquestion'),
    path('postanswer/<int:pk>/delete/',views.AnswerDeleteView.as_view(),name='delanswer'),
    path('postanswer/<int:pk>/update/',views.AnswerUpdateView.as_view(),name='ansupdate'),
]
