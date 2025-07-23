/**
 * 格式化工具函数
 * 提供时间、数字、文本等常用格式化功能
 */

/**
 * 格式化时间
 * @param {string|number|Date} timestamp - 时间戳或日期
 * @param {string} format - 格式类型 (relative, date, datetime, time)
 * @returns {string} 格式化后的时间字符串
 */
export const formatTime = (timestamp, format = 'relative') => {
  if (!timestamp) return ''

  let date
  try {
    date = new Date(timestamp)
    if (isNaN(date.getTime())) {
      return '无效时间'
    }
  } catch (error) {
    console.error('时间格式化错误:', error)
    return '无效时间'
  }

  const now = new Date()
  const diff = now.getTime() - date.getTime()

  switch (format) {
    case 'relative':
      return formatRelativeTime(diff)
    case 'date':
      return formatDate(date)
    case 'datetime':
      return formatDateTime(date)
    case 'time':
      return formatTimeOnly(date)
    default:
      return formatRelativeTime(diff)
  }
}

/**
 * 格式化相对时间
 * @param {number} diff - 时间差（毫秒）
 * @returns {string} 相对时间字符串
 */
const formatRelativeTime = (diff) => {
  const seconds = Math.floor(diff / 1000)
  const minutes = Math.floor(seconds / 60)
  const hours = Math.floor(minutes / 60)
  const days = Math.floor(hours / 24)
  const months = Math.floor(days / 30)
  const years = Math.floor(days / 365)

  if (seconds < 60) {
    return '刚刚'
  } else if (minutes < 60) {
    return `${minutes}分钟前`
  } else if (hours < 24) {
    return `${hours}小时前`
  } else if (days < 30) {
    return `${days}天前`
  } else if (months < 12) {
    return `${months}个月前`
  } else {
    return `${years}年前`
  }
}

/**
 * 格式化日期
 * @param {Date} date - 日期对象
 * @returns {string} 格式化的日期字符串
 */
const formatDate = (date) => {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  
  const now = new Date()
  const currentYear = now.getFullYear()
  
  // 如果是今年的日期，不显示年份
  if (year === currentYear) {
    return `${month}-${day}`
  } else {
    return `${year}-${month}-${day}`
  }
}

/**
 * 格式化日期时间
 * @param {Date} date - 日期对象
 * @returns {string} 格式化的日期时间字符串
 */
const formatDateTime = (date) => {
  const dateStr = formatDate(date)
  const timeStr = formatTimeOnly(date)
  return `${dateStr} ${timeStr}`
}

/**
 * 格式化时间（仅时分）
 * @param {Date} date - 日期对象
 * @returns {string} 格式化的时间字符串
 */
const formatTimeOnly = (date) => {
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  return `${hours}:${minutes}`
}

/**
 * 格式化数字
 * @param {number} num - 要格式化的数字
 * @param {string} type - 格式类型 (compact, full, percentage)
 * @returns {string} 格式化后的数字字符串
 */
export const formatNumber = (num, type = 'compact') => {
  if (typeof num !== 'number' || isNaN(num)) {
    return '0'
  }

  switch (type) {
    case 'compact':
      return formatCompactNumber(num)
    case 'full':
      return formatFullNumber(num)
    case 'percentage':
      return `${(num * 100).toFixed(1)}%`
    default:
      return formatCompactNumber(num)
  }
}

/**
 * 格式化紧凑数字（带单位）
 * @param {number} num - 数字
 * @returns {string} 格式化的数字字符串
 */
const formatCompactNumber = (num) => {
  if (num < 1000) {
    return num.toString()
  } else if (num < 10000) {
    return `${(num / 1000).toFixed(1)}K`
  } else if (num < 100000) {
    return `${Math.floor(num / 1000)}K`
  } else if (num < 1000000) {
    return `${(num / 10000).toFixed(1)}万`
  } else if (num < 100000000) {
    return `${Math.floor(num / 10000)}万`
  } else {
    return `${(num / 100000000).toFixed(1)}亿`
  }
}

/**
 * 格式化完整数字（带千分位分隔符）
 * @param {number} num - 数字
 * @returns {string} 格式化的数字字符串
 */
const formatFullNumber = (num) => {
  return num.toLocaleString('zh-CN')
}

/**
 * 格式化时长
 * @param {number} seconds - 秒数
 * @param {boolean} showHours - 是否显示小时
 * @returns {string} 格式化的时长字符串
 */
export const formatDuration = (seconds, showHours = false) => {
  if (typeof seconds !== 'number' || isNaN(seconds) || seconds < 0) {
    return '00:00'
  }

  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = Math.floor(seconds % 60)

  if (showHours || hours > 0) {
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  } else {
    return `${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  }
}

/**
 * 格式化文件大小
 * @param {number} bytes - 字节数
 * @param {number} decimals - 小数位数
 * @returns {string} 格式化的文件大小字符串
 */
export const formatFileSize = (bytes, decimals = 2) => {
  if (typeof bytes !== 'number' || isNaN(bytes) || bytes < 0) {
    return '0 B'
  }

  if (bytes === 0) return '0 B'

  const k = 1024
  const dm = decimals < 0 ? 0 : decimals
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']

  const i = Math.floor(Math.log(bytes) / Math.log(k))

  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i]
}

/**
 * 格式化文本长度
 * @param {string} text - 文本内容
 * @param {number} maxLength - 最大长度
 * @param {string} suffix - 截断后缀
 * @returns {string} 格式化的文本
 */
export const formatTextLength = (text, maxLength = 100, suffix = '...') => {
  if (!text || typeof text !== 'string') {
    return ''
  }

  if (text.length <= maxLength) {
    return text
  }

  return text.substring(0, maxLength - suffix.length) + suffix
}

/**
 * 格式化手机号
 * @param {string} phone - 手机号
 * @returns {string} 格式化的手机号
 */
export const formatPhone = (phone) => {
  if (!phone || typeof phone !== 'string') {
    return ''
  }

  // 移除所有非数字字符
  const cleaned = phone.replace(/\D/g, '')

  // 检查是否为有效的中国手机号
  if (cleaned.length === 11 && /^1[3-9]\d{9}$/.test(cleaned)) {
    return cleaned.replace(/(\d{3})(\d{4})(\d{4})/, '$1****$3')
  }

  return phone
}

/**
 * 格式化身份证号
 * @param {string} idCard - 身份证号
 * @returns {string} 格式化的身份证号
 */
export const formatIdCard = (idCard) => {
  if (!idCard || typeof idCard !== 'string') {
    return ''
  }

  const cleaned = idCard.replace(/\s/g, '')

  if (cleaned.length === 18) {
    return cleaned.replace(/(\d{6})\d{8}(\d{4})/, '$1********$2')
  } else if (cleaned.length === 15) {
    return cleaned.replace(/(\d{6})\d{6}(\d{3})/, '$1******$2')
  }

  return idCard
}

/**
 * 格式化价格
 * @param {number} price - 价格
 * @param {string} currency - 货币符号
 * @param {number} decimals - 小数位数
 * @returns {string} 格式化的价格字符串
 */
export const formatPrice = (price, currency = '¥', decimals = 2) => {
  if (typeof price !== 'number' || isNaN(price)) {
    return `${currency}0.00`
  }

  return `${currency}${price.toFixed(decimals)}`
}

/**
 * 格式化播放次数
 * @param {number} count - 播放次数
 * @returns {string} 格式化的播放次数
 */
export const formatPlayCount = (count) => {
  const formatted = formatNumber(count)
  return `${formatted} 次播放`
}

/**
 * 格式化评论数
 * @param {number} count - 评论数
 * @returns {string} 格式化的评论数
 */
export const formatCommentCount = (count) => {
  if (!count || count === 0) {
    return '评论'
  }
  return formatNumber(count)
}

/**
 * 格式化点赞数
 * @param {number} count - 点赞数
 * @returns {string} 格式化的点赞数
 */
export const formatLikeCount = (count) => {
  if (!count || count === 0) {
    return '点赞'
  }
  return formatNumber(count)
}

/**
 * 验证并格式化URL
 * @param {string} url - URL地址
 * @param {string} defaultUrl - 默认URL
 * @returns {string} 格式化的URL
 */
export const formatUrl = (url, defaultUrl = '') => {
  if (!url || typeof url !== 'string') {
    return defaultUrl
  }

  // 如果是相对路径，添加协议
  if (url.startsWith('//')) {
    return `https:${url}`
  }

  // 如果没有协议，添加https
  if (!url.startsWith('http://') && !url.startsWith('https://')) {
    return `https://${url}`
  }

  return url
}

/**
 * 格式化颜色值
 * @param {string} color - 颜色值
 * @param {number} opacity - 透明度 (0-1)
 * @returns {string} 格式化的颜色值
 */
export const formatColor = (color, opacity = 1) => {
  if (!color || typeof color !== 'string') {
    return 'transparent'
  }

  // 如果已经是rgba格式
  if (color.startsWith('rgba')) {
    return color
  }

  // 如果是rgb格式
  if (color.startsWith('rgb')) {
    return color.replace('rgb', 'rgba').replace(')', `, ${opacity})`)
  }

  // 如果是十六进制格式
  if (color.startsWith('#')) {
    const hex = color.slice(1)
    const r = parseInt(hex.slice(0, 2), 16)
    const g = parseInt(hex.slice(2, 4), 16)
    const b = parseInt(hex.slice(4, 6), 16)
    return `rgba(${r}, ${g}, ${b}, ${opacity})`
  }

  return color
}

/**
 * 安全的JSON解析
 * @param {string} jsonString - JSON字符串
 * @param {any} defaultValue - 默认值
 * @returns {any} 解析结果
 */
export const safeJSONParse = (jsonString, defaultValue = null) => {
  try {
    return JSON.parse(jsonString)
  } catch (error) {
    console.warn('JSON解析失败:', error)
    return defaultValue
  }
}

/**
 * 安全的JSON字符串化
 * @param {any} value - 要字符串化的值
 * @param {string} defaultValue - 默认值
 * @returns {string} JSON字符串
 */
export const safeJSONStringify = (value, defaultValue = '{}') => {
  try {
    return JSON.stringify(value)
  } catch (error) {
    console.warn('JSON字符串化失败:', error)
    return defaultValue
  }
}

// 默认导出所有格式化函数
export default {
  formatTime,
  formatNumber,
  formatDuration,
  formatFileSize,
  formatTextLength,
  formatPhone,
  formatIdCard,
  formatPrice,
  formatPlayCount,
  formatCommentCount,
  formatLikeCount,
  formatUrl,
  formatColor,
  safeJSONParse,
  safeJSONStringify
}