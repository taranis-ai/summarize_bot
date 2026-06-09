from typing import Any

def build_story_input_text(news_items: list[dict[str, Any]]) -> str:
    formatted_items = []
    formatted_items.extend(
        "\n".join(
            [
                f"News item {index}",
                f"Title: {news_item.get("title", "")}",
                "Content:",
                news_item.get("content", "-"),
            ]
        )
        for index, news_item in enumerate(news_items, start=1)
    )
    return "\n\n".join(formatted_items)
