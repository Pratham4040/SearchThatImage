import { useState } from 'react'

/**
 * SearchBar component – a controlled text input that triggers a search callback.
 *
 * @param {object}   props
 * @param {Function} props.onSearch - Called with the query string when submitted.
 * @param {boolean}  props.loading  - Disables the button while a search is in progress.
 */
export function SearchBar({ onSearch, loading = false }) {
  const [query, setQuery] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (query.trim()) {
      onSearch(query.trim())
    }
  }

  return (
    <form onSubmit={handleSubmit} className="flex w-full gap-2">
      <input
        type="search"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search by tag (e.g. 'sunset', 'dog', 'city')…"
        className="flex-1 rounded-xl border border-gray-300 px-4 py-2.5 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-200 transition"
      />
      <button
        type="submit"
        disabled={loading || !query.trim()}
        className="rounded-xl bg-indigo-600 px-5 py-2.5 text-sm font-medium text-white hover:bg-indigo-700 disabled:cursor-not-allowed disabled:opacity-50 transition-colors"
      >
        {loading ? 'Searching…' : 'Search'}
      </button>
    </form>
  )
}
