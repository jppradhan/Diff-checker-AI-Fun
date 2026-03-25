export default function Header() {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="container mx-auto px-4 py-6 max-w-6xl">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Diff Check using AI</h1>
            <p className="text-gray-600 mt-1">Compare texts with AI-powered analysis. We don't store any data</p>
          </div>
          <div className="text-right text-sm text-gray-500">
            <p>Powered by Pradhan</p>
          </div>
        </div>
      </div>
    </header>
  )
}
