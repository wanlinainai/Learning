from typing import List, Dict

from sqlalchemy import select

from server.db import KnowledgeBaseModel, KnowledgeFileModel
from server.db.models.knowledge_file_model import FileDocModel
from server.db.session import with_async_session
from server.knowledge_base.utils import KnowledgeFile

@with_async_session
async def add_docs_to_db(
        session,
        kb_name: str,
        file_name: str,
        doc_infos: List[Dict]
):
    """
    将知识库的某个文件所有Document信息添加到数据库
    :param session:
    :param kb_name:
    :param file_name:
    :param doc_infos: ["id": str, "metadata": dict, ...]
    :return:
    """
    if doc_infos is None:
        return False
    try:
        for doc_info in doc_infos:
            obj = FileDocModel(
                kb_name=kb_name,
                file_name=file_name,
                doc_id=doc_info['id'],
                meta_data=doc_info['metadata']
            )
            session.add(obj)
        await session.commit()
        print('文档信息成功添加到数据库')
        return True
    except Exception as e:
        print(f'在添加文档信息的时候发生错误： {e}')
        await session.rollback()
        return False


@with_async_session
async def do_add_to_db(
        session,
        kb_file: KnowledgeFile,
        docs_count: int = 0,
        custom_docs: bool = False,
        doc_infos: List[Dict] = []
):
    """
    文件添加到数据库中，如果文件存在，更新文件信息和版本号
    :param session: 数据库会话对象
    :param kb_file: 知识文件对象，包含文件的相关信息
    :param docs_count: 文档的数量
    :param custom_docs: 是否是自定义文档
    :param doc_infos: 文档信息列表：[{"id": str, "metadata": dict}, ...]
    :return:
    """
    print(f'开始查询 KnowledgeBase...')
    stmt = select(KnowledgeBaseModel).where(KnowledgeBaseModel.kb_name == kb_file.kb_name)
    kb_result = await session.execute(stmt)
    kb = kb_result.scalars().first()
    print(f'查询 KnowledgeBase 完成：{kb}')

    if kb:
        print(f'{kb} Knowledge已经存在，开始查询 KnowledgeFile ...')
        stmt = select(KnowledgeFileModel).where(
            KnowledgeFileModel.kb_name.ilike(kb_file.kb_name),
            KnowledgeFileModel.file_name.ilike(kb_file.filename)
        )

        file_result = await session.execute(stmt)
        existing_file = file_result.scalars().first()
        print(f'查询 KnowledgeFile 完成：{existing_file}')

        mtime = kb_file.get_mtime()
        size = kb_file.get_size()
        print(f'获取文件时间和大小： mtime={mtime}，文件大小 size={size}')

        if existing_file:
            print('文件已经存在，更新文件信息...')
            existing_file.file_mtime = mtime
            existing_file.file_size = size
            existing_file.docs_count = docs_count
            existing_file.custom_docs = custom_docs
            existing_file.file_version += 1
            print('文件信息更新成功')
        else:
            print('文件不存在，创建新文件...')
            new_file = KnowledgeFileModel(
                file_name=kb_file.filename,
                file_ext=kb_file.ext,
                kb_name=kb_file.kb_name,
                document_loader_name=kb_file.document_loader_name,
                text_splitter_name=kb_file.text_splitter_name,
                file_mtime=mtime,
                file_size=size,
                docs_count=docs_count,
                custom_docs=custom_docs
            )
            session.add(new_file)
            kb.file_count += 1
            print('新文件添加完成')
        print(' 开始添加文档信息... ')
        await add_docs_to_db(kb_name=kb_file.kb_name, file_name=kb_file.filename, doc_infos=doc_infos)

        print('文档信息添加完成')

        try:
            print('提交事务')
            await session.commit()

        except Exception as e:
            print(f'Error committing changes: {e}')
            await session.rollback()
            print('事务回滚')
            raise
    else:
        print('KnowledgeBase不存在，请检查')
    return True