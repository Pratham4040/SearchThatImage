import { useState } from 'react'
import { uploadImage } from '../services/api'

/**
 * ImageUpload component – handles image file selection and upload.
 *
 * @param {object}   props
 * @param {Function} props.onUploadSuccess - Callback called with the new image
 *                                           record after a successful upload.
 */
export function ImageUpload({ onUploadSuccess }) {
  const [file, setFile] = useState(null)
  const [preview, setPreview] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleFileChange = (e) => {
    const selected = e.target.files?.[0] ?? null
    setFile(selected)
    setError(null)
    if (selected) {
      setPreview(URL.createObjectURL(selected))
    } else {
      setPreview(null)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!file) {
      setError('Please select an image file.')
      return
    }
    setLoading(true)
    setError(null)
    try {
      const image = await uploadImage(file)
      setFile(null)
      setPreview(null)
      onUploadSuccess?.(image)
    } catch (err) {
      setError(err.response?.data?.error ?? 'Upload failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
      <h2 className="mb-4 text-xl font-semibold text-gray-800">Upload an Image</h2>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <label className="flex cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed border-indigo-300 bg-indigo-50 p-8 hover:bg-indigo-100 transition-colors">
          <span className="mb-2 text-sm text-gray-500">
            {file ? file.name : 'Click to choose a file or drag and drop'}
          </span>
          <input
            type="file"
            accept="image/*"
            className="hidden"
            onChange={handleFileChange}
          />
        </label>

        {preview && (
          <img
            src={preview}
            alt="Preview"
            className="h-48 w-full rounded-lg object-contain"
          />
        )}

        {error && <p className="text-sm text-red-600">{error}</p>}

        <button
          type="submit"
          disabled={loading || !file}
          className="rounded-xl bg-indigo-600 px-6 py-2.5 text-sm font-medium text-white hover:bg-indigo-700 disabled:cursor-not-allowed disabled:opacity-50 transition-colors"
        >
          {loading ? 'Uploading…' : 'Upload & Tag'}
        </button>
      </form>
    </div>
  )
}
