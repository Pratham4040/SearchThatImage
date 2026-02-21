/**
 * ImageCard component – displays a single image with its AI-generated tags.
 *
 * @param {object}   props
 * @param {object}   props.image - Image record returned by the API.
 */
import { BASE_URL, getDownloadUrl } from '../services/api'

export function ImageCard({ image, onDelete }) {
  const filename = image.filename || image.file_path?.split(/[\\/]/).pop()
  const imageSrc = filename
    ? `${BASE_URL}/images/file/${encodeURIComponent(filename)}`
    : ''

  return (
    <div className="group overflow-hidden rounded-2xl border border-gray-200 bg-white shadow-sm hover:shadow-md transition-shadow">
      <div className="aspect-square overflow-hidden bg-gray-100">
        <img
          src={imageSrc}
          alt={image.original_filename}
          className="h-full w-full object-cover group-hover:scale-105 transition-transform duration-300"
          loading="lazy"
        />
      </div>

      <div className="p-4">
        <p
          className="mb-2 truncate text-sm font-medium text-gray-700"
          title={image.original_filename}
        >
          {image.original_filename}
        </p>

        {image.tags.length > 0 ? (
          <div className="flex flex-wrap gap-1">
            {image.tags.map((tag) => (
              <span
                key={tag}
                className="rounded-full bg-indigo-100 px-2 py-0.5 text-xs text-indigo-700"
              >
                {tag}
              </span>
            ))}
          </div>
        ) : (
          <p className="text-xs text-gray-400">No tags available</p>
        )}

        <div className="mt-3 flex items-center gap-2">
          <a
            href={getDownloadUrl(image.id)}
            className="rounded-lg border border-indigo-200 px-3 py-1.5 text-xs text-indigo-700 hover:bg-indigo-50"
          >
            Download
          </a>
          <button
            type="button"
            onClick={() => onDelete?.(image)}
            className="rounded-lg border border-red-200 px-3 py-1.5 text-xs text-red-600 hover:bg-red-50"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  )
}
