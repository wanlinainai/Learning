import re

from langchain.docstore.document import Document
from unstructured.partition.text_type import under_non_alpha_ratio


def is_possible_title(
        text: str,
        title_max_word_length: int = 20,
        non_alpha_threshold: float = 0.5
) -> bool:
    """
    检查文本的内容是否有可能是标题
    :param text: 文本内容
    :param title_max_word_length: 一个标题中可能的最大长度
    :param non_alpha_threshold:  文本中作为标题所需要的最小标题数
    :return:
    """
    if len(text) == 0:
        print('Absolutely not title, text is empty.')
        return False
    # 如果文本中包含标题，不是title
    ENDS_IN_PUNCT_PATTERN = r"[^\w\s]\Z"
    ENDS_IN_PUNCT_RE = re.compile(ENDS_IN_PUNCT_PATTERN)
    if ENDS_IN_PUNCT_RE.search(text) is not None:
        return False

    # 文本的长度不能超过20
    if len(text) > title_max_word_length:
        return False

    # 文本中的数字占比不能太高
    if under_non_alpha_ratio(text, threshold=non_alpha_threshold):
        return False

    if text.isnumeric():
        print(f'Not a title, Text is all numeric: \n\n{text}')
        return False

    if len(text) < 5:
        text_5 = text
    else:
        text_5 = text[:5]
    alpha_in_text_5 = sum(list(map(lambda x : x.isnumeric(), list(text_5))))
    if not alpha_in_text_5:
        return False

    return True


def func_zh_title_enhance(docs: Document) -> Document:
    """
    增强中文文档标题识别
    :param docs:
    :return:
    """
    title = None
    if len(docs) > 0:
        for doc in docs:
            if is_possible_title(doc.page_content):
                doc.metadata['category'] = 'cn_Title'
                title = doc.page_content
            elif title:
                doc.page_content = f'下文与({title}) 有关。 {doc.page_content}'
        return docs
    else:
        print('文件不存在！')


if __name__ == '__main__':
    mock_docs = [
        # --- 这是一个标题 (符合长度<20, 且包含数字 '1') ---
        Document(page_content="第1章 Python基础", metadata={"source": "doc1"}),

        # --- 这是属于上面标题的内容 ---
        Document(page_content="Python 是一种解释型语言，语法简洁。", metadata={"source": "doc1"}),
        Document(page_content="它非常适合人工智能和数据分析。", metadata={"source": "doc1"}),

        # --- 这是一个新标题 (符合条件) ---
        Document(page_content="2. 环境搭建指南", metadata={"source": "doc1"}),

        # --- 这是属于新标题的内容 ---
        Document(page_content="首先需要安装 Anaconda 或者 Miniconda。", metadata={"source": "doc1"}),

        # --- 这是一个纯文本标题 (注意：根据你现有逻辑，这可能无法被识别为标题，见下文解释) ---
        Document(page_content="常见问题汇总", metadata={"source": "doc1"}),
        Document(page_content="如果遇到报错，请检查路径设置。", metadata={"source": "doc1"}),
    ]
    print(f'处理前---- （原始文档数：{len(mock_docs)}） ----')
    for i, doc in enumerate(mock_docs):
        print(f'[{i}] {doc.page_content}')

    enhanced_docs = func_zh_title_enhance(mock_docs)
    print('\n' + '='*50 + "\n")
    print(f'处理后---- （增强文档内容） ----')

    if enhanced_docs:
        for i, doc in enumerate(enhanced_docs):
            category = doc.metadata.get('category', '正文')
            print(f'[{i}] [{category}] {doc.page_content}')
    else:
        print('无文档返回')