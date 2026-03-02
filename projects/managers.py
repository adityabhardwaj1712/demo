from django.db import models


class TaskQuerySet(models.QuerySet):
    def overdue(self):
        return self.filter(status="open")

    def for_user(self, user):
        return self.filter(
            project__organization__memberships__user=user
        )