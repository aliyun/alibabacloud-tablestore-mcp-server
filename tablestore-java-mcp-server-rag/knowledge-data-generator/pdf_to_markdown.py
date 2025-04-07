import pdfplumber
from markdownify import markdownify

def pdf_to_markdown(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()

    # 将文本转换为 Markdown 格式
    markdown_content = markdownify(text)
    return markdown_content

pdf_path = "example.pdf"
markdown_result = pdf_to_markdown(pdf_path)
print(markdown_result)