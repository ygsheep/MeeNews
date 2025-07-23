import { useUserStore } from '@/store/user'

const BASE_URL = 'http://localhost:8090'

const request = (options) => {
  const userStore = useUserStore()
  return new Promise((resolve, reject) => {
    uni.request({
      url: BASE_URL + options.url,
      method: options.method || 'GET',
      data: options.data,
      header: {
        'Authorization': userStore.token ? `Bearer ${userStore.token}` : '',
        'Content-Type': 'application/json'
      },
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data)
        } else {
          uni.showToast({ title: res.data.message || '请求失败', icon: 'none' })
          reject(res.data)
        }
      },
      fail: (err) => {
        uni.showToast({ title: '网络错误', icon: 'none' })
        reject(err)
      }
    })
  })
}

const http = request

// 辅助函数：将对象拼接为url查询字符串
function buildQuery(url, params) {
  const query = Object.entries(params)
    .filter(([k, v]) => v !== undefined && v !== null && v !== '')
    .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(v)}`)
    .join('&')
  return query ? `${url}?${query}` : url
}

// 支持 http.get/post 风格
http.get = (url, params = {}) => {
  return http({ url: buildQuery(url, params), method: 'GET' })
}
http.post = (url, data = {}) => {
  return http({ url, method: 'POST', data })
}
http.put = (url, data = {}) => {
  return http({ url, method: 'PUT', data })
}
http.delete = (url, data = {}) => {
  return http({ url, method: 'DELETE', data })
}

export default request
export { http } 