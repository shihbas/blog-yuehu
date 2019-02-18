# coding=utf-8

# 文章列表中显示的默认图片
DEFAULT_ARTICLE_DISPLAY_IMAGE = "https://img.python-dog.com/default/article/1.jpg"

# 文章默认的简介
DEFAULT_ARTICLE_DESCRIPTION = "我觉得不需要简介，因为题目已经能概括它啦🤕"

# 文章无标签的显示
NULL_ARTICLE_TAG_DISPLAY = "😭噢"

## 文章状态
# 上线展示
ARTICLE_STATUS_DISPLAY = 0
# 暂时保存等待上线
ARTICLE_STATUS_WAIT = 1
# 被下线
ARTICLE_STATUS_NO_DISPLAY = 2

ARTICLE_STATUS_CHOICES = (
    (ARTICLE_STATUS_DISPLAY, "线上展示"),
    (ARTICLE_STATUS_WAIT, "暂存不展示"),
    (ARTICLE_STATUS_NO_DISPLAY, "被下线")
)

# 文章文本编辑工具
ARTICLE_EDIT_RICH_TEXT = 0
ARTICLE_EDIT_MARKDOWN = 1
ARTICLE_EDIT_JSON = 2
ARTICLE_EDIT_OTHER = 3


ARTICLE_EDIT_CHOICES = (
    (ARTICLE_EDIT_RICH_TEXT, "富文本"),
    (ARTICLE_EDIT_MARKDOWN, "markdown"),
    (ARTICLE_EDIT_JSON, "json"),
    (ARTICLE_EDIT_OTHER, "其他")
)

# 允许的文本编辑类型
ARTICLE_EDIT_ALLOW_LIST = [ARTICLE_EDIT_RICH_TEXT, ARTICLE_EDIT_MARKDOWN]

# cms个人文章能展示 的 状态列表
CMS_SELF_ARTICLE_SHOW_STATUS_LIST = [ARTICLE_STATUS_DISPLAY, ARTICLE_STATUS_WAIT]
# cms 所有文章能更新的 状态列表
CMS_ALL_ARTICLE_UPDATE_STATUS_LIST = [ARTICLE_STATUS_DISPLAY, ARTICLE_STATUS_WAIT]
# cms 管理员能展示 的 状态列表
CMS_ALL_ARTICLE_SHOW_STATUS_LIST = [ARTICLE_STATUS_DISPLAY, ARTICLE_STATUS_WAIT, ARTICLE_STATUS_NO_DISPLAY]

# 文章评论每页最大数量
ARTICLE_COMMENT_PAGE_SIZE_MAX = 10