from unittest.mock import patch
from django.test import TestCase

from blog.models import Post  # your actual model
from ai_content.services.summarize import summarize_post


class SummarizePostTests(TestCase):
    def setUp(self):
        self.post = Post.objects.create(title="Hello", content="Some long text...")

    # --- input validation ---
    def test_rejects_non_integer(self):
        with self.assertRaises(ValueError):
            summarize_post("1")

    def test_rejects_zero_and_negative(self):
        for bad in (0, -1):
            with self.assertRaises(ValueError):
                summarize_post(bad)

    def test_rejects_bool(self):
        with self.assertRaises(ValueError):
            summarize_post(True)

    # --- database ---
    def test_missing_post(self):
        with self.assertRaises(ValueError):
            summarize_post(99999)

    def test_empty_content(self):
        empty = Post.objects.create(title="Empty", content="   ")
        with self.assertRaises(ValueError):
            summarize_post(empty.id)

    # --- AI processing (patch where it's USED, not where it's defined) ---
    @patch("ai_content.services.summarize.ContentClient")
    def test_success(self, mock_client):
        mock_client.return_value.generate.return_value = "  A short summary.  "
        result = summarize_post(self.post.id)

        self.assertEqual(result, {
            "post_id": self.post.id,
            "title": "Hello",
            "summary": "A short summary.",
            "length": len("A short summary."),
        })
        mock_client.return_value.generate.assert_called_once()

    @patch("ai_content.services.summarize.ContentClient")
    def test_empty_summary_rejected(self, mock_client):
        mock_client.return_value.generate.return_value = "   "
        with self.assertRaises(ValueError):
            summarize_post(self.post.id)

    @patch("ai_content.services.summarize.ContentClient")
    def test_summary_truncated_to_500(self, mock_client):
        mock_client.return_value.generate.return_value = "x" * 800
        result = summarize_post(self.post.id)
        self.assertLessEqual(result["length"], 500)
        self.assertEqual(result["length"], len(result["summary"]))