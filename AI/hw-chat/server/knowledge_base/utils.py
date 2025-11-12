import os


def get_kb_path(knowledge_base_name: str):
    return os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), "knowledge_base"), knowledge_base_name)

def get_doc_path(knowledge_base_name: str):
    return os.path.join(get_kb_path(knowledge_base_name), 'content')