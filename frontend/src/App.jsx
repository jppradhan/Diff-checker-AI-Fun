import { useState, useEffect } from 'react'
import Header from './components/Header'
import DiffInput from './components/DiffInput'
import DiffResults from './components/DiffResults'
import LoadingSpinner from './components/LoadingSpinner'
import ErrorAlert from './components/ErrorAlert'
import { checkDiff } from './api'

function App() {
  const [text1, setText1] = useState('')
  const [text2, setText2] = useState('')
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleCompare = async () => {
    if (!text1.trim() || !text2.trim()) {
      setError('Both text fields must be filled')
      return
    }

    setError(null)
    setLoading(true)

    try {
      const data = await checkDiff(text1, text2)
      setResults(data)
    } catch (err) {
      setError(err.message)
      setResults(null)
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () => {
    setText1('')
    setText2('')
    setResults(null)
    setError(null)
  }

  const handleClear = () => {
    setError(null)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <Header />
      <main className="container mx-auto px-4 py-8 max-w-6xl">
        {error && <ErrorAlert message={error} onDismiss={handleClear} />}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <DiffInput
            text1={text1}
            setText1={setText1}
            text2={text2}
            setText2={setText2}
            onCompare={handleCompare}
            onReset={handleReset}
            loading={loading}
          />

          {loading && <LoadingSpinner />}
          {results && !loading && <DiffResults results={results} />}
        </div>
      </main>
    </div>
  )
}

export default App
