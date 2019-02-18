# coding=utf-8


class LogicException(Exception):
    """
        逻辑异常， 弹窗直接显示错误
    """
    def __init__(self, msg):
        if not isinstance(msg, str):
            raise ValueError("LogicException parameter [msg] error")

        self.code = "logic"
        self.msg = msg

        super(LogicException, self).__init__()


class ValidateException(Exception):
    """
        校验异常， 表单提示错误
    """
    def __init__(self):

        self.code = "validate"
        self.msg = dict()

    def add_message(self, key, value):
        """
            添加异常消息
        :param key: 异常键
        :param value: 异常说明
        :return:
        """
        self.msg[key] = value

    def add_field_null(self, key):
        """
            增加字段为空的异常消息
        :param key:
        :return:
        """
        self.msg[key] = 'null'

    def add_fields_null(self, key_list):
        """
            增加多个字段为空的异常消息
        :param key_list:
        :return:
        """
        for key in key_list:
            self.add_field_null(key)

    def is_error(self):
        """
            是否有异常
        :return:
        """
        return bool(self.msg)
