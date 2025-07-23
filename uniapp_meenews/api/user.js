import request from '@/utils/request'

export const getUserInfo = () => request({ url: '/user/info' })
export const login = (data) => request({ url: '/user/login', method: 'POST', data })
export const logout = () => request({ url: '/user/logout', method: 'POST' })
export const register = (data) => request({ url: '/user/register', method: 'POST', data })
export const updateProfile = (data) => request({ url: '/users/profile', method: 'PUT', data })
export const followUser = (userId, follow = true) =>
  request({ url: `/users/${userId}/follow`, method: 'POST', data: { follow } })
export const getFavorites = (params = {}) => request({ url: '/users/favorites', method: 'GET', data: params })
export const getRecentPlayed = (params = {}) => request({ url: '/users/recent-played', method: 'GET', data: params }) 