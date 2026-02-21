/**
 * API service – all fetch calls live here.
 * Components must NOT call fetch/axios directly.
 */

import axios from 'axios'

const RAW_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? '/api'
const NORMALIZED_BASE = RAW_BASE_URL.replace(/\/$/, '')
export const BASE_URL = NORMALIZED_BASE.endsWith('/api')
  ? NORMALIZED_BASE
  : `${NORMALIZED_BASE}/api`

console.log('🔗 API BASE_URL:', BASE_URL)

const api = axios.create({
  baseURL: BASE_URL,
  timeout: 120_000,  // 120 seconds – allows time for AI tag generation
})

// Add request interceptor for debugging
api.interceptors.request.use(
  (config) => {
    console.log(`📤 ${config.method.toUpperCase()} ${BASE_URL}${config.url}`)
    return config
  },
  (error) => {
    console.error('❌ Request setup error:', error)
    return Promise.reject(error)
  }
)

// Add response interceptor for debugging
api.interceptors.response.use(
  (response) => {
    console.log(`✅ ${response.status} received`)
    return response
  },
  (error) => {
    console.error(`❌ ${error.response?.status || 'NETWORK'} error:`, error.message)
    return Promise.reject(error)
  }
)

/**
 * Upload an image file to the backend.
 * @param {File} file - The image file to upload.
 * @returns {Promise<object>} The created image record.
 */
export const uploadImage = async (file) => {
  const formData = new FormData()
  formData.append('image', file)
  
  // Don't manually set Content-Type header – axios + FormData handle it automatically
  const { data } = await api.post('/images/upload', formData)
  return data
}

/**
 * Fetch all uploaded images (paginated).
 * @param {number} page  - Page number (1-based).
 * @param {number} limit - Results per page.
 * @returns {Promise<object>} Paginated image list.
 */
export const fetchImages = async (page = 1, limit = 20) => {
  const { data } = await api.get('/images/', { params: { page, limit } })
  return data
}

/**
 * Search images by tag keywords.
 * @param {string} query - The search query.
 * @returns {Promise<object>} Search results.
 */
export const searchImages = async (query) => {
  const { data } = await api.get('/search/', { params: { q: query } })
  return data
}

/**
 * Fetch a single image by ID.
 * @param {number} imageId - Primary key of the image.
 * @returns {Promise<object>} Image record.
 */
export const fetchImageById = async (imageId) => {
  const { data } = await api.get(`/images/${imageId}`)
  return data
}

/**
 * Delete a single image by ID.
 * @param {number} imageId - Primary key of the image.
 * @returns {Promise<object>} Delete result.
 */
export const deleteImage = async (imageId) => {
  const { data } = await api.delete(`/images/${imageId}`)
  return data
}

/**
 * Build a download URL for an image by ID.
 * @param {number} imageId - Primary key of the image.
 * @returns {string} Download URL.
 */
export const getDownloadUrl = (imageId) => `${BASE_URL}/images/${imageId}/download`

export default api
