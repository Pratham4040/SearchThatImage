/**
 * API service – all fetch calls live here.
 * Components must NOT call fetch/axios directly.
 */

import axios from 'axios'

const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? '/api'

const api = axios.create({
  baseURL: BASE_URL,
  timeout: 30_000,
})

/**
 * Upload an image file to the backend.
 * @param {File} file - The image file to upload.
 * @returns {Promise<object>} The created image record.
 */
export const uploadImage = async (file) => {
  const formData = new FormData()
  formData.append('image', file)
  const { data } = await api.post('/images/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
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

export default api
