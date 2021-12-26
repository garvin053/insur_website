# Django React Auth

## Overview

A class web project

frontend: use react + axio + rooter + bootstrap5, dompurify to prevent XSS attack

backend: use django + auth + router

database : mysql

## Dependencies

1. Python 3.5 or greater
2. Django 3.1
3. React 17.0

## project summary

First, we have a strong authentication and authorization system which can help the company efficiently to manage their user’s account login, logout, signup and manage the different pages and data viewed by different users with different permissions, like normal users account and staff account. To be more precisely, we use the django.contrib.auth model to automatically manage the sessions and permissions of each user, this model would create tables django_session table: store each user's encrypted session and expired time; django.group: store user’s type django.permission: store each group’s permission.

Second, the customer can update the user’s own information and create, update, read, delete the passenger’s information. The website will check each input field fully and separately, like if the newly created passenger’s passport id is the same as one in the database, if the input phone number is a legal phone number. We do this part based on the automatic type checking and some business rule checking.

Third, the customer can buy different types of insurance, and all types of insurance bought by this customer would be listed in the invoice list page. Each invoice has a parameter ‘expiry time’ which is caculated exact three days before the passenger’s departure time(business rule). For convenience, the invoices are ordered by its expiration time descending so that customers can see the most recent invoice. And if one invoice expired time is smaller than the current time, then this invoice would be marked expired, you can’t do any actions for this invoice. If this invoice expiry time is greater than the current time, you can click a button the view the payment history of this invoice(some digit of card number is masked for security), if this invoice is not fully paid, you can continue to do payment by both debit card or credit card method. If this invoice is fully paid, the website would hide the pay button and tell you that you are done with this invoice

Fourth, we have some special accounts for the company staff. If company staff use the staff account to login in the website, they can view an analyse page which is hidden from customer users.In the analyse page, staffs can view the total pairs sales amount of each month of this year and last year, they can do some analyses based the trend of sales amount or year-on-year comparison. This page also list the top 10 spenders in this year, list the spenders’ total insurance spending, order numbers, name and so on, staff can use this cart to do some customer lever analyse

Fifth, For website and sql security, We use some libraries and code rules to prevent SQL injection and Cross Site Scripting. In more detail, we use django’s model object and use parameters in raw sql , two ways to prevent sql injection. Using React’s dompurify package to prevent cross site scripting.
