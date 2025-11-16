import PyPDF2


def extract_text_from_pdf(filename: str, page_num: int):
    """
    使用pypdf解析PDF文件
    :param filename:
    :param page_num:
    :return:
    """
    try:
        with open(filename, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            if page_num < len(reader.pages):
                page = reader.pages[page_num]
                text = page.extract_text()
                if text:
                    return text
                else:
                    return "No text found on this page"
            else:
                return f'Page number {page_num} is out of range, The document has {len(reader.pages)} pages'
    except Exception as e:
        return f'Erorr ! {str(e)}'


if __name__ == '__main__':
    filename = '/Users/a1234/Downloads/hw-chat-0.2/data/parse/data/1706.03762v7.pdf'
    page_num = 5
    text = extract_text_from_pdf(filename, page_num)

    print(f'Text from file {filename} on page {page_num}')
    print(text if text else 'No text available on the selected page.')
