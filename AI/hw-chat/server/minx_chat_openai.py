import logging
from typing import Tuple

import tiktoken

logger = logging.getLogger(__name__)

class MinxChatOpenAI:


    @staticmethod
    def get_encoding_model(self) -> Tuple[str, "tiktoken.Encoding"]:
        tiktoken_= tiktoken
        if self.tiktoken_model_name is not None:
            model = self.tiktoken_model_name
        else:
            model = self.model_name
            if model == 'gpt-4':
                model = 'gpt-4-0314'
        try:
            encoding = tiktoken_.encoding_for_model(model)
        except Exception as e:
            logger.warning(f'Warning: model not found. Using other encoding.')
            model = "cl100k_base"
            encoding = tiktoken_.get_encoding(model)

        return model, encoding