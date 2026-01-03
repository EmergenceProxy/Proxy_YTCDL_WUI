import boto3
import json
import youtube_comment_downloader 
from itertools import islice 
def analyze_overall_sentiment(youtube_url,loadNumComments, region="us-east-1"):
    youtube_url = youtube_url.strip()
    # youtube_url = "https://www.youtube.com/watch?v=c52IzePdOag"
    print(f"Analyzing sentiment for URL: {youtube_url} with {loadNumComments} comments")
    # Download comments
    downloader = youtube_comment_downloader.YoutubeCommentDownloader()
    SORT_BY_RECENT = 1

    comments_iter = downloader.get_comments_from_url(
        youtube_url,
        sort_by=SORT_BY_RECENT,
        language=None,
        sleep=0.1
    )

    # Extract up to 20 comment texts safely
    texts = []
    for c in islice(comments_iter, loadNumComments):
        t = c.get("text")
        if t:
            texts.append(t.strip())

    if not texts:
        raise RuntimeError("No comments were retrieved. Check the URL or downloader output.")

    # Format comments into a block for the prompt
    comments_block = "\n".join([f'{i+1}. "{t}"' for i, t in enumerate(texts)])

    client = boto3.client("bedrock-runtime", region_name="us-east-1")

    # Use an f-string so comments_block gets injected
    prompt = f"""
    You are a sentiment analysis system.

    Analyze the overall sentiment of the following YouTube comments as a group.

    Tasks:
    1. Determine the overall sentiment: POSITIVE, NEGATIVE, or NEUTRAL.
    2. Count how many comments fall into each category.
    3. Briefly explain what themes or language drove the overall sentiment (max 3 sentences).

    Return JSON only in this exact format:
    {{
    "overall_sentiment": "POSITIVE|NEGATIVE|NEUTRAL",
    "counts": {{
        "positive": 0,
        "negative": 0,
        "neutral": 0
    }},
    "summary": "short explanation"
    }}

    Comments:
    {comments_block}
    """.strip()

    response = client.invoke_model(
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 600,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        })
    )

    raw = json.loads(response["body"].read())

    # Claude responses are typically in raw["content"] as a list of blocks
    # We'll extract the combined text.
    content_blocks = raw.get("content", [])
    model_text = "".join(block.get("text", "") for block in content_blocks)
    print("RAW MODEL TEXT >>>", repr(model_text), "<<<")
    print(model_text)
    return json.loads(model_text)


