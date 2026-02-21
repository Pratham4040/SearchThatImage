import { useEffect, useState } from 'react'
import { ImageCard } from '../components/ImageCard'
import { SearchBar } from '../components/SearchBar'
import { fetchImages, searchImages } from '../services/api'

/**
 * Home page – lists all images and provides search + upload navigation.
 */
export default function Home() {
  const [images, setImages] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchLoading, setSearchLoading] = useState(false)
  const [error, setError] = useState(null)
  const [searchQuery, setSearchQuery] = useState('')

  const loadImages = async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await fetchImages()
      setImages(data.images || [])
    } catch {
      setError('Failed to load images. Is the backend running?')
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = async (query) => {
    setSearchQuery(query)
    setSearchLoading(true)
    setError(null)
    try {
      const data = await searchImages(query)
      setImages(data.results || [])
    } catch {
      setError('Search failed. Please try again.')
    } finally {
      setSearchLoading(false)
    }
  }

  const handleClear = () => {
    setSearchQuery('')
    loadImages()
  }

  useEffect(() => {
    loadImages()
  }, [])

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <h1 className="text-2xl font-bold text-indigo-600">SearchThatImage</h1>
          <a
            href="/upload"
            className="rounded-xl bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700 transition-colors"
          >
            + Upload Image
          </a>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-6 py-8">
        {/* Search */}
        <div className="mb-8 flex flex-col gap-2">
          <SearchBar onSearch={handleSearch} loading={searchLoading} />
          {searchQuery && (
            <div className="flex items-center gap-2 text-sm text-gray-600">
              <span>
                Showing results for <strong>"{searchQuery}"</strong>
              </span>
              <button
                onClick={handleClear}
                className="text-indigo-600 underline hover:no-underline"
              >
                Clear
              </button>
            </div>
          )}
        </div>

        {/* States */}
        {loading && (
          <p className="text-center text-gray-500">Loading images…</p>
        )}
        {error && (
          <p className="text-center text-red-500">{error}</p>
        )}
        {!loading && !error && images.length === 0 && (
          <p className="text-center text-gray-400">
            No images found.{' '}
            <a href="/upload" className="text-indigo-600 underline">
              Upload one!
            </a>
          </p>
        )}

        {/* Grid */}
        {!loading && images.length > 0 && (
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5">
            {images.map((image) => (
              <ImageCard key={image.id} image={image} />
            ))}
          </div>
        )}
      </main>
    </div>
  )
}
