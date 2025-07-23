import request from '@/utils/request'

export const getAiSummary = (data) => request({ url: '/ai/summary', method: 'POST', data })
export const getAiTTS = (data) => request({ url: '/ai/tts', method: 'POST', data }) 