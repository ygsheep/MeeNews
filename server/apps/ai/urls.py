from django.urls import path
from .views import AITTSGenerateView, AITTSStatusView

urlpatterns = [
    path('ai/tts', AITTSGenerateView.as_view()),  # 提交AI音频生成任务
    path('ai/tts/<str:task_id>', AITTSStatusView.as_view()),  # 查询AI音频生成任务状态
] 