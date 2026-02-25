from django.db import models


class TaskQuerySet(models.QuerySet):
    def overdue(self):
        return self.filter(status="open")