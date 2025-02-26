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
    """Returns the language associated with the given code. If no match is found, it returns 'English'."""
    return language_mapping.get(language_code, "English")


def combine_documents(docs, document_separator="\n\n"):
    return document_separator.join([doc.page_content for doc in docs])


def clear_tags(message):
    return re.sub(r"(-? ?\[@?.*\]\(.*?\))|}|{", "", message).strip()


def entry_as_string(entry: HistoryItem):
    if entry.role == MessageSenderRole.HUMAN:
        return f"Human: {clear_tags(entry.content)}"
    return f"Assistant: {clear_tags(entry.content)}"


def history_as_text(history: list[HistoryItem]):
    return "\n".join(list(map(entry_as_string, history)))
