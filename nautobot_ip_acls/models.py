from django.db import models
from django.urls import reverse
from nautobot.apps.models import BaseModel, ChangeLoggedModel, PrimaryModel

class ACL(PrimaryModel):
    class Meta:
        verbose_name = "ACL"
    identifier = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return self.identifier

class ACLEntry(BaseModel, ChangeLoggedModel):
    class Meta:
        ordering = ("acl__identifier", "sequence_number")
        unique_together = [("acl", "sequence_number")]
        verbose_name = "ACL entry"
        verbose_name_plural = "ACL entries"
    acl = models.ForeignKey(ACL, on_delete=models.CASCADE)
    sequence_number = models.PositiveSmallIntegerField()
    prefix = models.ForeignKey(
    "ipam.Prefix", blank=True, null=True, on_delete=models.CASCADE
    )
    action = models.CharField(
    max_length=10,
    choices=[("permit", "Permit"), ("deny", "Deny")]
    )
    def __str__(self):
        return (
            f"ACL {self.acl}: {self.sequence_number} {self.action} "
            f"{self.prefix or 'any'}"
        )
    def get_absolute_url(self):
        return reverse(
            "plugins:nautobot_ip_acls:aclentry",
            kwargs={"pk": self.pk}
        )
