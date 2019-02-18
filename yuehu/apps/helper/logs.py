# coding=utf-8

import logging


def get_logger(name, prefix='yuehu'):
    return logging.getLogger('{prefix}.{name}'.format(prefix=prefix, name=name))

visit_article_logger = logging.getLogger('visit_article')

def visit_article_log(user_id, article_id):
    """
        写入访问日志
    :param user_id: 用户ID
    :param article_id: 文章ID
    :return:
    """
    visit_article_logger.info(f'{user_id}-{article_id}')


class ExcludeFilter(logging.Filter):
    def __init__(self, exclude_name='yuehu.actions', exclude_level=logging.ERROR):
        super(ExcludeFilter, self).__init__()
        self.exclude_name = exclude_name
        self.exclude_level = exclude_level

    def filter(self, record):
        if record.name == self.exclude_name:
            return False
        if record.levelno >= self.exclude_level:
            return False
        return True
