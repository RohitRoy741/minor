# College Social Network

## Introduction

The django web app performs most of the basic functions of a social application like facebook, instagram and twiiter.
The application's backend is completely written in python using django framework and database used is SQLite3 which is
default database of django.

## Features

<ul>
  <li>New Users can register and then subsequently login to their account.</li>
  ![](images/login.png)
  <li>Logged in users can create posts which will be visible to all the users who follow them.</li>
  <li>Users can also create requests to follow other users.</li>
  <li>Follow requests will be visible on the homepage which can be accepted.</li>
  <li>Authenticated Users can also like and comment on the posts of other users who have followed them.</li>
  <li>A suggestion link at the navbar provides a list of users to follow.</li>
  <li>A Question and Answer section where authenticated users can ask and answer questions.</li>
</ul>

## Under Development

<ul>
  <li>Two factor face recognition system (Just change the view in minor/urls.py).</li>
  <li>Direct messaging between the users.</li>
  <li>A search bar to search users,questions and posts.</li>
  <li>Tagging Friends in posts, questions, etc.</li>
  <li>Adding nice icons for liking, commenting etc.</li>
  <li>Using ajax to prevent page refresh every time a user likes a post or follow someone</li>
  <li>A better UI aimed at simplifying the application</li>
  <li>Making the face recognition more robust</li>
</ul>

## Installation

<p>Follow these steps to run the web app in your local machine</p>

<ol>
  <li>Make a virtual environment</li>
  <li>Clone the git repo using the command
  
  ``` bash
  git clone https://github.com/RohitRoy741/minor.git
  ```
  </li>
  <li> Move inside the minor directory (the one which contains requirements.txt) </li>
  <li> Install the requirements using pip
  
  ``` bash
  pip install -r requirements.txt
  ```
  </li>
  <li> Run the local server 
  
  ``` bash
  python manage.py runserver
  ```
  </li>
</ol>

## Contribution

<p> Any contribution is welcome, the web app is yet a work in progress. You can do a pull requests however it will better to
open and issue for discussing major changes </p>
