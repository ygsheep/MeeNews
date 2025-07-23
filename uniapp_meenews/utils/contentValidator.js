/**
 * 内容类型验证和处理工具
 * 提供健壮的内容类型检测、验证和规范化功能
 */

// 支持的内容类型枚举
export const CONTENT_TYPES = {
  AUDIO: 'audio',
  VIDEO: 'video',
  ARTICLE: 'article',
  PODCAST: 'podcast',
  NEWS: 'news',
  LIVE: 'live'
}

// 内容类型配置
export const CONTENT_TYPE_CONFIG = {
  [CONTENT_TYPES.AUDIO]: {
    name: '音频',
    icon: 'volume-up',
    color: '#667eea',
    supportedFormats: ['mp3', 'wav', 'aac', 'm4a', 'flac'],
    maxDuration: 3600 * 4, // 4小时
    minDuration: 10, // 10秒
    playerType: 'audio',
    supportTTS: false,
    supportLyrics: true
  },
  [CONTENT_TYPES.VIDEO]: {
    name: '视频',
    icon: 'play',
    color: '#f093fb',
    supportedFormats: ['mp4', 'webm', 'mov', 'avi'],
    maxDuration: 3600 * 2, // 2小时
    minDuration: 5, // 5秒
    playerType: 'video',
    supportTTS: false,
    supportSubtitles: true
  },
  [CONTENT_TYPES.ARTICLE]: {
    name: '文章',
    icon: 'document',
    color: '#4facfe',
    supportedFormats: ['html', 'markdown', 'text'],
    maxLength: 100000, // 最大字符数
    minLength: 100, // 最小字符数
    playerType: 'reader',
    supportTTS: true,
    supportBookmark: true
  },
  [CONTENT_TYPES.PODCAST]: {
    name: '播客',
    icon: 'radio',
    color: '#a8edea',
    supportedFormats: ['mp3', 'wav', 'aac'],
    maxDuration: 3600 * 6, // 6小时
    minDuration: 60, // 1分钟
    playerType: 'audio',
    supportTTS: false,
    supportChapters: true
  },
  [CONTENT_TYPES.NEWS]: {
    name: '资讯',
    icon: 'newspaper',
    color: '#ff9a9e',
    supportedFormats: ['html', 'markdown'],
    maxLength: 50000,
    minLength: 50,
    playerType: 'reader',
    supportTTS: true,
    supportShare: true
  },
  [CONTENT_TYPES.LIVE]: {
    name: '直播',
    icon: 'broadcast',
    color: '#ff6b6b',
    supportedFormats: ['hls', 'rtmp', 'webrtc'],
    playerType: 'live',
    supportTTS: false,
    supportChat: true
  }
}

/**
 * 内容验证器类
 */
export class ContentValidator {
  /**
   * 验证内容对象的完整性和有效性
   * @param {Object} content - 内容对象
   * @returns {Object} 验证结果
   */
  static validateContent(content) {
    const result = {
      isValid: false,
      errors: [],
      warnings: [],
      normalizedContent: null
    }

    try {
      // 基础字段验证
      if (!content) {
        result.errors.push('内容对象不能为空')
        return result
      }

      if (!content.id) {
        result.errors.push('缺少内容ID')
      }

      if (!content.title || typeof content.title !== 'string') {
        result.errors.push('缺少有效的标题')
      } else if (content.title.length > 200) {
        result.warnings.push('标题过长，建议不超过200字符')
      }

      // 内容类型验证
      const contentType = this.detectContentType(content)
      if (!contentType) {
        result.errors.push('无法确定内容类型')
        return result
      }

      // 内容类型特定验证
      const typeValidation = this.validateByType(content, contentType)
      result.errors.push(...typeValidation.errors)
      result.warnings.push(...typeValidation.warnings)

      // URL 验证
      const urlValidation = this.validateUrls(content, contentType)
      result.errors.push(...urlValidation.errors)
      result.warnings.push(...urlValidation.warnings)

      // 元数据验证
      const metaValidation = this.validateMetadata(content)
      result.warnings.push(...metaValidation.warnings)

      // 规范化内容
      result.normalizedContent = this.normalizeContent(content, contentType)

      // 确定最终验证状态
      result.isValid = result.errors.length === 0

    } catch (error) {
      console.error('Content validation error:', error)
      result.errors.push('内容验证过程出错')
    }

    return result
  }

  /**
   * 检测内容类型
   * @param {Object} content - 内容对象
   * @returns {string|null} 内容类型
   */
  static detectContentType(content) {
    // 优先使用明确指定的类型
    if (content.content_type && this.isValidContentType(content.content_type)) {
      return content.content_type
    }

    // 向后兼容的 type 字段
    if (content.type && this.isValidContentType(content.type)) {
      return content.type
    }

    // 基于 URL 和内容特征推断类型
    if (content.audio_url || content.stream_url) {
      return CONTENT_TYPES.AUDIO
    }

    if (content.video_url || content.hls_url) {
      return CONTENT_TYPES.VIDEO
    }

    if (content.content || content.html_content || content.markdown_content) {
      return CONTENT_TYPES.ARTICLE
    }

    // 基于文件扩展名推断
    const urls = [
      content.media_url,
      content.source_url,
      content.file_url
    ].filter(Boolean)

    for (const url of urls) {
      const type = this.detectTypeFromUrl(url)
      if (type) return type
    }

    // 基于 MIME 类型推断
    if (content.mime_type) {
      return this.detectTypeFromMimeType(content.mime_type)
    }

    // 基于分类标签推断
    if (content.category || content.tags) {
      const tags = Array.isArray(content.tags) ? content.tags : [content.category]
      const type = this.detectTypeFromTags(tags)
      if (type) return type
    }

    return null
  }

  /**
   * 验证内容类型是否有效
   * @param {string} type - 内容类型
   * @returns {boolean}
   */
  static isValidContentType(type) {
    return Object.values(CONTENT_TYPES).includes(type)
  }

  /**
   * 从 URL 检测内容类型
   * @param {string} url - 文件 URL
   * @returns {string|null}
   */
  static detectTypeFromUrl(url) {
    if (!url || typeof url !== 'string') return null

    const extension = url.split('.').pop()?.toLowerCase()
    if (!extension) return null

    for (const [type, config] of Object.entries(CONTENT_TYPE_CONFIG)) {
      if (config.supportedFormats?.includes(extension)) {
        return type
      }
    }

    return null
  }

  /**
   * 从 MIME 类型检测内容类型
   * @param {string} mimeType - MIME 类型
   * @returns {string|null}
   */
  static detectTypeFromMimeType(mimeType) {
    if (!mimeType) return null

    const mimeMap = {
      'audio/': CONTENT_TYPES.AUDIO,
      'video/': CONTENT_TYPES.VIDEO,
      'text/html': CONTENT_TYPES.ARTICLE,
      'text/markdown': CONTENT_TYPES.ARTICLE,
      'text/plain': CONTENT_TYPES.ARTICLE,
      'application/json': CONTENT_TYPES.ARTICLE
    }

    for (const [mime, type] of Object.entries(mimeMap)) {
      if (mimeType.startsWith(mime)) {
        return type
      }
    }

    return null
  }

  /**
   * 从标签检测内容类型
   * @param {Array} tags - 标签数组
   * @returns {string|null}
   */
  static detectTypeFromTags(tags) {
    if (!Array.isArray(tags)) return null

    const tagMap = {
      '音频': CONTENT_TYPES.AUDIO,
      '音乐': CONTENT_TYPES.AUDIO,
      'music': CONTENT_TYPES.AUDIO,
      'audio': CONTENT_TYPES.AUDIO,
      '视频': CONTENT_TYPES.VIDEO,
      'video': CONTENT_TYPES.VIDEO,
      '电影': CONTENT_TYPES.VIDEO,
      '文章': CONTENT_TYPES.ARTICLE,
      'article': CONTENT_TYPES.ARTICLE,
      '新闻': CONTENT_TYPES.NEWS,
      'news': CONTENT_TYPES.NEWS,
      '播客': CONTENT_TYPES.PODCAST,
      'podcast': CONTENT_TYPES.PODCAST,
      '直播': CONTENT_TYPES.LIVE,
      'live': CONTENT_TYPES.LIVE
    }

    for (const tag of tags) {
      if (typeof tag === 'string') {
        const normalizedTag = tag.toLowerCase().trim()
        if (tagMap[normalizedTag]) {
          return tagMap[normalizedTag]
        }
      }
    }

    return null
  }

  /**
   * 按类型验证内容
   * @param {Object} content - 内容对象
   * @param {string} contentType - 内容类型
   * @returns {Object} 验证结果
   */
  static validateByType(content, contentType) {
    const result = { errors: [], warnings: [] }
    const config = CONTENT_TYPE_CONFIG[contentType]

    if (!config) {
      result.errors.push(`不支持的内容类型: ${contentType}`)
      return result
    }

    switch (contentType) {
      case CONTENT_TYPES.AUDIO:
      case CONTENT_TYPES.PODCAST:
        this.validateAudioContent(content, result, config)
        break
      case CONTENT_TYPES.VIDEO:
        this.validateVideoContent(content, result, config)
        break
      case CONTENT_TYPES.ARTICLE:
      case CONTENT_TYPES.NEWS:
        this.validateArticleContent(content, result, config)
        break
      case CONTENT_TYPES.LIVE:
        this.validateLiveContent(content, result, config)
        break
    }

    return result
  }

  /**
   * 验证音频内容
   */
  static validateAudioContent(content, result, config) {
    if (!content.audio_url && !content.stream_url && !content.media_url) {
      result.errors.push('缺少音频播放地址')
    }

    if (content.duration) {
      if (content.duration > config.maxDuration) {
        result.warnings.push(`音频时长过长，建议不超过${Math.floor(config.maxDuration / 60)}分钟`)
      }
      if (content.duration < config.minDuration) {
        result.warnings.push(`音频时长过短，建议不少于${config.minDuration}秒`)
      }
    }

    if (content.artist && typeof content.artist !== 'object') {
      result.warnings.push('艺术家信息格式不正确')
    }
  }

  /**
   * 验证视频内容
   */
  static validateVideoContent(content, result, config) {
    // 兼容嵌套 video_content 结构
    const videoUrl = content.video_url || content.hls_url || content.media_url || (content.video_content && (content.video_content.video_url || content.video_content.hls_url || content.video_content.media_url))
    if (!videoUrl) {
      result.errors.push('缺少视频播放地址')
    }

    const duration = content.duration || (content.video_content && content.video_content.duration)
    if (duration) {
      if (duration > config.maxDuration) {
        result.warnings.push(`视频时长过长，建议不超过${Math.floor(config.maxDuration / 60)}分钟`)
      }
      if (duration < config.minDuration) {
        result.warnings.push(`视频时长过短，建议不少于${config.minDuration}秒`)
      }
    }

    const thumbnailUrl = content.thumbnail_url || content.cover_url || (content.video_content && (content.video_content.thumbnail_url || content.video_content.cover_url))
    if (!thumbnailUrl) {
      result.warnings.push('缺少视频缩略图')
    }
  }

  /**
   * 验证文章内容
   */
  static validateArticleContent(content, result, config) {
    if (!content.content && !content.html_content && !content.markdown_content) {
      result.errors.push('缺少文章正文内容')
    }

    const textContent = content.content || content.html_content || content.markdown_content || ''
    const textLength = this.getTextLength(textContent)

    if (textLength > config.maxLength) {
      result.warnings.push(`文章内容过长，建议不超过${config.maxLength}字符`)
    }
    if (textLength < config.minLength) {
      result.warnings.push(`文章内容过短，建议不少于${config.minLength}字符`)
    }

    if (!content.summary && textLength > 500) {
      result.warnings.push('建议添加文章摘要')
    }

    if (!content.author && !content.source) {
      result.warnings.push('缺少作者或来源信息')
    }
  }

  /**
   * 验证直播内容
   */
  static validateLiveContent(content, result, config) {
    if (!content.live_url && !content.stream_url) {
      result.errors.push('缺少直播流地址')
    }

    if (!content.is_live && content.status !== 'live') {
      result.warnings.push('直播状态不明确')
    }

    if (!content.start_time) {
      result.warnings.push('缺少直播开始时间')
    }
  }

  /**
   * 验证 URL 地址
   */
  static validateUrls(content, contentType) {
    const result = { errors: [], warnings: [] }

    // 检查封面图片
    if (content.cover_url) {
      if (!this.isValidUrl(content.cover_url)) {
        result.warnings.push('封面图片URL格式无效')
      }
    }

    // 检查头像
    if (content.author?.avatar_url) {
      if (!this.isValidUrl(content.author.avatar_url)) {
        result.warnings.push('作者头像URL格式无效')
      }
    }

    // 检查媒体URL
    const mediaUrls = [
      content.audio_url,
      content.video_url,
      content.stream_url,
      content.hls_url,
      content.live_url,
      content.media_url
    ].filter(Boolean)

    for (const url of mediaUrls) {
      if (!this.isValidUrl(url)) {
        result.errors.push('媒体URL格式无效')
        break
      }
    }

    return result
  }

  /**
   * 验证元数据
   */
  static validateMetadata(content) {
    const result = { warnings: [] }

    // 检查时间戳
    const timeFields = ['created_at', 'updated_at', 'published_at']
    for (const field of timeFields) {
      if (content[field] && !this.isValidTimestamp(content[field])) {
        result.warnings.push(`${field}时间格式无效`)
      }
    }

    // 检查数值字段
    const numberFields = ['duration', 'view_count', 'like_count', 'comment_count']
    for (const field of numberFields) {
      if (content[field] !== undefined && (!Number.isInteger(content[field]) || content[field] < 0)) {
        result.warnings.push(`${field}数值无效`)
      }
    }

    return result
  }

  /**
   * 规范化内容对象
   * @param {Object} content - 原始内容
   * @param {string} contentType - 内容类型
   * @returns {Object} 规范化后的内容
   */
  static normalizeContent(content, contentType) {
    const normalized = { ...content }

    // 统一内容类型字段
    normalized.content_type = contentType
    if (normalized.type !== contentType) {
      normalized.type = contentType
    }

    // 规范化基础字段
    normalized.title = (normalized.title || '').trim()
    normalized.summary = (normalized.summary || '').trim()

    // 兼容 video_content 嵌套字段
    if (contentType === CONTENT_TYPES.VIDEO && content.video_content) {
      normalized.video_url = normalized.video_url || normalized.video_content.video_url || normalized.video_content.hls_url || normalized.video_content.media_url
      normalized.duration = normalized.duration || normalized.video_content.duration
      normalized.thumbnail_url = normalized.thumbnail_url || normalized.video_content.thumbnail_url || normalized.video_content.cover_url
    }

    // 规范化数值字段
    const numberFields = ['duration', 'view_count', 'like_count', 'comment_count']
    for (const field of numberFields) {
      if (normalized[field] !== undefined) {
        normalized[field] = Math.max(0, parseInt(normalized[field]) || 0)
      }
    }

    // 规范化布尔字段
    const booleanFields = ['is_liked', 'is_bookmarked', 'is_following', 'is_live']
    for (const field of booleanFields) {
      if (normalized[field] !== undefined) {
        normalized[field] = Boolean(normalized[field])
      }
    }

    // 规范化作者信息
    if (normalized.author && typeof normalized.author === 'object') {
      normalized.author = {
        id: normalized.author.id,
        name: (normalized.author.name || '').trim(),
        avatar_url: normalized.author.avatar_url || '',
        description: (normalized.author.description || '').trim(),
        is_following: Boolean(normalized.author.is_following)
      }
    }

    // 添加类型配置信息
    normalized._typeConfig = CONTENT_TYPE_CONFIG[contentType]

    return normalized
  }

  /**
   * 辅助方法：检查 URL 是否有效
   */
  static isValidUrl(url) {
    try {
      new URL(url)
      return true
    } catch {
      return false
    }
  }

  /**
   * 辅助方法：检查时间戳是否有效
   */
  static isValidTimestamp(timestamp) {
    const date = new Date(timestamp)
    return !isNaN(date.getTime())
  }

  /**
   * 辅助方法：获取文本长度（去除HTML标签）
   */
  static getTextLength(content) {
    if (!content) return 0
    
    // 简单的 HTML 标签移除
    const textContent = content.replace(/<[^>]*>/g, '').trim()
    return textContent.length
  }
}

/**
 * 内容类型工具函数
 */
export const ContentTypeUtils = {
  /**
   * 获取内容类型配置
   */
  getTypeConfig(contentType) {
    return CONTENT_TYPE_CONFIG[contentType] || null
  },

  /**
   * 获取内容类型名称
   */
  getTypeName(contentType) {
    return CONTENT_TYPE_CONFIG[contentType]?.name || '未知'
  },

  /**
   * 获取内容类型图标
   */
  getTypeIcon(contentType) {
    return CONTENT_TYPE_CONFIG[contentType]?.icon || 'file'
  },

  /**
   * 获取内容类型颜色
   */
  getTypeColor(contentType) {
    return CONTENT_TYPE_CONFIG[contentType]?.color || '#8d96a0'
  },

  /**
   * 检查是否支持某个功能
   */
  supportsFeature(contentType, feature) {
    const config = CONTENT_TYPE_CONFIG[contentType]
    if (!config) return false
    
    return Boolean(config[feature])
  },

  /**
   * 获取推荐的播放器类型
   */
  getPlayerType(contentType) {
    return CONTENT_TYPE_CONFIG[contentType]?.playerType || 'unknown'
  },

  /**
   * 批量验证内容数组
   */
  validateContentArray(contentArray) {
    if (!Array.isArray(contentArray)) {
      return {
        isValid: false,
        validItems: [],
        invalidItems: [],
        errors: ['输入必须是数组']
      }
    }

    const validItems = []
    const invalidItems = []
    const errors = []

    contentArray.forEach((content, index) => {
      const validation = ContentValidator.validateContent(content)
      
      if (validation.isValid) {
        validItems.push(validation.normalizedContent)
      } else {
        invalidItems.push({
          index,
          content,
          errors: validation.errors,
          warnings: validation.warnings
        })
        errors.push(`第${index + 1}项: ${validation.errors.join(', ')}`)
      }
    })

    return {
      isValid: invalidItems.length === 0,
      validItems,
      invalidItems,
      errors,
      summary: {
        total: contentArray.length,
        valid: validItems.length,
        invalid: invalidItems.length
      }
    }
  }
}

// 默认导出
export default {
  CONTENT_TYPES,
  CONTENT_TYPE_CONFIG,
  ContentValidator,
  ContentTypeUtils
}