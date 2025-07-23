import request from '@/utils/request'

export const recordPlay = (data) => request({ url: '/player/record', method: 'POST', data }) 