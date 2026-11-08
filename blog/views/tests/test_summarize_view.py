from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from blog.ai_content.services.summarize import PostNotFoundError
from blog.models.post import Post

# Patch where the VIEW looks the function up, not where it's defined.
VIEW_SERVICE = "blog.views.summarize.summarize_post"
SERVICE_CLIENT = "blog.ai_content.services.summarize.ContentClient"


class SummarizeViewUnitTests(TestCase):
    """The service is mocked, so these only test the view's HTTP behavior."""

    def url(self, post_id=1):
        return reverse("summarize-post", args=[post_id])

    @patch(VIEW_SERVICE)
    def test_success_returns_200_and_service_result(self, mock_service):
        payload = {"post_id": 1, "title": "Hi", "summary": "Short.", "length": 6}
        mock_service.return_value = payload

        response = self.client.post(self.url(1))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), payload)
        mock_service.assert_called_once_with(1)

    @patch(VIEW_SERVICE, side_effect=PostNotFoundError("No post found with id 5"))
    def test_missing_post_returns_404(self, _):
        response = self.client.post(self.url(5))
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.json())

    @patch(VIEW_SERVICE, side_effect=ValueError("Post content is empty"))
    def test_value_error_returns_400(self, _):
        response = self.client.post(self.url(1))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "Post content is empty"})

    @patch(VIEW_SERVICE, side_effect=RuntimeError("secret internal detail"))
    def test_unexpected_error_returns_500_without_leaking(self, _):
        response = self.client.post(self.url(1))
        self.assertEqual(response.status_code, 500)
        self.assertNotIn("secret", response.content.decode())

    def test_get_not_allowed(self):
        self.assertEqual(self.client.get(self.url(1)).status_code, 405)


class SummarizeViewIntegrationTests(TestCase):
    """Real view + real service + real DB; only the OpenAI client is mocked."""

    @patch(SERVICE_CLIENT)
    def test_end_to_end_success(self, mock_client):
        mock_client.return_value.generate.return_value = "  A tidy summary.  "
        post = Post.objects.create(title="Hello", content="A long body of text.")

        response = self.client.post(reverse("summarize-post", args=[post.id]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "post_id": post.id,
            "title": "Hello",
            "summary": "A tidy summary.",
            "length": len("A tidy summary."),
        })

    def test_end_to_end_missing_post(self):
        response = self.client.post(reverse("summarize-post", args=[99999]))
        self.assertEqual(response.status_code, 404)