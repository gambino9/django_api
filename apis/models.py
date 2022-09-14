from django.db import models


class MakeQuery(models.Model):
    received_query = models.CharField(max_length=200)
