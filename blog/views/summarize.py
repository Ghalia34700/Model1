import logging

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from blog.ai_content.services.summarize import PostNotFoundError, summarize_post

logger = logging.getLogger(__name__)


@csrf_exempt
@require_POST
def summarize_view(request, post_id):
    try:
        result = summarize_post(post_id)
    except PostNotFoundError as exc:
        return JsonResponse({"error": str(exc)}, status=404)
    except ValueError as exc:
        return JsonResponse({"error": str(exc)}, status=400)
    except Exception:
        logger.exception("Summarization failed for post %s", post_id)
        return JsonResponse({"error": "Could not generate summary."}, status=500)

    return JsonResponse(result, status=200)