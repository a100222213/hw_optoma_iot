from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone

"""
[summary]
簡訊相關
"""


class Member(models.Model):
    """
    會員
    """

    # 男女列舉
    MALE = 1
    FEMALE = 0
    GENDER_CHOICES = (
        (MALE, 'male'),
        (FEMALE, 'female'),
    )

    email = models.CharField(
        max_length=160,  primary_key=True, null=False, db_column='email')
    phone = models.CharField(
        u'會員電話', max_length=30, null=True, db_column='phone'
    )
    name = models.CharField(
        u'會員姓名', max_length=160, null=True, db_column='name')
    birthday = models.DateField(
        u'會員生日', null=True, db_column='birthday')
    gender = models.IntegerField(
        u'性別', null=True, choices=GENDER_CHOICES, db_column='gender')
    address = models.CharField(
        u'會員地址',  max_length=255, null=True, db_column='address')
    oauthid = models.CharField(
        u'認證ID', max_length=255, null=True, db_column='oauthid')
    password = models.CharField(
        u'會員密碼', max_length=160, null=False, db_column='password')

    class Meta:
        db_table = 'member'
