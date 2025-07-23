from django.core.management.base import BaseCommand
from apps.content.models import RawNews, NewsCategory, ContentTag, ContentTagRelation, ContentModeration, ContentInteractionStats, Article, VideoContent, AudioContent, UserContentInteraction

class Command(BaseCommand):
    help = '一键清空所有内容相关表数据（危险操作！仅用于开发/测试环境）'

    def handle(self, *args, **options):
        # 先删依赖表，后删主表，避免外键约束错误
        models = [
            VideoContent, AudioContent,  # 先删依赖 RawNews 的内容表
            RawNews, NewsCategory, ContentTag, ContentTagRelation, ContentModeration,
            ContentInteractionStats, Article, UserContentInteraction
        ]
        for model in models:
            count = model.objects.all().count()
            model.objects.all().delete()
            self.stdout.write(self.style.WARNING(f'{model.__name__} 已删除 {count} 条记录'))
        self.stdout.write(self.style.SUCCESS('所有内容相关表数据已清空！')) 