from tortoise.models import Model
from tortoise import fields


class Proxy(Model):
    id = fields.IntField(pk=True)
    # change to max length of proxy?
    ip = fields.CharField(unique=True, max_length=255)
    port = fields.IntField()
    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)
    is_anonymous = fields.BooleanField(default=False)
    is_https = fields.BooleanField(default=False)
    monitor_stability = fields.FloatField(default=100)
    monitor_latency = fields.FloatField(default=0)
    monitor_success = fields.IntField(default=0)
    monitor_attempts = fields.IntField(default=0)
    requests_stability = fields.FloatField(default=100)
    requests_made = fields.IntField(default=0)
    request_latency = fields.IntField(default=0)
    status_2xx = fields.IntField(default=0)
    status_4xx = fields.IntField(default=0)
    status_5xx = fields.IntField(default=0)
    region = fields.CharField(null=True, max_length=255)

    def __str__(self):
        return self.ip
