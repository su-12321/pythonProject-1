"""
数据库模型
"""

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class Category(models.Model):
    """文章分类"""
    name = models.CharField('分类名称', max_length=100)
    description = models.TextField('描述', blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'
        ordering = ['name']

    def __str__(self):
        return self.name

class Tag(models.Model):
    """文章标签"""
    name = models.CharField('标签名称', max_length=50)
    description = models.TextField('描述', blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'
        ordering = ['name']

    def __str__(self):
        return self.name

class Post(models.Model):
    """博客文章"""
    STATUS_CHOICES = (
        ('draft', '草稿'),
        ('published', '已发布'),
        ('archived', '已归档'),
    )

    title = models.CharField('标题', max_length=200)
    content = models.TextField('内容')
    summary = models.TextField('摘要', max_length=500, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                null=True, blank=True, verbose_name='分类')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='标签')
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='draft')
    cover_image = models.ImageField('封面图片', upload_to='post_covers/', blank=True)
    is_featured = models.BooleanField('是否推荐', default=False)
    view_count = models.PositiveIntegerField('浏览数', default=0)
    created_at = models.DateTimeField('创建时间', default=timezone.now)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def increment_view_count(self):
        """增加浏览数"""
        self.view_count += 1
        self.save(update_fields=['view_count'])

    @property
    def short_content(self):
        """内容预览"""
        return self.content[:200] + '...' if len(self.content) > 200 else self.content

class Comment(models.Model):
    """文章评论"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='文章')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='评论者')
    content = models.TextField('评论内容')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                              related_name='replies', verbose_name='父评论')
    is_active = models.BooleanField('是否显示', default=True)
    created_at = models.DateTimeField('创建时间', default=timezone.now)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.author.username} 评论了 {self.post.title}'

class VisitStatistics(models.Model):
    """访问统计"""
    ip_address = models.GenericIPAddressField('IP地址')
    user_agent = models.TextField('用户代理', blank=True)
    path = models.CharField('访问路径', max_length=500)
    method = models.CharField('请求方法', max_length=10)
    status_code = models.IntegerField('状态码')
    visit_time = models.DateTimeField('访问时间', auto_now_add=True)

    class Meta:
        verbose_name = '访问统计'
        verbose_name_plural = '访问统计'
        ordering = ['-visit_time']

    def __str__(self):
        return f'{self.ip_address} - {self.path}'


# 在 blog/models.py 文件中添加以下模型

class PrivateChatSession(models.Model):
    """私聊会话"""
    user1 = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='chat_sessions_as_user1',
                              verbose_name='用户1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='chat_sessions_as_user2',
                              verbose_name='用户2')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('最后更新时间', auto_now=True)
    is_active = models.BooleanField('是否活跃', default=True)

    class Meta:
        verbose_name = '私聊会话'
        verbose_name_plural = '私聊会话'
        unique_together = ['user1', 'user2']
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user1.username} 和 {self.user2.username} 的聊天"

    def other_user(self, current_user):
        """获取会话中的另一个用户"""
        return self.user2 if current_user == self.user1 else self.user1

    def unread_count_for_user(self, user):
        """获取用户未读消息数"""
        return self.messages.filter(
            receiver=user,
            is_read=False
        ).count()


class PrivateMessage(models.Model):
    """私聊消息"""
    session = models.ForeignKey(PrivateChatSession, on_delete=models.CASCADE,
                                related_name='messages', verbose_name='会话')
    sender = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='sent_private_messages',
                               verbose_name='发送者')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name='received_private_messages',
                                 verbose_name='接收者')
    content = models.TextField('消息内容')
    is_read = models.BooleanField('是否已读', default=False)
    read_at = models.DateTimeField('阅读时间', null=True, blank=True)
    created_at = models.DateTimeField('发送时间', auto_now_add=True)

    class Meta:
        verbose_name = '私聊消息'
        verbose_name_plural = '私聊消息'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['session', 'created_at']),
            models.Index(fields=['sender', 'receiver', 'created_at']),
            models.Index(fields=['receiver', 'is_read']),
        ]

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}: {self.content[:50]}"

    def mark_as_read(self):
        """标记消息为已读"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])