// 内容相关API，适配Django后端RESTful接口
import { http } from '@/utils/request'

/**
 * 获取推荐内容（多媒体混排）
 * @param {Object} params - 查询参数（type, category, tag, sort, page, page_size等）
 * @returns {Promise<Array>} 推荐内容列表
 */
export const getRecommendList = async (params = {}) => {
  const res = await http.get('/content/recommend', params)
  if (res && res.success && res.data && Array.isArray(res.data.results)) {
    return res.data.results
  }
  return []
}

/**
 * 获取每日资讯内容（文章为主）
 * @param {Object} params - 查询参数（可扩展）
 * @returns {Promise<Array>} 每日资讯内容列表
 */
export const getDailyNews = async (params = {}) => {
  const query = { ...params, type: 'article', category: 'daily', sort: 'published_at' }
  const res = await http.get('/content/recommend', query)
  if (res && res.success && res.data && Array.isArray(res.data.results)) {
    return res.data.results
  }
  return []
}

/**
 * 获取关注内容
 * @param {Object} params - 查询参数（可扩展）
 * @returns {Promise<Array>} 关注内容列表
 */
export const getFollowContent = async (params = {}) => {
  const query = { ...params, tag: 'follow' }
  const res = await http.get('/content/recommend', query)
  if (res && res.success && res.data && Array.isArray(res.data.results)) {
    return res.data.results
  }
  return []
}

/**
 * 获取资讯内容
 * @param {Object} params - 查询参数（可扩展）
 * @returns {Promise<Array>} 资讯内容列表
 */
export const getNewsContent = async (params = {}) => {
  const query = { ...params, tag: 'news', sort: 'latest' }
  const res = await http.get('/content/recommend', query)
  if (res && res.success && res.data && Array.isArray(res.data.results)) {
    return res.data.results
  }
  return []
}

/**
 * 获取推荐作者/专栏（如后端支持）
 * @param {Object} params - 查询参数（可扩展）
 * @returns {Promise<Array>} 推荐作者列表
 */
export const getRecommendedAuthors = async (params = {}) => {
  // const res = await http.get('/authors/recommend', params)
  // if (res && res.success && res.data && Array.isArray(res.data.results)) {
  //   return res.data.results
  // }
  return []
}

/**
 * 获取内容详情
 * @param {number|string} contentId - 内容ID
 * @returns {Promise<Object|null>} 内容详情对象
 */
export const getContentDetail = async (contentId) => {
  if (!contentId) return null
  const res = await http.get(`/content/${contentId}`)
  if (res && res.success && res.data) {
    return res.data
  }
  return null
}

/**
 * 获取文章详情
 * @param {number|string} articleId - 文章ID
 * @returns {Promise<Object>} 文章详情
 */
export const getArticleDetail = async (articleId) => {
  if (!articleId) return null
  const res = await http.get(`/content/${articleId}`)
  return res
}

/**
 * 搜索内容
 * @param {Object} params - 查询参数（q, type, category_id, tag, page, page_size等）
 * @returns {Promise<Array>} 搜索结果列表
 */
export const searchContent = async (params = {}) => {
  const res = await http.get('/content/search', params)
  if (res && res.success && res.data && Array.isArray(res.data.results)) {
    return res.data.results
  }
  return []
}

/**
 * 获取分类列表
 * @param {Object} params - 查询参数（parent_id, is_active等）
 * @returns {Promise<Array>} 分类列表
 */
export const getCategoryList = async (params = {}) => {
  const res = await http.get('/categories', params)
  if (res && res.success && Array.isArray(res.data)) {
    return res.data
  }
  return []
}

/**
 * 获取热门内容
 * @param {Object} params - 查询参数（period, category_id, limit等）
 * @returns {Promise<Array>} 热门内容列表
 */
export const getTrendingContent = async (params = {}) => {
  const res = await http.get('/content/trending', params)
  if (res && res.success && res.data && Array.isArray(res.data.results)) {
    return res.data.results
  }
  return []
}

/**
 * 获取最近播放内容
 * @param {Object} params - 查询参数（如分页）
 * @returns {Promise<Array>} 最近播放内容列表
 */
export const getRecentPlayed = async (params = {}) => {
  const res = await http.get('/users/recent-played', params)
  if (res && res.success && res.data && Array.isArray(res.data.results)) {
    return res.data.results
  }
  return []
}

/**
 * 收藏/取消收藏内容
 * @param {number|string} contentId - 内容ID
 * @param {boolean} bookmarked - 是否收藏
 * @returns {Promise<Object>} 操作结果
 */
export const bookmarkContent = async (contentId, bookmarked) => {
  if (!contentId) return null
  const res = await http.post('/content/bookmark', { content_id: contentId, bookmarked })
  return res
}

/**
 * 关注/取关用户
 * @param {number|string} userId - 用户ID
 * @param {boolean} follow - true=关注，false=取关
 * @returns {Promise<Object>} 操作结果
 */
export const followUser = async (userId, follow) => {
  if (!userId) return null
  const res = await http.post('/user/follow', { user_id: userId, follow })
  return res
}

/**
 * 点赞/取消点赞内容
 * @param {number|string} contentId - 内容ID
 * @param {boolean} liked - 是否点赞
 * @returns {Promise<Object>} 操作结果
 */
export const likeContent = async (contentId, liked) => {
  if (!contentId) return null
  const res = await http.post('/content/like', { content_id: contentId, liked })
  return res
}

/**
 * 获取相关文章
 * @param {number|string} articleId - 文章ID
 * @param {Object} params - 其他查询参数（如 limit, exclude_current）
 * @returns {Promise<Object>} 相关文章列表
 */
export const getRelatedArticles = async (articleId, params = {}) => {
  if (!articleId) return null
  const res = await http.get(`/content/${articleId}/related`, params)
  return res
}