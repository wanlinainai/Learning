import json
import os
import tempfile

from bs4 import BeautifulSoup
from rich.progress import SpinnerColumn, Progress, TextColumn
from unstructured.partition.image import partition_image
from unstructured.partition.pdf import partition_pdf


class UnstructuredProcessor(object):
    def __init__(self):
        pass
    def extract_data(self, file_path, strategy, model_name, options, local=True, debug=False):
        """
        指定文件读取数据
        :param file_path: 文件的路径，指定要处理的文件
        :param strategy: 使用什么策略来提取数据
        :param model_name: 使用的模型名称，此处使用的是 yolox
        :param options: dict，额外的选项和参数，用来干预数据提取的过程和结果
        :param local: 是否在本地执行
        :param debug: 如果设置成True，会显示更多的调试信息
        :return:
        """
        elements = self.invoke_pipeline_step(
            lambda: self.process_file(file_path, strategy, model_name),
            "文档提取元素...",
            local
        )

        if debug:
            new_extension = 'json'
            new_file_path = self.change_file_extension(file_path, new_extension)

            content, table_content = self.invoke_pipeline_step(
                lambda: self.load_text_data(elements, new_file_path, options),
                'Loading text data...',
                local
            )

        else :
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_file_path = os.path.join(temp_dir, 'file_data.json')

                content, table_content = self.invoke_pipeline_step(
                    lambda: self.load_text_data(elements, temp_file_path, options),
                    'Loading text data...',
                    local
                )

        if debug:
            print('数据提取')
            print(content)
            print('表格数据提取')
            if table_content:
                print(table_content)
            print(f'table content length: {len(table_content)}')
        return content, table_content

    def load_text_data(self, elements, file_path, options):
        """
        将元素保存到 JSON 文件中，确保使用 ensure_ascii = False
        :param elements:
        :param file_path:
        :param options:
        :return:
        """
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump([e.to_dict() for e in elements], file, ensure_ascii=False)

        content, table_content = None, None
        if options is None:
            content = self.process_json_file(file_path)

        if options and 'tables' in options and 'unstructured' in options:
            content = self.process_json_file(file_path=file_path, option='form')
            table_content = self.process_json_file(file_path, 'table')

        return content, table_content

    def process_json_file(self, file_path, option = None):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

            extracted_elements = []
            for entry in data:
                if entry['type'] == 'Table' and (option is None or option == 'table' or option == 'form'):
                    table_data = entry['metadata']['text_as_html']
                    if option == 'table' and self.table_has_header(table_data):
                        extracted_elements.append(table_data)
                    if option is None or option == 'form':
                        extracted_elements.append(table_data)

                elif entry['type'] == 'Title' and (option is None or option == 'form'):
                    extracted_elements.append(entry['text'])

                elif entry['type'] == 'NarrativeText' and (option is None or option == 'form'):
                    extracted_elements.append(entry['text'])

                elif entry['type'] == 'UncategorizedText' and (option is None or option == 'form'):
                    extracted_elements.append(entry['text'])
                elif entry['type'] == 'Image' and (option is None or option == 'form'):
                    extracted_elements.append(entry['text'])

            if option is None or option == 'form':
                extracted_elements = '\n\n'.join(extracted_elements)
                return extracted_elements

            return extracted_elements


    def table_has_header(self, table_data):
        soup = BeautifulSoup(table_data, 'html.parser')
        table = soup.find('table')

        if table.find('thread'):
            return True

        if table.find_all('th'):
            return True

        return False

    def invoke_pipeline_step(self, task_call, task_description, local):
        """
        执行管道步骤，可以在本地或非本地运行
        :param task_call:  执行的方法
        :param task_description:  任务描述
        :param local: 是否在本地运行，是则显示进度条，否则打印信息
        :return:
        """
        if local:
            with Progress(
                SpinnerColumn(),
                TextColumn(f'[progress.description]{task_description}'),
                transient=False
            ) as progress:
                # 添加进度任务
                progress.add_task(description=task_description, total=None)
                ret = task_call()
        else:
            print(task_description)
            ret = task_call()
        return ret

    def process_file(self, file_path, strategy, model_name):
        """
        处理文件并提取数据，支持PDF文件和图像文件
        :param file_path:
        :param strategy:
        :param model_name:
        :return:
        """
        elements = None
        if file_path.lower().endswith('.pdf'):
            # hi_res搭配 infer_table_structure 处理表格效果比较好
            elements = partition_pdf(
                filename=file_path,
                # strategy控制PDF解析方法：”auto“、"hi_res"、"ocr_only"、"fast"
                strategy=strategy,
                infer_table_structure=True,
                hi_res_model_name=model_name,
                languages=['chi_sim']
            )
        elif file_path.lower().endswith(('.jpg', '.jpeg', '.png')):
            elements = partition_image(
                filename=file_path,
                strategy=strategy,
                infer_table_structure=True,
                hi_res_model_name=model_name,
                languages=['chi_sim']
            )
        return elements

    def change_file_extension(self, file_path, new_extension, suffix = None):
        """
        :param file_path:
        :param new_extension:
        :return:
        """
        if not new_extension.startswith('.'):
            new_extension = '.' + new_extension

        base = file_path.rsplit('.', 1)[0]

        if suffix is None:
            new_file_path = base + new_extension
        else:
            new_file_path = base + '_' + suffix + new_extension

        return new_file_path

if __name__ == '__main__':
    processor = UnstructuredProcessor()

    # 提取PDF中的数据
    content, table_content = processor.extract_data(
        '/Users/a1234/Downloads/hw-chat-0.2/data/parse/data/invoice_2.pdf',
        'hi_res',
        'yolox',
        ['tables', 'unstructured'],
        True,
        True
    )
