import argparse
import html
import json
import os
import re
import shutil
import subprocess
import sys
from concurrent.futures.thread import ThreadPoolExecutor
from multiprocessing import Pool
from pathlib import Path

import spacy
from nltk.corpus.reader import documents
from tqdm import tqdm


def load_corpus(dir_path):
    keywords = [
        '智能教育',
        '大模型',
        'Langchain',
        '机器学习',
        '深度学习',
        'Java',
        '自然语言处理',
        'Python',
        '人工智能',
        'AI',
        'AI骗局'
    ]

    def iter_files(dir_path):
        if os.path.isfile(dir_path):
            yield dir_path
        elif os.path.isdir(dir_path):
            for dirpath, _, filenames in os.walk(dir_path):
                for f in filenames:
                    yield os.path.join(dirpath, f)
        else:
            raise RuntimeError(f'Path {dir_path} is invalid!')

    def read_jsonl_file(file):
        """ 读取.jsonl文件的行，将相关数据添加到语料库中 """
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                json_data = json.loads(line)
                if any(keyword in json_data['text'] for keyword in keywords):
                    corpus.append(json_data)

                    # 如果语料库超过100，不再添加
                    if len(corpus) >= 100:
                        break;


    all_files = [file for file in iter_files(dir_path)]

    # 初始化语料库列表
    corpus = []
    with ThreadPoolExecutor(max_workers=args.num_workers) as executor:
        for file in all_files:
            executor.submit(read_jsonl_file, file)

    return corpus

def basic_process(title, text):
    """ 对每一个 """
    title = html.unescape(title)
    text = html.unescape(text)

    # 删除文本首尾的空白字符
    text = text.strip()

    # # 如果标题含有特定的消歧义标记，则不处理这类页面
    if '(disambiguation)' in title.lower():
        return None, None
    if '(disambiguation page)' in title.lower():
        return None, None

    # 排除以列表、索引或大纲开头的页面，这些页面大多只包含链接
    if re.match(r'(List of .+)|(Index of .+)|(Outline of .+)',
                title):
        return None, None

    # 排除重定向页面
    if text.startswith("REDIRECT") or text.startswith("redirect"):
        return None, None

    # 如果文本以 ". References." 结尾，则删除该部分
    if text.endswith(". References."):
        text = text[:-len(" References.")].strip()

    # 删除文本中的特定格式标记，如引用标记
    text = re.sub('\{\{cite .*?\}\}', ' ', text, flags=re.DOTALL)

    # 替换或删除不必要的格式和标签
    text = text.replace(r"TABLETOREPLACE", " ")
    text = text.replace(r"'''", " ")
    text = text.replace(r"[[", " ")
    text = text.replace(r"]]", " ")
    text = text.replace(r"{{", " ")
    text = text.replace(r"}}", " ")
    text = text.replace("<br>", " ")
    text = text.replace("&quot;", "\"")
    text = text.replace("&amp;", "&")
    text = text.replace("& amp;", "&")
    text = text.replace("nbsp;", " ")
    text = text.replace("formatnum:", "")

    # 删除特定HTML标签内的文本，如<math>, <chem>, <score>
    text = re.sub('<math.*?</math>', '', text, flags=re.DOTALL)
    text = re.sub('<chem.*?</chem>', '', text, flags=re.DOTALL)
    text = re.sub('<score.*?</score>', '', text, flags=re.DOTALL)

    # 使用正则表达式删除样式相关的属性，例如：item_style, col_style等
    text = re.sub('\| ?item[0-9]?_?style= ?.*? ', ' ', text)
    text = re.sub('\| ?col[0-9]?_?style= ?.*? ', ' ', text)
    text = re.sub('\| ?row[0-9]?_?style= ?.*? ', ' ', text)
    text = re.sub('\| ?style= ?.*? ', ' ', text)
    text = re.sub('\| ?bodystyle= ?.*? ', ' ', text)
    text = re.sub('\| ?frame_?style= ?.*? ', ' ', text)
    text = re.sub('\| ?data_?style= ?.*? ', ' ', text)
    text = re.sub('\| ?label_?style= ?.*? ', ' ', text)
    text = re.sub('\| ?headerstyle= ?.*? ', ' ', text)
    text = re.sub('\| ?list_?style= ?.*? ', ' ', text)
    text = re.sub('\| ?title_?style= ?.*? ', ' ', text)
    text = re.sub('\| ?ul_?style= ?.*? ', ' ', text)
    text = re.sub('\| ?li_?style= ?.*? ', ' ', text)
    text = re.sub('\| ?border-style= ?.*? ', ' ', text)
    text = re.sub('\|? ?style=\".*?\"', '', text)
    text = re.sub('\|? ?rowspan=\".*?\"', '', text)
    text = re.sub('\|? ?colspan=\".*?\"', '', text)
    text = re.sub('\|? ?scope=\".*?\"', '', text)
    text = re.sub('\|? ?align=\".*?\"', '', text)
    text = re.sub('\|? ?valign=\".*?\"', '', text)
    text = re.sub('\|? ?lang=\".*?\"', '', text)
    text = re.sub('\|? ?bgcolor=\".*?\"', '', text)
    text = re.sub('\|? ?bg=\#[a-z]+', '', text)
    text = re.sub('\|? ?width=\".*?\"', '', text)
    text = re.sub('\|? ?height=[0-9]+', '', text)
    text = re.sub('\|? ?width=[0-9]+', '', text)
    text = re.sub('\|? ?rowspan=[0-9]+', '', text)
    text = re.sub('\|? ?colspan=[0-9]+', '', text)
    text = re.sub(r'[\n\t]', ' ', text)
    text = re.sub('<.*?/>', '', text)
    text = re.sub('\|? ?align=[a-z]+', '', text)
    text = re.sub('\|? ?valign=[a-z]+', '', text)
    text = re.sub('\|? ?scope=[a-z]+', '', text)
    text = re.sub('&lt;ref&gt;.*?&lt;/ref&gt;', ' ', text)
    text = re.sub('&lt;.*?&gt;', ' ', text)
    text = re.sub('File:[A-Za-z0-9 ]+\.[a-z]{3,4}(\|[0-9]+px)?', '', text)
    text = re.sub('Source: \[.*?\]', '', text)

    # 清理可能因XML导出错误而残留的格式标签
    # 使用正则表达式匹配并替换各种样式相关的属性
    text = text.replace("Country flag|", "country:")
    text = text.replace("flag|", "country:")
    text = text.replace("flagicon|", "country:")
    text = text.replace("flagcountry|", "country:")
    text = text.replace("Flagu|", "country:")
    text = text.replace("display=inline", "")
    text = text.replace("display=it", "")
    text = text.replace("abbr=on", "")
    text = text.replace("disp=table", "")

    title = title.replace("\n", " ").replace("\t", " ")

    return title, text

def single_worker(docs):
    """处理一个文档列表，对每一个文档应用清洗和格式化操作"""
    results = []
    for item in tqdm(docs):
        # 应用基础处理函数 basic_process 来处理问个文档的标题和文本
        title, text = basic_process(item[0], item[1])
        if title is None:
            continue
        title = f"\"{title}\""
        results.append((title, text))
    return results

def split_list(list, n):
    """ 将一个列表切割成 n 个大致相等的部分 """
    k, m = divmod(len(list), n)
    return [list[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]

if __name__ == '__main__':
    sys.argv = [
        'preprocess_wiki',
        '--dump_path',
        '/Users/a1234/Downloads/hw-chat-0.2/knowledge_base/wiki/wiki_data/zhwiki-latest-stub-articles1.xml.gz',
        '--save_path',
        '/Users/a1234/github_repository/Learning/AI/hw-chat/knowledge_base/wiki/data.jsonl'
    ]
    parser = argparse.ArgumentParser(description='Generate clean wiki corpus file for indexing.')
    parser.add_argument('--dump_path', type=str)
    parser.add_argument('--seg_size', default=None, type=int)
    parser.add_argument("--stride", default=None, type=int)
    parser.add_argument('--num_workers', default=4, type=int)
    parser.add_argument('--save_path', type=str, default='clean_corpus.jsonl')
    args = parser.parse_args()

    # 设置Wikis数据临时存储目录
    temp_dir = os.path.join(Path(args.save_path).parent, 'temp')
    os.makedirs(temp_dir, exist_ok=True)
    # 使用wikiextractor从维基百科中提取文本，输出JSON格式，过滤歧义页面
    subprocess.run(['python', '-m',
                    'wikiextractor.WikiExtractor',
                    '--json', '--filter_disambig_pages', '--quiet',
                    '-o', temp_dir,
                    '--process', str(args.num_workers),
                    args.dump_path])

    # 加载处理之后的语料库
    corpus = load_corpus(temp_dir)
    # 加载spacy语料库
    nlp = spacy.load('zh_core_web_lg')
    # 初始化一个字典来存储文档，避免页面重复
    documents = {}
    # 显示进度条
    for item in tqdm(corpus):
        title = item['title']
        text = item['text']

        # 如果已经存在标题，追加该标题的内容文本
        if title in documents:
            documents[title] += " " + text
        else:
            documents[title] = text
    # 开始预处理文本
    print(f'Start pre-processing...')
    documents = list(documents.items())
    # 线程池进行并行处理
    with Pool(processes=args.num_workers) as p:
        result_list = list(tqdm(p.imap(single_worker, split_list(documents, args.num_workers))))
    result_list = sum(result_list, [])

    all_title = [item[0] for item in result_list]
    all_text = [item[1] for item in result_list]

    print(f'Start chunking...')
    idx = 0
    clean_corpus = []
    # 使用spacy的pipe方法进行高效的文本处理，指定进程数和批处理大小
    for doc in tqdm(nlp.pipe(all_text, n_process=args.num_workers, batch_size=10), total=len(all_text)):
        title = all_title[idx]
        idx += 1
        # 初始化段落列表
        segments = []
        # 初始化单词计数器
        word_count = 0
        # 初始化段落的token列表
        segment_tokens = []
        # 遍历文档中的每个token
        for token in doc:
            # token（包括空格）添加到段落令牌列表
            segment_tokens.append(token.text_with_ws)
            # 如果令牌不是空格也不是标点
            if not token.is_space and not token.is_punct:
                # 单词计数加一
                word_count += 1
                # 如果单词计数达到100，则重置计数器，生成一个新段落
                if word_count == 100:
                    word_count = 0
                    segments.append(''.join([token for token in segment_tokens]))
                    segment_tokens = []
        # 检查最后是否还有剩余的单词没有形成完整段落
        if word_count != 0:
            for token in doc:
                segment_tokens.append(token.text_with_ws)
                if not token.is_space and not token.is_punct:
                    word_count += 1
                    if word_count == 100:
                        word_count = 0
                        segments.append(''.join([token for token in segment_tokens]))
                        break
        # 检查最后一组token是否已添加到segments
        if word_count != 0:
            segments.append(''.join([token for token in segment_tokens]))

        for segment in segments:
            text = segment.replace("\n", " ").replace("\t", " ")
            # 将处理后的标题和文本以字典形式添加到清洗后的语料库列表
            clean_corpus.append({"title": title, "text": text})

    # 删除临时目录以及文件
    shutil.rmtree(temp_dir)
    # 检查保存路径的目录是否存在，不存在就创建
    os.makedirs(os.path.dirname(args.save_path), exist_ok=True)
    # JSON写入文件
    with open(args.save_path, 'w', encoding='utf-8') as f:
        for idx, item in enumerate(clean_corpus):
            json_string = json.dumps({
                'id': idx,
                'title': item['title'],
                'contents': item['text']
            }, ensure_ascii=False)

            f.write(json_string + '\n')

    print('Finish')