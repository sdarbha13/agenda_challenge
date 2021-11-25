from django.db import models


class ProfileTypes(models.TextChoices):
	STUDENT = "student"
	ORGANIZER = "organizer"
