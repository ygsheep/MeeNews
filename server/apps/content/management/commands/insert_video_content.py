from django.core.management.base import BaseCommand
from apps.content.models import RawNews, VideoContent, NewsCategory
from django.utils import timezone

class Command(BaseCommand):
    help = '批量插入 RawNews + VideoContent 测试数据（视频元数据与视频内容一体化）'

    def handle(self, *args, **options):
        # 获取或创建一个分类
        recommend_category = NewsCategory.objects.get(slug='recommend')
        # 测试数据
        test_data = [
            {
                'title': '原神角色演示：枫原万叶',
                'content': '原神角色演示视频，枫原万叶，风之剑士，潇洒自在。',
                'type': 'video',
                'summary': '原神枫原万叶角色演示，展示其独特技能与风格。',
                'source': '米哈游',
                'source_url': 'https://webstatic.mihoyo.com/upload/contentweb/2022/07/04/1169862f9fa35734b06ce09c96dad9ae_616082062681680005.png',
                'category': recommend_category,
                'published_at': timezone.now(),
                'video_url': 'https://webstatic.mihoyo.com/upload/contentweb/2022/07/01/v2/hk4e/157750/492f5f50c6da93a03bdb4e4025d14a39_747062606835292364.mp4',
                'duration': 247,  # 假设时长为247秒
                'video_quality': '1080p',  # 假设画质为1080p
                # 新增标签，覆盖原有标签，更贴合视频内容
                'tags': ['原神', '角色演示', '枫原万叶', '米哈游', '游戏', '风之剑士', '短剧', '推荐'],
                'keywords': ['原神', '枫原万叶', '角色技能', '游戏演示', '米哈游', '风元素', '角色介绍'],
                'sentiment_score': 0.95,
                'importance_score': 0.98,
                'is_processed': True,
            },
        ]
        created_count = 0
        for data in test_data:
            if not RawNews.objects.filter(source_url=data['source_url']).exists():
                raw_news = RawNews.objects.create(
                    type='video',
                    title=data['title'],
                    content=data['content'],
                    summary=data['summary'],
                    source=data['source'],
                    source_url=data['source_url'],
                    category=data['category'],
                    published_at=data['published_at'],
                    tags=data['tags'],
                    keywords=data['keywords'],
                    is_processed=True,
                    sentiment_score=data.get('sentiment_score'),
                    importance_score=data.get('importance_score'),
                )
                video = VideoContent.objects.create(
                    title=data['title'],
                    description=data['summary'],
                    source=data['source'],
                    source_url=data['source_url'],
                    video_url=data['video_url'],
                    duration=data['duration'],
                    quality_level='high',
                    published_at=data['published_at'],
                    keywords=data['keywords'],
                )
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"已插入视频新闻: {data['title']}"))
            else:
                self.stdout.write(self.style.WARNING(f"已存在: {data['title']}"))
        self.stdout.write(self.style.SUCCESS(f'共插入 {created_count} 条 RawNews + VideoContent 测试数据')) 