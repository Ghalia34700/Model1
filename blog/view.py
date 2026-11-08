from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Post
from .ai_content.services.summarize import summarize_post

# call the decorator
@csrf_exempt
def summarize_post_view(request, post_id):
    try:
        result = summarize_post(post_id)
        return JsonResponse(result, status=200)

# Handle missing posts
    except Post.DoesNotExist:
        return JsonResponse({"error": f"Post with ID {post_id} does not exist."}, status=404)

    except ValueError as e:
        return JsonResponse({"error": e}, status=400)

