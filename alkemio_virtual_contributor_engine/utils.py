import re
from alkemio_virtual_contributor_engine.events.input import (
    HistoryItem,
    MessageSenderRole,
)

language_mapping = {
    "EN": "English",
    "US": "English",
    "UK": "English",
    "FR": "French",
    "DE": "German",
    "ES": "Spanish",
    "NL": "Dutch",
    "BG": "Bulgarian",
    "UA": "Ukranian",
}


# function to retrieve language from country
def get_language_by_code(language_code):
    """
    Returns the language associated with the given code.
    If no match is found, it returns 'English'.
    """
    return language_mapping.get(language_code, "English")


def combine_documents(docs, document_separator="\n\n"):
    """Combine a list of documents into a single string.

    Accepts either LangChain Document objects (with .page_content)
    or plain strings.
    """
    parts = []
    for doc in docs:
        if isinstance(doc, str):
            parts.append(doc)
        else:
            parts.append(doc.page_content)
    return document_separator.join(parts)


def clear_tags(message):
    return re.sub(r"(-? ?\[@?.*\]\(.*?\))|}|{", "", message).strip()


def entry_as_string(entry: HistoryItem):
    if entry.role == MessageSenderRole.HUMAN:
        return f"Human: {clear_tags(entry.content)}"
    return f"Assistant: {clear_tags(entry.content)}"


def history_as_text(history: list[HistoryItem]):
    return "\n".join(list(map(entry_as_string, history)))


def history_as_conversation(history: list[HistoryItem]):
    return "\n".join(list(map(
        lambda message: f"{message.role}: {clear_tags(message.content)}",
        history
    )))


def history_as_dict(history: list[HistoryItem]):
    return list(
        map(
            lambda history_item: {
                "role": history_item.role,
                "content": clear_tags(history_item.content)
            },
            history
        )
    )
