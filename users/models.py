from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    #mname = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30)
    nationality = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=30, blank=True)
    street = models.CharField(max_length=30, blank=True)
    zipcode = models.IntegerField(blank=True,default=0)
    #email = models.CharField(max_length=30)
    emer_contact_num = models.CharField(max_length=14, blank=True)
    emer_contact_person = models.CharField(max_length=30, blank=True)
    gender = models.CharField(max_length=1, blank=True)
    numbers_passengers = models.SmallIntegerField(blank=True, default=1)
    customer_type = models.CharField(max_length=1, blank=True)
    password = models.CharField(max_length=150)
    #nationality = models.CharField('nationality', max_length=150, blank=True)

    def __str__(self):
        return self.email

    class Meta:
        managed = False
        db_table = 'users_customuser'


class YwryAgent(models.Model):
    customer = models.OneToOneField('CustomUser', models.DO_NOTHING, primary_key=True)
    agent_name = models.CharField(max_length=30)
    agent_web = models.CharField(max_length=30)
    agent_phone = models.CharField(max_length=14)

    class Meta:
        managed = False
        db_table = 'ywry_agent'


class YwryAircraft(models.Model):
    aircraft_id = models.IntegerField(primary_key=True)
    model_name = models.CharField(max_length=30)
    manufacturer = models.CharField(max_length=30)
    number_engines = models.IntegerField()
    number_fleet = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ywry_aircraft'


class YwryAirlAirc(models.Model):
    airline = models.ForeignKey('YwryAirline', models.DO_NOTHING, blank=True, null=True)
    aircraft = models.ForeignKey(YwryAircraft, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ywry_airl_airc'


class YwryAirline(models.Model):
    airline_id = models.IntegerField(primary_key=True)
    airline_name = models.CharField(max_length=30)
    main_hub = models.CharField(max_length=30)
    headquarter_city = models.CharField(max_length=30)
    country = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'ywry_airline'


class YwryAirport(models.Model):
    airport_id = models.IntegerField(primary_key=True)
    airport_code = models.CharField(max_length=10)
    name = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    type = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'ywry_airport'


# class YwryCustomer(models.Model):
#     customer_id = models.IntegerField(primary_key=True)
#     fname = models.CharField(max_length=30)
#     mname = models.CharField(max_length=30, blank=True, null=True)
#     lname = models.CharField(max_length=30)
#     nationality = models.CharField(max_length=30)
#     city = models.CharField(max_length=30)
#     street = models.CharField(max_length=30)
#     zipcode = models.IntegerField()
#     email = models.CharField(max_length=30)
#     emer_contact_num = models.CharField(max_length=14)
#     emer_contact_person = models.CharField(max_length=30)
#     gender = models.CharField(max_length=1)
#     numbers_passengers = models.SmallIntegerField()
#     customer_type = models.CharField(max_length=1)
#
#     class Meta:
#         managed = False
#         db_table = 'ywry_customer'


class YwryFlight(models.Model):
    flight_id = models.IntegerField(primary_key=True)
    departure_time = models.DateTimeField()
    departure_time_zone = models.CharField(max_length=30)
    arrival_time = models.DateTimeField()
    arrival_time_zone = models.CharField(max_length=30)
    airline = models.ForeignKey(YwryAirline, models.DO_NOTHING, blank=True, null=True)
    #departure_airport = models.ForeignKey(YwryAirport, models.DO_NOTHING)
    arrival_airport = models.ForeignKey(YwryAirport, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'ywry_flight'


class YwryInsuranceInvoice(models.Model):
    insurance = models.ForeignKey('YwryInsurancePlans', models.DO_NOTHING, blank=True, null=True)
    invoice = models.ForeignKey('YwryInvoice', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'ywry_insurance_invoice'


class YwryInsurancePlans(models.Model):
    insurance_id = models.IntegerField(primary_key=True)
    plan_name = models.CharField(max_length=30)
    description = models.CharField(max_length=1000)
    cost_per_person = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'ywry_insurance_plans'


class YwryInvoice(models.Model):
    invoice_id = models.IntegerField(primary_key=True)
    invoice_date = models.DateTimeField()
    invoice_amount = models.DecimalField(max_digits=7, decimal_places=2)
    flight = models.ForeignKey(YwryFlight, models.DO_NOTHING, blank=True, null=True)
    passenger = models.ForeignKey('YwryPassenger', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ywry_invoice'


class YwryMember(models.Model):
    customer = models.OneToOneField(CustomUser, models.DO_NOTHING, primary_key=True)
    membership_name = models.CharField(max_length=30)
    associated_airline = models.CharField(max_length=30)
    mem_start_date = models.DateTimeField()
    mem_end_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ywry_member'


class YwryPassenger(models.Model):
    passenger_id = models.IntegerField(primary_key=True)
    fname = models.CharField(max_length=30)
    mname = models.CharField(max_length=30, blank=True, null=True)
    lname = models.CharField(max_length=30)
    dob = models.DateTimeField()
    nationaliry = models.CharField(max_length=30)
    gender = models.CharField(max_length=1)
    passport_number = models.CharField(max_length=30)
    passport_expiry_date = models.DateTimeField()
    customer = models.ForeignKey(CustomUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'ywry_passenger'


class YwryPayment(models.Model):
    payment_date = models.DateTimeField()
    payment_amount = models.DecimalField(max_digits=7, decimal_places=2)
    method = models.CharField(max_length=30)
    card_number = models.CharField(max_length=20)
    name_on_card = models.CharField(max_length=30)
    expire_date = models.DateTimeField()
    invoice = models.ForeignKey(YwryInvoice, models.DO_NOTHING, blank=True, null=True)
    customer = models.ForeignKey(CustomUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ywry_payment'


class YwrySpeRequest(models.Model):
    assistance_id = models.IntegerField(primary_key=True)
    assistance_name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'ywry_spe_request'


class YwryTravelDetail(models.Model):
    travel_id = models.IntegerField(primary_key=True)
    cabin_class = models.CharField(max_length=2)
    meal_plan = models.CharField(max_length=30)
    passenger = models.ForeignKey(YwryPassenger, models.DO_NOTHING, blank=True, null=True)
    flight = models.ForeignKey(YwryFlight, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ywry_travel_detail'


class YwryTravelRequest(models.Model):
    travel = models.ForeignKey(YwryTravelDetail, models.DO_NOTHING, blank=True, null=True)
    assistance = models.ForeignKey(YwrySpeRequest, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ywry_travel_request'