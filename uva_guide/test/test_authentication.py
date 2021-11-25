from allauth.tests import MockedResponse
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.google.provider import GoogleProvider
from allauth.socialaccount.tests import OAuth2TestsMixin
from django.contrib.auth.models import User
from django.test import TestCase


class LoginTests(OAuth2TestsMixin, TestCase):
	provider_id = GoogleProvider.id

	def get_mocked_response(
			self,
			family_name="test",
			given_name="test",
			name="test",
			email="test@example.com",
			verified_email=True,
	):
		return MockedResponse(
			200,
			"""
			  {"family_name": "%s", "name": "%s",
			   "picture": "https://lh5.googleusercontent.com/photo.jpg",
			   "locale": "nl", "gender": "male",
			   "email": "%s",
			   "link": "https://plus.google.com/108204268033311374519",
			   "given_name": "%s", "id": "108204268033311374519",
			   "verified_email": %s }
		"""
			% (
				family_name,
				name,
				email,
				given_name,
				(repr(verified_email).lower()),
			),
		)

	def test_login(self):
		given_name = "John"
		email = "johndoe@example.com"
		self.login(self.get_mocked_response("Doe", given_name, "John Doe", "johndoe@example.com", verified_email=True))

		user = User.objects.get(email=email)
		self.assertEqual(user.first_name, given_name)
		self.assertTrue(
			SocialAccount.objects.filter(user=user, provider=GoogleProvider.id).exists()
		)


