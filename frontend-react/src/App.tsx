import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Layout } from './components/Layout'
import { Home } from './pages/Home'
import { Design } from './pages/Design'
import { Results } from './pages/Results'
import { Editor } from './pages/Editor'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="design" element={<Design />} />
          <Route path="results" element={<Results />} />
          <Route path="editor" element={<Editor />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App

// Made with Bob
