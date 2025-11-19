import json
import os
import tempfile
from typing import List

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from rich.progress import Progress, SpinnerColumn, TextColumn
from unstructured.partition.image import partition_image
from unstructured.partition.pdf import partition_pdf


class UnstructuredLightPipeline:
    async def run_pipeline(self,
                           file_path: str,
                           options: List[str] = None,
                           debug: bool = False,
                           local: bool = True):
        print(f'\n 运行pipeline with Langchain \n')

        strategy = 'hi_res'
        model_name = 'yolox'

        extract_tables = False

        if 'tables' in options:
            extract_tables = True

        elements = self.invoke_pipeline_step(
            lambda: self.process_file(file_path, strategy, model_name),
            "文档处理数据",
            local
        )

        if debug:
            new_extension = 'json'
            # 修改文件格式，修改后缀名
            new_file_path = self.change_file_extension(file_path, new_extension)

            documents = self.invoke_pipeline_step(
                lambda: self.load_text_data(elements, new_file_path, extract_tables),
                "Loading text data...",
                local
            )
        else:
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_file_path = os.path.join(temp_dir, 'file_data.json')

                documents = self.invoke_pipeline_step(
                    lambda: self.load_text_data(elements, temp_file_path, extract_tables),
                    'Loading text data...',
                    local
                )

        docs = self.invoke_pipeline_step(
            lambda: self.split_text(documents, chunk_size=20, overlap=50),
            'Splitting text...',
            local
        )

        return docs

    def split_text(self, documents, chunk_size, overlap):
        text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
        docs = text_splitter.split_documents(documents)
        return docs


    def change_file_extension(self, file_path, new_extension):
        if not new_extension.startswith('.'):
            new_extension = '.' + new_extension
        base = file_path.rsplit('.', 1)[0]

        new_file_path = base + new_extension
        return new_file_path

    def load_text_data(self, elements, file_path, extract_tables):
        # 手动将元素保存到JSON中
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump([e.to_dict() for e in elements], file, ensure_ascii=False)

        text_file = self.process_json_file(file_path, extract_tables)

        loader = TextLoader(text_file)
        documents = loader.load()

        return documents


    def process_file(self, file_path: str, strategy: str, model_name: str):
        elements = None
        # 处理pdf文件和图片文件的方式
        if file_path.lower().endswith('.pdf'):
            elements = partition_pdf(
                filename=file_path,
                strategy=strategy,
                model_name=model_name,
                infer_table_structure=True # 处理表格内容，保留HTML样式
            )
        elif file_path.lower().endswith(('.jpg', '.jpeg', '.png')):
            elements = partition_image(
                filename=file_path,
                strategy=strategy,
                infer_table_structure=True, # 保留表格的结构，html格式
                model_name=model_name,
            )
        return elements

    def process_json_file(self, file_path, extract_tables):
        # 处理JSON格式数据
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        extracted_elements = []
        for entry in data:
            if entry['type'] == 'Table':
                extracted_elements.append(entry['metadata']['text_as_html'])
            elif entry['type'] == 'Title' and extract_tables is False:
                extracted_elements.append(entry['text'])
            elif entry['type'] == 'NarrativeText' and extract_tables is False:
                extracted_elements.append(entry['text'])
            elif entry['type'] == 'UncategorizedText' and extract_tables is False:
                extracted_elements.append(entry['text'])

        # 写入txt文档中
        new_extension = 'txt'
        new_file_path = self.change_file_extension(file_path, new_extension)
        with open(new_file_path, 'w') as output_file:
            for element in extracted_elements:
                output_file.write(element + '\n\n')

        return new_file_path



    def invoke_pipeline_step(self, task_call, task_description, local):
        if local:
            with Progress(
                SpinnerColumn(),
                TextColumn('[progress.description]{task.description}'),
                transient=False
            ) as progress:
                progress.add_task(description=task_description, total=None)
                ret = task_call()
        else:
            print(task_description)
            ret=task_call()
        return ret