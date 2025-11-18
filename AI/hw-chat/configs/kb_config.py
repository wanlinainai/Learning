
# 数据库连接信息
username='root'
hostname = "192.168.121.129"
database_name = "test"
password = "Zhang123454321."

SQLALCHEMY_DATABASE_URI = f'mysql+asyncmy://{username}:{password}@{hostname}/{database_name}?charset=utf8mb4'


KB_INFO = {
    "知识库名称": "知识库介绍",
    "samples": "关于本项目的ISSUES解答"
}


# 自定义的文本切分器名称
TEXT_SPLITTER_NAME = "ChineseRecursiveTextSplitter"


# 是否开启中文标题增强
ZH_TITLE_ENHANCE = True

CHUNK_SIZE = 250

OVERLAP_SIZE = 50


# 分词器配置项
text_splitter_dict = {
    # Markdown文档的处理
    "MarkdownHeaderTextSplitter": {
        "header_to_split_on": [
            ('#', 'head1'),
            ('##', 'head2'),
            ('###', 'head3'),
            ('####', 'head4'),
        ]
    },
    "ChineseRecursiveTextSplitter": {
        "source": "huggingface",
        "tokenizer_name_or_path": ""
    },
    "SpacyTextSplitter": {
        "source": "huggingface",
        "tokenizer_name_or_path": "gpt3"
    },
    "RecursiveCharacterTextSplitter": {
        "source": "tiktoken",
        "tokenizer_name_or_path": "cl100k_base"
    }
}
