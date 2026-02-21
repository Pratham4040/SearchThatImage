import { BrowserRouter, Route, Routes } from 'react-router-dom'
import Home from './pages/Home'
import Upload from './pages/Upload'

/**
 * App – root component that declares client-side routes.
 * Uses functional components and React Router v6.
 */
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/upload" element={<Upload />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
