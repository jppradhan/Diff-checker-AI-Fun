import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const checkDiff = async (text1, text2) => {
  try {
    const response = await api.post('/check_diff_agent', {
      text1,
      text2,
    })
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.detail || error.message || 'Failed to check diff')
  }
}

export const getHealth = async () => {
  try {
    const response = await api.get('/health')
    return response.data
  } catch (error) {
    throw new Error('Failed to get health status')
  }
}

export default api
