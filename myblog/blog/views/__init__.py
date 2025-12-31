"""
视图导出文件
将所有视图函数导出，方便导入使用
"""

from .core import (
    home_view,
    post_detail_view,
    post_create_view,
    post_edit_view,
    post_delete_view,
    my_posts_view,
    category_posts_view,
    tag_posts_view
)

from .auth import (
    register_view,
    login_view,
    logout_view,
    profile_view
)

from .stats import (
    statistics_view,
    api_visit_stats
)

from .chat import (
    chat_view,
    chat_messages_api,
    send_message_api
)

from .private_chat import (
    private_chat_list_view,
    private_chat_detail_view,
    start_private_chat_view,
    api_private_messages,
    api_send_private_message,
    api_private_chat_summary,
    api_mark_all_as_read,
)

__all__ = [
    # 核心视图
    'home_view',
    'post_detail_view',
    'post_create_view',
    'post_edit_view',
    'post_delete_view',
    'my_posts_view',
    'category_posts_view',
    'tag_posts_view',

    # 认证视图
    'register_view',
    'login_view',
    'logout_view',
    'profile_view',

    # 统计视图
    'statistics_view',
    'api_visit_stats',

    # 聊天视图
    'chat_view',
    'chat_messages_api',
    'send_message_api',
    # 私聊视图
    'private_chat_list_view',
    'private_chat_detail_view',
    'start_private_chat_view',
    'api_private_messages',
    'api_send_private_message',
    'api_private_chat_summary',
    'api_mark_all_as_read',
]
