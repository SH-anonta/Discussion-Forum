from markdown2 import markdown

class MarkdownToHtmlConverter:
    @classmethod
    def convert(cls, markdown_text):
        return markdown(markdown_text)