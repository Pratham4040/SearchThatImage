import { useState } from 'react'
import { ImageUpload } from '../components/ImageUpload'

/**
 * Upload page – allows users to upload a new image to be tagged by AI.
 */
export default function Upload() {
  const [uploaded, setUploaded] = useState(null)

  const handleSuccess = (image) => {
    setUploaded(image)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <a href="/" className="text-2xl font-bold text-indigo-600">
            SearchThatImage
          </a>
          <a
            href="/"
            className="text-sm text-indigo-600 underline hover:no-underline"
          >
            ← Back to gallery
          </a>
        </div>
      </header>

      <main className="mx-auto max-w-lg px-6 py-12">
        <ImageUpload onUploadSuccess={handleSuccess} />

        {uploaded && (
          <div className="mt-6 rounded-2xl border border-green-200 bg-green-50 p-4">
            <p className="mb-2 font-medium text-green-800">
              ✅ Upload successful!
            </p>
            <p className="mb-1 text-sm text-gray-700">
              <strong>File:</strong> {uploaded.original_filename}
            </p>
            <div className="flex flex-wrap gap-1">
              {uploaded.tags.map((tag) => (
                <span
                  key={tag}
                  className="rounded-full bg-indigo-100 px-2 py-0.5 text-xs text-indigo-700"
                >
                  {tag}
                </span>
              ))}
            </div>
            <a
              href="/"
              className="mt-3 inline-block text-sm text-indigo-600 underline"
            >
              View in gallery →
            </a>
          </div>
        )}
      </main>
    </div>
  )
}
