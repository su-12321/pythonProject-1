"""
自定义中间件
包含访问统计中间件
"""

import time
from django.utils.deprecation import MiddlewareMixin
from .models import VisitStatistics
from .utils import get_client_ip

class VisitStatisticsMiddleware(MiddlewareMixin):
    """
    访问统计中间件
    记录每个请求的访问信息
    """

    def process_request(self, request):
        """在请求开始时记录时间"""
        request.start_time = time.time()

    def process_response(self, request, response):
        """在响应时记录访问统计"""
        # 排除管理后台和静态文件
        if request.path.startswith('/admin/') or request.path.startswith('/static/'):
            return response

        # 排除API请求（可选）
        if request.path.startswith('/api/'):
            return response

        try:
            # 计算响应时间
            response_time = 0
            if hasattr(request, 'start_time'):
                response_time = time.time() - request.start_time

            # 获取客户端信息
            ip_address = get_client_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT', '')

            # 记录访问统计
            VisitStatistics.objects.create(
                ip_address=ip_address,
                user_agent=user_agent[:500],  # 限制长度
                path=request.path[:500],
                method=request.method,
                status_code=response.status_code,
            )

        except Exception as e:
            # 记录日志但不影响正常请求
            print(f"记录访问统计失败: {e}")

        return response

    def process_exception(self, request, exception):
        """处理异常请求"""
        try:
            ip_address = get_client_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT', '')

            VisitStatistics.objects.create(
                ip_address=ip_address,
                user_agent=user_agent[:500],
                path=request.path[:500],
                method=request.method,
                status_code=500,  # 服务器错误
            )
        except:
            pass

        return None
