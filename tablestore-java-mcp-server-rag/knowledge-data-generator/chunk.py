from markdown_it import MarkdownIt

def parse_markdown_to_ast(markdown_text):
    md = MarkdownIt()
    tokens = md.parse(markdown_text)
    return tokens, md

def get_token_text(token):
    if token.type == "inline":
        return "".join(child.content for child in token.children if hasattr(child, "content"))
    elif token.type in ["paragraph_open", "paragraph_close"]:
        return ""
    else:
        return token.content or ""

def split_ast_by_size(tokens, max_size):
    chunks = []
    current_chunk = []
    current_size = 0

    for token in tokens:
        token_text = get_token_text(token)
        token_size = len(token_text)

        if current_size + token_size > max_size and current_chunk:
            chunks.append(current_chunk)
            current_chunk = []
            current_size = 0

        current_chunk.append(token)
        current_size += token_size

    if current_chunk:
        chunks.append(current_chunk)

    return chunks

def tokens_to_markdown(tokens, md):
    return md.renderer.render(tokens, md.options, {})

def process_markdown(markdown_text, max_size):
    tokens, md = parse_markdown_to_ast(markdown_text)
    chunks = split_ast_by_size(tokens, max_size)
    return [tokens_to_markdown(chunk, md) for chunk in chunks]

def to_chunks(markdown_text, max_size):
    chunks = process_markdown(markdown_text, max_size)
    return chunks