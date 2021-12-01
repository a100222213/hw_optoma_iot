from django.db import models

# Create your models here.


class Device(models.Model):
    """
    裝置
    """
    # 綁定未綁定列舉
    BIND = 1
    UNBIND = 0
    BIND_CHOICES = (
        (BIND, 'BIND'),
        (UNBIND, 'UNBIND'),
    )

    serialnumber = models.CharField(
        u'裝置序列號', primary_key=True, max_length=300, serialize=False, db_column='serialnumber')
    model = models.CharField(
        u'裝置型號', null=True, max_length=128, serialize=False, db_column='model')
    name = models.CharField(
        u'裝置名稱', null=True, max_length=128, serialize=False, db_column='name')
    bind = models.IntegerField(
        u'是否綁定', null=True, choices=BIND_CHOICES, db_column='bind')
