"""
聊天功能视图
处理实时聊天功能
"""

import json
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_datetime
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import timedelta

# 简单的内存存储（生产环境应使用数据库或Redis）
chat_messages = []
MAX_MESSAGES = 60  # 最大消息存储数

@login_required
def chat_view(request):
    """
    聊天室视图
    """
    # 获取在线用户（简化版）
    active_users = []

    context = {
        'active_users': active_users,
    }

    return render(request, 'blog/chat.html', context)

def chat_messages_api(request):
    """
    API: 获取聊天消息
    """
    # 清理旧消息（超过1小时）
    global chat_messages
    one_hour_ago = timezone.now() - timedelta(hours=1)
    chat_messages = [
        msg for msg in chat_messages
        if parse_datetime(msg.get('timestamp', timezone.now().isoformat())) > one_hour_ago
    ]

    return JsonResponse({
        'messages': chat_messages[-50:],  # 返回最近50条消息
        'count': len(chat_messages),
    })

@csrf_exempt
@login_required
def send_message_api(request):
    """
    API: 发送聊天消息
    """
    if request.method != 'POST':
        return JsonResponse({'error': '只支持POST请求'}, status=400)

    try:
        data = json.loads(request.body)
        message_content = data.get('message', '').strip()

        if not message_content:
            return JsonResponse({'error': '消息内容不能为空'}, status=400)

        # 创建消息对象
        message = {
            'id': len(chat_messages) + 1,
            'user_id': request.user.id,
            'username': request.user.username,
            'avatar': '',  # 可以添加头像URL
            'content': message_content,
            'timestamp': timezone.now().isoformat(),
        }

        # 添加消息到存储
        chat_messages.append(message)

        # 限制消息数量
        if len(chat_messages) > MAX_MESSAGES:
            chat_messages.pop(0)

        return JsonResponse({
            'success': True,
            'message': message,
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': '无效的JSON数据'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
