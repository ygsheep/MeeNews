# 羊咩快报 - API设计文档

## API概述

羊咩快报后端API基于Django REST Framework构建，提供RESTful风格的接口服务。API支持多种内容类型（文章、音频、视频）的统一管理，并提供音频文章同步阅读的核心功能。

### 基础信息

- **API版本**: v1
- **基础URL**: `https://api.yangmie.com/api/v1/`
- **认证方式**: JWT Token
- **数据格式**: JSON
- **字符编码**: UTF-8

### 通用响应格式

```json
{
  "code": 200,
  "message": "success",
  "data": {}, 
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 100,
    "has_next": true,
    "has_previous": false
  },
  "timestamp": "2025-07-20T10:00:00Z"
}
```

### 错误响应格式

```json
{
  "code": 400,
  "message": "请求参数错误",
  "errors": {
    "field_name": ["错误详情"]
  },
  "timestamp": "2025-07-20T10:00:00Z"
}
```

## 认证相关API

### 用户注册

```http
POST /auth/register/
```

**请求参数:**
```json
{
  "username": "user123",
  "email": "user@example.com",
  "password": "password123",
  "nickname": "昵称",
  "phone": "13800138000"
}
```

**响应:**
```json
{
  "code": 200,
  "message": "注册成功",
  "data": {
    "user": {
      "id": 1001,
      "username": "user123",
      "email": "user@example.com",
      "nickname": "昵称",
      "avatar_url": null,
      "created_at": "2025-07-20T10:00:00Z"
    },
    "tokens": {
      "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
      "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
    }
  }
}
```

### 用户登录

```http
POST /auth/login/
```

**请求参数:**
```json
{
  "username": "user123",
  "password": "password123"
}
```

**响应:**
```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "user": {
      "id": 1001,
      "username": "user123",
      "nickname": "昵称",
      "avatar_url": "https://cdn.example.com/avatar.jpg",
      "premium_until": null,
      "preferences": {
        "theme": "auto",
        "preferred_voice": "standard_female",
        "auto_play": true
      }
    },
    "tokens": {
      "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
      "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
    }
  }
}
```

### 刷新Token

```http
POST /auth/refresh/
```

**请求参数:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

## 内容相关API

### 获取内容列表

```http
GET /content/
```

**查询参数:**
- `category_id`: 分类ID
- `content_type`: 内容类型 (article, audio, video)
- `page`: 页码
- `page_size`: 每页数量
- `sort`: 排序方式 (latest, popular, recommended)
- `tags`: 标签过滤
- `search`: 搜索关键词

**响应示例:**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "results": [
      {
        "id": 1001,
        "title": "AI技术发展新突破",
        "summary": "人工智能技术在多个领域取得重大突破...",
        "content_type": "audio",
        "cover_image_url": "https://cdn.example.com/cover.jpg",
        "published_at": "2025-07-20T10:00:00Z",
        "duration": 180,
        "category": {
          "id": 1,
          "name": "科技",
          "color": "#4CD964"
        },
        "author": "AI记者",
        "view_count": 15230,
        "like_count": 892,
        "comment_count": 156,
        "share_count": 78,
        "tags": ["AI", "科技", "突破"],
        "has_audio": true,
        "has_article": true,
        "has_video": false,
        "sync_reading_available": true
      }
    ]
  },
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 100,
    "has_next": true,
    "has_previous": false
  }
}
```

### 获取内容详情

```http
GET /content/{news_id}/
```

**响应示例:**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "news": {
      "id": 1001,
      "title": "AI技术发展新突破",
      "content_type": "audio",
      "summary": "人工智能技术在多个领域取得重大突破...",
      "cover_image_url": "https://cdn.example.com/cover.jpg",
      "published_at": "2025-07-20T10:00:00Z",
      "category": {
        "id": 1,
        "name": "科技",
        "color": "#4CD964"
      },
      "author": "AI记者",
      "view_count": 15230,
      "like_count": 892,
      "comment_count": 156,
      "share_count": 78,
      "tags": ["AI", "科技", "突破"],
      "keywords": ["人工智能", "技术突破", "发展"]
    },
    "contents": {
      "audio": {
        "id": 2001,
        "audio_url": "https://cdn.example.com/audio/1001.mp3",
        "backup_audio_urls": [
          "https://backup1.example.com/audio/1001.mp3",
          "https://backup2.example.com/audio/1001.mp3"
        ],
        "duration": 180,
        "file_size": 5242880,
        "bitrate": 128,
        "format": "mp3",
        "voice_type": "news_female",
        "voice_gender": "female",
        "transcription": "各位听众大家好，今天为大家带来AI技术的最新进展...",
        "chapter_timestamps": [
          {
            "title": "AI技术概述",
            "start": 0,
            "end": 45
          },
          {
            "title": "技术突破点",
            "start": 45,
            "end": 120
          },
          {
            "title": "未来展望",
            "start": 120,
            "end": 180
          }
        ],
        "related_article_id": 3001,
        "sync_reading_enabled": true,
        "audio_quality": "high",
        "generation_method": "tts",
        "download_enabled": true,
        "play_count": 25430
      },
      "article": {
        "id": 3001,
        "content": "人工智能技术正在经历前所未有的发展，各大科技公司纷纷加大投入...",
        "html_content": "<div class='article'><p>人工智能技术正在经历前所未有的发展...</p></div>",
        "markdown_content": "# AI技术发展新突破\n\n人工智能技术正在经历前所未有的发展...",
        "content_structure": {
          "paragraphs": [
            {
              "id": "p1",
              "text": "人工智能技术正在经历前所未有的发展，各大科技公司纷纷加大投入...",
              "start_char": 0,
              "end_char": 68,
              "word_count": 35
            },
            {
              "id": "p2",
              "text": "在自然语言处理领域，大语言模型的能力已经达到了人类水平...",
              "start_char": 69,
              "end_char": 145,
              "word_count": 38
            }
          ],
          "chapters": [
            {
              "title": "技术发展概述",
              "paragraph_ids": ["p1", "p2"]
            }
          ]
        },
        "word_count": 1200,
        "read_time_estimate": 5,
        "tts_enabled": true,
        "tts_script": "各位听众，今天我们来聊聊人工智能技术的最新发展...",
        "content_quality_score": 0.92,
        "readability_score": 0.85
      }
    },
    "sync_data": {
      "id": 4001,
      "sync_type": "full",
      "auto_scroll_enabled": true,
      "highlight_enabled": true,
      "reading_speed_factor": 1.0,
      "sync_accuracy": 0.95,
      "sync_mapping": {
        "paragraphs": [
          {
            "paragraph_id": "p1",
            "start_time": 15,
            "end_time": 45,
            "text": "人工智能技术正在经历前所未有的发展...",
            "confidence": 0.92
          },
          {
            "paragraph_id": "p2",
            "start_time": 45,
            "end_time": 75,
            "text": "在自然语言处理领域，大语言模型的能力...",
            "confidence": 0.88
          }
        ],
        "chapters": [
          {
            "title": "AI技术概述",
            "start_time": 0,
            "end_time": 45,
            "paragraph_ids": ["p1"]
          }
        ],
        "highlights": [
          {
            "start_time": 30,
            "end_time": 35,
            "text": "重大突破",
            "type": "important",
            "color": "#FF6B6B"
          }
        ]
      }
    },
    "user_progress": {
      "current_position": 67,
      "total_duration": 180,
      "progress_percentage": 37.22,
      "last_play_mode": "sync_reading",
      "sync_reading_position": "p2",
      "bookmark_positions": [30, 95, 150],
      "notes": [
        {
          "position": 30,
          "content": "重要观点",
          "created_at": "2025-07-20T15:30:00Z"
        }
      ],
      "play_count": 3,
      "last_updated_at": "2025-07-20T16:45:00Z"
    },
    "related_content": [
      {
        "id": 1002,
        "title": "相关文章标题",
        "content_type": "article",
        "cover_image_url": "https://cdn.example.com/related.jpg"
      }
    ]
  }
}
```

### 切换播放模式

```http
POST /content/{news_id}/switch-mode/
```

**请求参数:**
```json
{
  "from_mode": "audio_only",
  "to_mode": "sync_reading",
  "current_position": 67,
  "device_info": {
    "type": "mobile",
    "os": "iOS",
    "version": "17.0",
    "app_version": "1.0.0"
  }
}
```

**响应:**
```json
{
  "code": 200,
  "message": "模式切换成功",
  "data": {
    "current_mode": "sync_reading",
    "position": 67,
    "sync_data": {
      "current_paragraph": "p2",
      "scroll_position": 320,
      "highlight_words": ["技术", "发展"]
    }
  }
}
```

### 搜索内容

```http
GET /content/search/
```

**查询参数:**
- `q`: 搜索关键词
- `content_type`: 内容类型过滤
- `category_id`: 分类过滤
- `duration_min`: 最小时长（秒）
- `duration_max`: 最大时长（秒）
- `date_from`: 开始日期
- `date_to`: 结束日期
- `sort`: 排序方式 (relevance, date, popularity)

**响应格式与获取内容列表相同**

## 播放进度相关API

### 获取用户播放进度

```http
GET /user/progress/{news_id}/
```

**响应:**
```json
{
  "code": 200,
  "data": {
    "news_id": 1001,
    "content_type": "audio",
    "content_id": 2001,
    "current_position": 67,
    "total_duration": 180,
    "progress_percentage": 37.22,
    "last_play_mode": "sync_reading",
    "sync_reading_position": "p2",
    "bookmark_positions": [30, 95, 150],
    "notes": [
      {
        "position": 30,
        "content": "重要观点",
        "paragraph_id": "p1",
        "created_at": "2025-07-20T15:30:00Z"
      }
    ],
    "play_count": 3,
    "device_type": "mobile",
    "last_updated_at": "2025-07-20T16:45:00Z",
    "created_at": "2025-07-20T10:15:00Z"
  }
}
```

### 更新播放进度

```http
POST /user/progress/{news_id}/
```

**请求参数:**
```json
{
  "content_type": "audio",
  "current_position": 67,
  "play_mode": "sync_reading",
  "sync_reading_position": "p2",
  "session_data": {
    "play_duration": 45,
    "pause_count": 3,
    "seek_count": 1,
    "start_position": 22,
    "end_position": 67,
    "play_speed": 1.0,
    "quality": "high",
    "network_type": "wifi"
  },
  "device_info": {
    "type": "mobile",
    "os": "iOS",
    "version": "17.0"
  }
}
```

**响应:**
```json
{
  "code": 200,
  "message": "进度更新成功",
  "data": {
    "current_position": 67,
    "progress_percentage": 37.22,
    "play_count": 3,
    "updated_at": "2025-07-20T16:45:00Z"
  }
}
```

### 批量获取播放进度

```http
GET /user/progress/
```

**查询参数:**
- `news_ids`: 资讯ID列表，逗号分隔
- `content_type`: 内容类型过滤
- `page`: 页码
- `page_size`: 每页数量

### 添加/更新书签

```http
POST /user/progress/{news_id}/bookmarks/
```

**请求参数:**
```json
{
  "position": 95,
  "mode": "sync_reading",
  "paragraph_id": "p3",
  "note": "重要内容标记",
  "title": "技术突破点"
}
```

### 删除书签

```http
DELETE /user/progress/{news_id}/bookmarks/{position}/
```

## 评论相关API

### 获取评论列表

```http
GET /content/{news_id}/comments/
```

**查询参数:**
- `content_type`: 内容类型 (article, audio, video)
- `comment_type`: 评论类型 (general, timestamped, paragraph)
- `parent_id`: 父评论ID（获取回复）
- `sort`: 排序方式 (latest, oldest, popular)
- `page`: 页码
- `page_size`: 每页数量

**响应:**
```json
{
  "code": 200,
  "data": {
    "results": [
      {
        "id": 5001,
        "user": {
          "id": 1001,
          "nickname": "用户昵称",
          "avatar_url": "https://cdn.example.com/avatar.jpg"
        },
        "content": "这个观点很有意思",
        "comment_type": "timestamped",
        "audio_timestamp": 67,
        "video_timestamp": null,
        "article_paragraph_id": "p2",
        "like_count": 15,
        "reply_count": 3,
        "is_liked": false,
        "is_pinned": false,
        "created_at": "2025-07-20T15:30:00Z",
        "replies": [
          {
            "id": 5002,
            "user": {
              "id": 1002,
              "nickname": "回复者",
              "avatar_url": "https://cdn.example.com/avatar2.jpg"
            },
            "content": "我也这么认为",
            "reply_to_user": {
              "id": 1001,
              "nickname": "用户昵称"
            },
            "like_count": 5,
            "created_at": "2025-07-20T15:35:00Z"
          }
        ]
      }
    ]
  },
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 156
  }
}
```

### 添加评论

```http
POST /content/{news_id}/comments/
```

**请求参数:**
```json
{
  "content_type": "audio",
  "content_id": 2001,
  "content": "这个观点很有意思",
  "comment_type": "timestamped",
  "audio_timestamp": 67,
  "article_paragraph_id": "p2",
  "parent_id": null,
  "reply_to_user_id": null
}
```

**响应:**
```json
{
  "code": 200,
  "message": "评论发布成功",
  "data": {
    "id": 5001,
    "content": "这个观点很有意思",
    "comment_type": "timestamped",
    "audio_timestamp": 67,
    "article_paragraph_id": "p2",
    "like_count": 0,
    "reply_count": 0,
    "created_at": "2025-07-20T15:30:00Z"
  }
}
```

### 删除评论

```http
DELETE /comments/{comment_id}/
```

### 点赞/取消点赞评论

```http
POST /comments/{comment_id}/like/
```

**请求参数:**
```json
{
  "is_like": true
}
```

## 用户互动API

### 点赞内容

```http
POST /content/{news_id}/like/
```

**请求参数:**
```json
{
  "target_type": "news",
  "target_id": 1001,
  "is_like": true
}
```

**响应:**
```json
{
  "code": 200,
  "message": "点赞成功",
  "data": {
    "is_liked": true,
    "like_count": 893
  }
}
```

### 收藏内容

```http
POST /content/{news_id}/favorite/
```

**请求参数:**
```json
{
  "content_type": "audio",
  "folder_name": "技术类收藏",
  "tags": ["AI", "技术"],
  "notes": "很好的技术分析文章",
  "favorite_position": 67,
  "favorite_context": "讲到AI发展前景的部分"
}
```

### 分享内容

```http
POST /content/{news_id}/share/
```

**请求参数:**
```json
{
  "content_type": "audio",
  "content_id": 2001,
  "share_platform": "wechat",
  "share_text": "推荐一篇很棒的AI技术文章",
  "audio_position": 67,
  "article_paragraph_id": "p2"
}
```

### 获取用户收藏列表

```http
GET /user/favorites/
```

**查询参数:**
- `content_type`: 内容类型过滤
- `folder_name`: 收藏夹名称
- `tags`: 标签过滤
- `sort`: 排序方式 (latest, oldest, title)
- `page`: 页码
- `page_size`: 每页数量

## 分类和标签API

### 获取分类列表

```http
GET /categories/
```

**响应:**
```json
{
  "code": 200,
  "data": [
    {
      "id": 1,
      "name": "科技",
      "name_en": "Technology",
      "description": "AI、互联网、科技创新相关资讯",
      "icon_url": "https://cdn.example.com/icons/tech.svg",
      "color_code": "#4CD964",
      "parent_id": null,
      "sort_order": 1,
      "content_count": 1250,
      "is_active": true,
      "children": [
        {
          "id": 11,
          "name": "人工智能",
          "color_code": "#4CD964",
          "content_count": 430
        }
      ]
    }
  ]
}
```

### 获取热门标签

```http
GET /tags/popular/
```

**查询参数:**
- `category_id`: 分类ID
- `period`: 时间段 (day, week, month)
- `limit`: 返回数量

## 推荐系统API

### 获取个性化推荐

```http
GET /recommendations/
```

**查询参数:**
- `content_type`: 内容类型
- `count`: 推荐数量
- `algorithm`: 推荐算法 (collaborative, content_based, trending)
- `scene`: 使用场景 (home_feed, related_content, continue_reading)

**响应:**
```json
{
  "code": 200,
  "data": {
    "recommendations": [
      {
        "content": {
          "id": 1002,
          "title": "推荐内容标题",
          "content_type": "audio",
          "cover_image_url": "https://cdn.example.com/cover2.jpg"
        },
        "score": 0.92,
        "reasons": ["相似用户喜欢", "匹配兴趣标签"],
        "algorithm": "collaborative"
      }
    ],
    "metadata": {
      "algorithm_mix": {
        "collaborative": 0.4,
        "content_based": 0.4,
        "trending": 0.2
      },
      "personalization_level": 0.85
    }
  }
}
```

### 获取热门内容

```http
GET /trending/
```

**查询参数:**
- `content_type`: 内容类型
- `category_id`: 分类ID
- `period`: 时间段 (hour, day, week)
- `metric`: 排序指标 (view, like, share, comment)

### 获取相关内容

```http
GET /content/{news_id}/related/
```

**查询参数:**
- `count`: 返回数量
- `exclude_current`: 是否排除当前内容

## 用户设置API

### 获取用户偏好设置

```http
GET /user/preferences/
```

**响应:**
```json
{
  "code": 200,
  "data": {
    "language": "zh-CN",
    "theme": "auto",
    "audio_quality": "high",
    "auto_play": true,
    "notification_enabled": true,
    "push_news": true,
    "push_comments": true,
    "preferred_voice": "news_female",
    "playback_speed": 1.0,
    "sync_reading_preferences": {
      "auto_scroll_enabled": true,
      "highlight_enabled": true,
      "scroll_speed": 1.2,
      "highlight_color": "#FFD700",
      "font_size": "16px",
      "line_height": 1.6
    },
    "scene_preferences": ["morning_news", "tech_updates"],
    "interest_categories": {
      "tech": 0.8,
      "finance": 0.6,
      "sports": 0.3
    }
  }
}
```

### 更新用户偏好设置

```http
PUT /user/preferences/
```

**请求参数:**
```json
{
  "auto_play": false,
  "preferred_voice": "sweet_female",
  "playback_speed": 1.25,
  "sync_reading_preferences": {
    "auto_scroll_enabled": true,
    "highlight_color": "#FF6B6B"
  }
}
```

### 获取同步阅读配置

```http
GET /content/{news_id}/sync-config/
```

**响应:**
```json
{
  "code": 200,
  "data": {
    "sync_enabled": true,
    "auto_scroll_speed": 1.2,
    "highlight_color": "#FFD700",
    "reading_speed_factor": 1.0,
    "chapter_navigation": true,
    "progress_indicator": true,
    "word_highlight_enabled": false,
    "custom_settings": {
      "font_size": "16px",
      "line_height": 1.6,
      "paragraph_spacing": "12px",
      "reading_width": "700px"
    }
  }
}
```

## 统计分析API

### 内容播放统计

```http
POST /analytics/play/
```

**请求参数:**
```json
{
  "news_id": 1001,
  "content_type": "audio",
  "content_id": 2001,
  "play_duration": 45,
  "total_duration": 180,
  "completion_rate": 25.0,
  "play_mode": "sync_reading",
  "play_source": "home",
  "device_info": {
    "type": "mobile",
    "os": "iOS",
    "version": "17.0"
  },
  "session_data": {
    "start_time": "2025-07-20T16:00:00Z",
    "end_time": "2025-07-20T16:00:45Z",
    "pause_count": 2,
    "seek_count": 1,
    "volume_level": 0.8,
    "play_speed": 1.0
  }
}
```

### 用户行为统计

```http
POST /analytics/behavior/
```

**请求参数:**
```json
{
  "action": "mode_switch",
  "from_mode": "audio_only",
  "to_mode": "sync_reading",
  "news_id": 1001,
  "position": 67,
  "context": {
    "trigger": "user_click",
    "previous_actions": ["play", "pause", "seek"]
  }
}
```

## WebSocket API

### 实时同步连接

```websocket
ws://api.yangmie.com/ws/sync/{news_id}/
```

**连接时发送认证信息:**
```json
{
  "type": "auth",
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**同步位置更新:**
```json
{
  "type": "position_update",
  "position": 67,
  "mode": "sync_reading",
  "paragraph_id": "p2"
}
```

**接收同步事件:**
```json
{
  "type": "sync_update",
  "data": {
    "position": 67,
    "paragraph_id": "p2",
    "highlight_words": ["技术", "发展"],
    "scroll_position": 320
  }
}
```

## 错误代码说明

| 错误代码 | 说明 |
|---------|------|
| 400 | 请求参数错误 |
| 401 | 未授权，需要登录 |
| 403 | 权限不足 |
| 404 | 资源不存在 |
| 409 | 资源冲突 |
| 429 | 请求频率限制 |
| 500 | 服务器内部错误 |
| 503 | 服务不可用 |

## 请求频率限制

| 接口类型 | 限制规则 |
|---------|----------|
| 用户认证 | 10次/分钟 |
| 内容查询 | 100次/分钟 |
| 进度更新 | 60次/分钟 |
| 评论操作 | 30次/分钟 |
| 互动操作 | 50次/分钟 |

## 数据缓存策略

| 数据类型 | 缓存时间 |
|---------|----------|
| 内容列表 | 5分钟 |
| 内容详情 | 10分钟 |
| 用户偏好 | 30分钟 |
| 分类标签 | 1小时 |
| 推荐内容 | 15分钟 |

---

*本API文档持续更新，实际使用中请以最新版本为准。*