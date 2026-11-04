from blog.models.post import Post
from ..client import ContentClient

MAX_SUMMARY_LENGTH = 500

def _build_prompt(text):
    return (
        f"Summarize the following blog post in at most {MAX_SUMMARY_LENGTH}"
        f"characters. Return only the summary. \n\n{text}"
    )
def summarize_post(post_id):
    if not isinstance(post_id, int) or isinstance(post_id, bool) or post_id <= 0:
        raise ValueError("post_id must be a positive integer")

    post = Post.objects.filter(pk=post_id).first()
    if post is None:
        raise ValueError(f"No post found with id {post_id}")

    if not post.content or not post.content.strip():
        raise ValueError("Post content is empty")

    response = ContentClient().generate(_build_prompt(post.content))

    summary = (response or "").strip()
    if not summary:
        raise ValueError("The model returned an empty summary")

    summary = summary[:MAX_SUMMARY_LENGTH].strip()

    return {
        "post_id": post.id,
        "title": post.title,
        "summary": summary,
        "length": len(summary),
    }
