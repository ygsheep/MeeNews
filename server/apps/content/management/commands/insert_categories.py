from django.core.management.base import BaseCommand
from apps.content.models import NewsCategory
from django.utils.text import slugify

class Command(BaseCommand):
    help = '批量插入演示分类数据（关注、推荐、资讯）'

    def handle(self, *args, **options):
        categories = [
            {'name': '关注', 'name_en': 'Follow', 'description': '你关注的内容', 'color_code': '#007AFF'},
            {'name': '推荐', 'name_en': 'Recommend', 'description': '为你推荐的内容', 'color_code': '#4CD964'},
            {'name': '资讯', 'name_en': 'News', 'description': '最新资讯', 'color_code': '#FF9500'},
        ]
        for cat in categories:
            slug = slugify(cat['name_en'] or cat['name'])
            cat['slug'] = slug
            obj, created = NewsCategory.objects.get_or_create(slug=slug, defaults=cat)
            if created:
                self.stdout.write(self.style.SUCCESS(f"已添加分类: {cat['name']}"))
            else:
                self.stdout.write(self.style.WARNING(f"分类已存在: {cat['name']}"))
        self.stdout.write(self.style.SUCCESS('分类数据插入完成')) 