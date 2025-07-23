from django.core.management.base import BaseCommand
from apps.content.models import RawNews, NewsCategory
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = '插入测试新闻数据用于推荐功能测试'

    def handle(self, *args, **options):
        # 获取分类（用slug唯一查找，避免name重复报错）
        try:
            recommend_category = NewsCategory.objects.get(slug='recommend')
            news_category = NewsCategory.objects.get(slug='news')
            follow_category = NewsCategory.objects.get(slug='follow')
        except NewsCategory.DoesNotExist:
            self.stdout.write(self.style.ERROR('请先运行 python manage.py insert_categories 创建分类'))
            return

        # 测试新闻数据
        test_news = [
            {
                'title': 'AI驱动的新闻推荐系统正式上线',
                'content': '羊咩快报平台今日正式发布AI驱动的新闻推荐系统，该系统采用最新的机器学习算法，能够根据用户的阅读习惯和兴趣偏好，为用户提供个性化的资讯推荐服务。系统上线后，用户满意度提升了35%，阅读时长平均增加了40%。',
                'summary': 'AI推荐系统助力个性化资讯推送，用户满意度大幅提升',
                'source': '羊咩快报',
                'source_url': 'https://yangmie.com/news/ai-recommendation-launch',
                'category': recommend_category,
                'tags': ['AI', '推荐算法', '个性化', '用户体验'],
                'keywords': ['人工智能', '机器学习', '推荐系统', '个性化服务'],
                'sentiment_score': 0.95,
                'importance_score': 0.98,
                'is_processed': True,
                'published_at': datetime.now() - timedelta(hours=2)
            },
            {
                'title': 'OpenAI发布GPT-5预览版，性能提升显著',
                'content': 'OpenAI今日发布了GPT-5的预览版本，新模型在多个基准测试中表现优异。相比GPT-4，GPT-5在推理能力、代码生成、多模态理解等方面都有显著提升。该模型预计将在下个月正式发布。',
                'summary': 'GPT-5预览版发布，AI能力再上新台阶',
                'source': '科技前沿',
                'source_url': 'https://tech.com/news/gpt5-preview',
                'category': news_category,
                'tags': ['OpenAI', 'GPT-5', 'AI模型', '技术突破'],
                'keywords': ['人工智能', '大语言模型', 'GPT-5', '技术发展'],
                'sentiment_score': 0.92,
                'importance_score': 0.96,
                'is_processed': True,
                'published_at': datetime.now() - timedelta(hours=4)
            },
            {
                'title': '新能源汽车市场持续增长，比亚迪领跑销量榜',
                'content': '根据最新数据显示，2025年第一季度新能源汽车销量同比增长45%，比亚迪以28%的市场份额继续领跑。特斯拉、蔚来、小鹏等品牌也表现强劲，市场竞争日趋激烈。',
                'summary': '新能源汽车市场火爆，比亚迪稳居销量榜首',
                'source': '财经日报',
                'source_url': 'https://finance.com/news/ev-market-growth',
                'category': news_category,
                'tags': ['新能源汽车', '比亚迪', '市场分析', '销量数据'],
                'keywords': ['电动汽车', '市场趋势', '销量统计', '行业分析'],
                'sentiment_score': 0.88,
                'importance_score': 0.85,
                'is_processed': True,
                'published_at': datetime.now() - timedelta(hours=6)
            },
            {
                'title': '世界杯预选赛：中国队2-1战胜韩国队',
                'content': '在昨晚进行的世界杯预选赛中，中国队以2-1的比分战胜韩国队，取得了关键的三分。武磊在第35分钟和第78分钟分别进球，帮助球队取得胜利。这场胜利为中国队晋级世界杯决赛圈增添了希望。',
                'summary': '国足2-1胜韩国，世界杯出线希望大增',
                'source': '体育快报',
                'source_url': 'https://sports.com/news/china-korea-match',
                'category': news_category,
                'tags': ['足球', '世界杯', '中国队', '武磊'],
                'keywords': ['足球比赛', '世界杯预选赛', '国家队', '体育新闻'],
                'sentiment_score': 0.98,
                'importance_score': 0.92,
                'is_processed': True,
                'published_at': datetime.now() - timedelta(hours=8)
            },
            {
                'title': '元宇宙概念股大涨，投资者热情高涨',
                'content': '受Facebook母公司Meta发布新一代VR设备影响，元宇宙概念股今日集体大涨。多家相关公司股价涨幅超过10%，投资者对元宇宙未来发展前景持乐观态度。',
                'summary': '元宇宙概念股集体大涨，投资者看好未来发展',
                'source': '投资时报',
                'source_url': 'https://investment.com/news/metaverse-stocks',
                'category': news_category,
                'tags': ['元宇宙', '股票', '投资', 'VR设备'],
                'keywords': ['虚拟现实', '股票市场', '投资机会', '科技股'],
                'sentiment_score': 0.75,
                'importance_score': 0.78,
                'is_processed': True,
                'published_at': datetime.now() - timedelta(hours=10)
            },
            {
                'title': '5G网络覆盖率达到85%，用户体验显著提升',
                'content': '据工信部最新统计，全国5G网络覆盖率已达到85%，用户平均下载速度提升至500Mbps。5G技术的普及为智慧城市、自动驾驶、远程医疗等应用提供了强有力的网络支撑。',
                'summary': '5G网络覆盖率超85%，用户体验大幅提升',
                'source': '通信科技',
                'source_url': 'https://telecom.com/news/5g-coverage-85',
                'category': recommend_category,
                'tags': ['5G', '网络技术', '通信', '智慧城市'],
                'keywords': ['5G网络', '网络覆盖', '通信技术', '数字化转型'],
                'sentiment_score': 0.90,
                'importance_score': 0.87,
                'is_processed': True,
                'published_at': datetime.now() - timedelta(hours=12)
            },
            {
                'title': '环保新政策出台，绿色能源发展加速',
                'content': '国家发改委今日发布新的环保政策，加大对绿色能源项目的支持力度。政策包括税收优惠、补贴支持等措施，预计将推动太阳能、风能等清洁能源快速发展。',
                'summary': '环保新政策助力绿色能源发展，清洁能源前景广阔',
                'source': '环保日报',
                'source_url': 'https://environment.com/news/green-energy-policy',
                'category': follow_category,
                'tags': ['环保', '绿色能源', '政策', '可持续发展'],
                'keywords': ['环境保护', '清洁能源', '政策支持', '可持续发展'],
                'sentiment_score': 0.93,
                'importance_score': 0.89,
                'is_processed': True,
                'published_at': datetime.now() - timedelta(hours=14)
            },
            {
                'title': '人工智能在医疗领域的应用取得重大突破',
                'content': '最新研究显示，AI在疾病诊断、药物研发、个性化治疗等方面取得重大突破。多家医院已开始使用AI辅助诊断系统，诊断准确率提升至95%以上，大大提高了医疗效率。',
                'summary': 'AI医疗应用突破，诊断准确率超95%',
                'source': '医疗科技',
                'source_url': 'https://medical.com/news/ai-medical-breakthrough',
                'category': recommend_category,
                'tags': ['AI医疗', '疾病诊断', '医疗技术', '健康'],
                'keywords': ['人工智能', '医疗诊断', '健康科技', '医学突破'],
                'sentiment_score': 0.96,
                'importance_score': 0.94,
                'is_processed': True,
                'published_at': datetime.now() - timedelta(hours=16)
            }
        ]

        # 插入测试数据
        created_count = 0
        for news_data in test_news:
            # 检查是否已存在（避免重复插入）
            if not RawNews.objects.filter(source_url=news_data['source_url']).exists():
                RawNews.objects.create(**news_data)
                created_count += 1
                self.stdout.write(f"已创建新闻: {news_data['title']}")
            else:
                self.stdout.write(f"新闻已存在: {news_data['title']}")