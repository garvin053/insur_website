import hashlib

from django.contrib import auth
from django.db import connection
from django.shortcuts import redirect, render
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from .models import CustomUser, YwryPassenger
from .forms import CustomUserCreationForm
from .serializers import UserSerializer
from rest_framework.decorators import action
from django.contrib.auth import login, logout
from rest_framework.response import Response
import re
from datetime import date, datetime
from django.db.utils import DataError


# class UserListView(ListAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [IsAdminUser]

class UserViewset(ModelViewSet):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

    @action(methods=['POST'], url_path='login', detail=False)
    def login(self, request):

        username = request.data.get('username')

        pwd = request.data.get('password')
        pwd = hashlib.sha256(str(pwd).encode('utf-8')).hexdigest()
        res = {
            'code': 0,
            'msg': '',
            'data': {}
        }

        try:
            user = CustomUser.objects.get(username=username, password=pwd)
        except:
            res['msg'] = 'wrong user or password!'
            return Response(res)
        if user.is_active != 1:
            res['msg'] = 'user is not active!'
            return Response(res)

        login(request, user)

        request.session['login'] = True
        request.session['FS_YWPT'] = True
        request.session.set_expiry(0)
        print(request.session['login'], request.session['_auth_user_id'], request.session['_auth_user_hash'],
              request.session['_auth_user_backend'], user.customer_id)
        res['msg'] = '登陆成功'
        res['code'] = 1
        res['data'] = {'username': username, 'token': request.session['_auth_user_hash'], 'id': user.customer_id,
                       'is_staff': user.is_staff}
        return Response(res)

    @action(methods=['POST'], url_path='register', detail=False)
    def register(self, request):

        email = request.data.get('email')
        password1 = request.data.get('password1')
        password2 = request.data.get('password2')
        first_name = request.data.get('fname')
        last_name = request.data.get('lname')
        nationality = request.data.get('nationality')
        city = request.data.get('city')
        street = request.data.get('street')
        zipcode = request.data.get('zipcode')
        emer_contact_num = request.data.get('contact')
        emer_contact_person = request.data.get('contactPerson')
        gender = request.data.get('gender')
        username = email
        if gender == 'male':
            gender = 1
        else:
            gender = 0

        # customer_type = request.data.get('emer_contact_person')

        res = {
            'code': 0,
            'msg': '',
            'data': {}
        }

        if CustomUser.objects.filter(email=email):
            res['msg'] = 'email exist'
            return Response(res)

        if password1 != password2:
            res['msg'] = 'The two password fields does not match'
            return Response(res)

        pattern = re.compile("^[\dA-Z]{3}-[\dA-Z]{3}-[\dA-Z]{4}$", re.IGNORECASE)
        if not pattern.match(emer_contact_num):
            res['msg'] = 'emergency contact number type is wrong'
            return Response(res)
        password = hashlib.sha256(str(password2).encode('utf-8')).hexdigest()

        CustomUser.objects.create(first_name=first_name, email=email, password=password, last_name=last_name,
                                  nationality=nationality, city=city, street=street, zipcode=zipcode,
                                  emer_contact_person=emer_contact_person,
                                  emer_contact_num=emer_contact_num, gender=gender, username=username)

        # request.data['password'] = password
        # request.data['username'] = username
        # print(request.data)
        # user = auth.authenticate(request, username=username,
        #                          password=password)
        # print(user, '111222')
        # print(auth.login(request, user))
        # print(request.session)
        # res['data']['token'] = hashlib.sha256(str(email).encode('utf-8')).hexdigest()
        res['code'] = 1

        return Response(res)

    @action(methods=['POST'], url_path='logout', detail=False)
    def logout(self, request):
        res = {
            'code': 1,
            'msg': '',
            'data': {}
        }
        return Response(res)

    @action(methods=['POST'], url_path='userinfo', detail=False)
    def userinfo(self, request):

        res = {
            'code': 0,
            'msg': '',
            'data': {}
        }

        user_name = request.data.get('username')

        user = CustomUser.objects.raw('SELECT * FROM users_customuser WHERE username = %s', [user_name])
        for i in user:
            for attr, value in i.__dict__.items():
                if attr == 'gender':
                    value = 'Male' if value == 1 else 'Female'
                res['data'][str(attr)] = str(value)

        return Response(res)

    @action(methods=['POST'], url_path='userinfoedit', detail=False)
    def userinfoedit(self, request):
        res = {
            'code': 1,
            'msg': '',
            'data': {}
        }

        gender = request.data.get('gender')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')

        street = request.data.get('street')
        zipcode = request.data.get('zipcode')
        nationality = request.data.get('nationality')
        city = request.data.get('city')
        username = request.data.get('username')
        if gender == 'Female':
            gender = '0'
        else:
            gender = '1'

        print('222', [first_name, last_name, gender, street, zipcode, nationality, city, username])

        with connection.cursor() as cursor:
            cursor.execute(' update users_customuser set first_name = %s,last_name = %s, '
                           ' gender = %s, street = %s , zipcode = %s,'
                           ' nationality = %s, city = %s where username = %s'
                           , [first_name, last_name, gender, street, zipcode, nationality, city,
                              username])
            row = cursor.fetchall()
            print(row)

        return Response(res)

    @action(methods=['POST'], url_path='invoice', detail=False)
    def InvoiceInfomation(self, request):
        res = {
            'code': 1,
            'msg': '',
            'data': []
        }

        customer_id = request.data.get('customer_id')

        rows = []
        with connection.cursor() as cursor:
            cursor.execute(
                'select ywry_invoice.invoice_id, ywry_passenger.fname,ywry_passenger.lname, ywry_passenger.passport_number, ywry_invoice.invoice_amount, ywry_invoice.invoice_date, ywry_invoice.flight_id '
                'from users_customuser,ywry_passenger,ywry_invoice '
                'where users_customuser.customer_id = ywry_passenger.customer_id AND '
                'ywry_passenger.passenger_id = ywry_invoice.passenger_id AND users_customuser.customer_id = %s '
                'ORDER BY invoice_date desc '
                , [customer_id])
            rows = cursor.fetchall()
        print(rows[0])

        attrs = ['invoice_id', 'fname', 'lname', 'passport_number', 'invoice_amount', 'invoice_date', 'flight_id']
        for row in rows:
            tmp_data = {'name': ''}
            for i in range(len(attrs)):

                if attrs[i] == 'invoice_date':
                    tmp_data['invoice_date'] = str(row[i])[:19]
                    if datetime.strptime(tmp_data['invoice_date'], '%Y-%m-%d %H:%M:%S') < datetime.now():
                        tmp_data['expired'] = 1
                    else:
                        tmp_data['expired'] = 0
                    continue
                if attrs[i] == 'fname' or attrs[i] == 'lname':
                    tmp_data['name'] += row[i] + " "
                    continue

                tmp_data[attrs[i]] = row[i]

            res['data'].append(tmp_data)
        print(res)
        return Response(res)

    @action(methods=['POST'], url_path='payment', detail=False)
    def PaymentInfo(self, request):
        res = {
            'code': 1,
            'msg': '',
            'data': []
        }

        invoice_id = request.data.get('invoice_id')
        print(invoice_id)
        rows = []
        with connection.cursor() as cursor:
            cursor.execute(
                ' select invoice_amount,payment_amount,payment_date,card_number,name_on_card,expire_date,method from ywry_invoice,ywry_payment'
                ' where ywry_invoice.invoice_id = ywry_payment.invoice_id'
                ' and ywry_invoice.invoice_id = %s'
                , [invoice_id])
            rows = cursor.fetchall()
        print(rows[0])

        attrs = ['invoice_amount', 'payment_amount', 'payment_date', 'card_number', 'name_on_card', 'expire_date',
                 'method']
        payment_amount = 0
        for row in rows:
            tmp_data = {}
            for i in range(len(attrs)):

                if attrs[i] == 'card_number':
                    tmp_data['card_number'] = '*' * (len(row[i]) - 4) + str(row[i])[-4:]
                    continue
                if attrs[i] == 'expire_date':
                    tmp_data['expire_date'] = str(row[i])[:10]
                    continue
                if attrs[i] == 'payment_date':
                    tmp_data['payment_date'] = str(row[i])[:19]
                    continue
                if attrs[i] == 'payment_amount':
                    payment_amount += row[i]

                tmp_data[attrs[i]] = row[i]

            res['data'].append(tmp_data)
        balance = rows[0][0] - payment_amount
        print(balance)
        res['payment_amount'] = payment_amount
        res['balance'] = balance

        return Response(res)


class PassengerViewset(ModelViewSet):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

    @action(methods=['POST'], url_path='passengerInfo', detail=False)
    def passengerinfo(self, request):

        res = {
            'code': 0,
            'msg': '',
            'data': []
        }
        if request.data.get('username') and not request.data.get('passenger_id'):
            # select all passenger of one customer
            user_name = request.data.get('username')

            user = CustomUser.objects.raw('SELECT customer_id FROM users_customuser WHERE username = %s', [user_name])
            print(request, user[0].customer_id)
            customer_id = user[0].customer_id
            passengers = YwryPassenger.objects.raw('select * from ywry_passenger where customer_id = %s', [customer_id])
            for passenger in passengers:
                tmp_data = {}
                for attr, value in passenger.__dict__.items():
                    if attr == 'gender':
                        value = 'Male' if value == 'M' else 'Female'
                    if attr == 'dob' or attr == 'passport_expiry_date':
                        value = str(value)[:10]
                    tmp_data[str(attr)] = str(value)

                res['data'].append(tmp_data)

            return Response(res)

        else:
            # select the information by passenger_id
            passenger_id = request.data.get('passenger_id')['id']

            passengers = YwryPassenger.objects.raw('select * from ywry_passenger where passenger_id = %s',
                                                   [passenger_id])

            for passenger in passengers:
                tmp_data = {}
                for attr, value in passenger.__dict__.items():
                    if attr == 'gender':
                        value = 'Male' if value == 'M' else 'Female'
                    if attr == 'dob' or attr == 'passport_expiry_date':
                        value = str(value)[:10]
                    tmp_data[str(attr)] = str(value)

                res['data'].append(tmp_data)

            return Response(res)

    @action(methods=['POST'], url_path='passengerInfoEdit', detail=False)
    def passengerinfoedit(self, request):

        res = {
            'code': 1,
            'msg': '',
            'data': {}
        }

        passenger_id = request.data.get('passenger_id')

        fname = request.data.get('fname')
        lname = request.data.get('lname')
        dob = request.data.get('dob')
        nationaliry = request.data.get('nationaliry')
        gender = request.data.get('gender')
        if gender == 'Female':
            gender = 'F'
        else:
            gender = 'M'
        passport_number = request.data.get('passport_number')
        passport_expiry_date = request.data.get('passport_expiry_date')

        with connection.cursor() as cursor:
            cursor.execute('update ywry_passenger set lname = %s,fname = %s, '
                           'dob = %s, nationaliry = %s , gender = %s,'
                           'passport_number = %s,passport_expiry_date = %s where passenger_id = %s'
                           , [lname, fname, dob, nationaliry, gender, passport_number, passport_expiry_date,
                              passenger_id])
            row = cursor.fetchone()

        res['data']['passenger_id'] = passenger_id

        return Response(res)

    @action(methods=['POST'], url_path='passengerInfoInsert', detail=False)
    def passengerinfoinsert(self, request):

        res = {
            'code': 1,
            'msg': '',
            'data': {}
        }

        customer_id = request.data.get('customer_id')

        fname = request.data.get('fname')
        lname = request.data.get('lname')
        dob = request.data.get('dob')
        nationaliry = request.data.get('nationaliry')
        gender = request.data.get('gender')
        if gender == 'Female':
            gender = 'F'
        else:
            gender = 'M'
        passport_number = request.data.get('passport_number')
        passport_expiry_date = request.data.get('passport_expiry_date')

        with connection.cursor() as cursor:
            cursor.execute(
                'insert into ywry_passenger(lname,fname,dob,nationaliry,gender,passport_number,passport_expiry_date,customer_id) values(%s,%s,%s,%s,%s,%s,%s,%s)'
                , [lname, fname, dob, nationaliry, gender, passport_number, passport_expiry_date,
                   customer_id])
            row = cursor.fetchone()

        return Response(res)

    @action(methods=['POST'], url_path='passengerDelete', detail=False)
    def passengerDelete(self, request):

        res = {
            'code': 1,
            'msg': '',
            'data': {}
        }

        passenger_id = request.data.get('passenger_id')

        with connection.cursor() as cursor:
            cursor.execute(
                'delete from ywry_passenger where passenger_id = %s'
                , [passenger_id])
            row = cursor.fetchone()

        return Response(res)


class AnalyseViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

    @action(methods=['POST'], url_path='invoice', detail=False)
    def invoiceanalyse(self, request):
        res = {
            'code': 1,
            'msg': '',
            'data': {}
        }


        invoice_total = [0] * 12

        rows = []
        with connection.cursor() as cursor:
            cursor.execute(
                'select DATE_FORMAT(invoice_date,"%Y%m") as date, SUM(invoice_amount) from ywry_invoice'
                ' where is_complete = 1'
                ' GROUP BY date')
            rows = cursor.fetchall()

        for row in rows:
            print(row[0],row[1])
            date = str(row[0])
            if date[:4] == '2021':
                invoice_total[int(date[-2:]) -1] = row[1]

        res['data'] = invoice_total
        return Response(res)

    @action(methods=['POST'], url_path='passenger', detail=False)
    def passengeranalyse(self, request):
        res = {
            'code': 1,
            'msg': '',
            'data': []
        }

        invoice_total = [0] * 12

        rows = []
        attrs = ['amount','passenger_id','first_name','last_name','order_num']
        with connection.cursor() as cursor:
            cursor.execute(
                'select sum(invoice_amount) as amount,ywry_passenger.passenger_id,ywry_passenger.fname,ywry_passenger.lname,count(*)'
                ' from ywry_passenger, ywry_invoice where ywry_passenger.passenger_id = ywry_invoice.passenger_id'
                ' GROUP BY ywry_passenger.passenger_id ORDER BY amount DESC limit 10')
            rows = cursor.fetchall()

        for row in rows:
            tmp_data = {}
            for i in range(len(attrs)):

                tmp_data[attrs[i]] = row[i]

            res['data'].append(tmp_data)


        return Response(res)


