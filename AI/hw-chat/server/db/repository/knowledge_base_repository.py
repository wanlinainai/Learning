from sqlalchemy.future import select

from configs.model_config import EMBEDDING_MODEL
from server.db.models.knowledge_base_model import KnowledgeBaseModel
from server.db.session import with_async_session


@with_async_session
async def load_kb_from_db(session, kb_name):
    stmt = select(KnowledgeBaseModel).filter(KnowledgeBaseModel.kb_name.ilike(kb_name))
    result = await session.execute(stmt)
    kb = result.scalar_one_or_none()
    if kb:
        kb_name, vs_type, embed_model = kb.kb_name, kb.vs_type, kb.embed_model
    else:
        kb_name, vs_type, embed_model = None, None, EMBEDDING_MODEL
    return kb_name, vs_type, embed_model


@with_async_session
async def add_kb_to_db(session, kb_name, kb_info, vs_type, embed_model, user_id):
    """
    添加知识库到数据库
    :return:
    """
    kb = await session.execute(
        select(KnowledgeBaseModel)
        .where(KnowledgeBaseModel.kb_name.ilike(kb_name))
    )

    kb = kb.scalars().first()

    if not kb:
        # 创建新的数据库实例
        kb = KnowledgeBaseModel(kb_name=kb_name, kb_info=kb_info, vs_type=vs_type, embed_model=embed_model, user_id=user_id)
        session.add(kb)
    else:
        # 更新现有的知识库实例
        kb.kb_info = kb_info
        kb.vs_type = vs_type
        kb.embed_model = embed_model
        kb.user_id = user_id
    # 异步提交数据库事务
    await session.commit()
    return True