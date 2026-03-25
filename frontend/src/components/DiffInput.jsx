export default function DiffInput({ text1, setText1, text2, setText2, onCompare, onReset, loading }) {
  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="space-y-4">
          <div>
            <label htmlFor="text1" className="block text-sm font-semibold text-gray-700 mb-2">
              Original Text
            </label>
            <textarea
              id="text1"
              value={text1}
              onChange={(e) => setText1(e.target.value)}
              placeholder="Paste or type the original text here..."
              className="w-full h-64 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none focus:outline-none"
              disabled={loading}
            />
            <p className="text-xs text-gray-500 mt-2">{text1.length} characters</p>
          </div>

          <div>
            <label htmlFor="text2" className="block text-sm font-semibold text-gray-700 mb-2">
              Modified Text
            </label>
            <textarea
              id="text2"
              value={text2}
              onChange={(e) => setText2(e.target.value)}
              placeholder="Paste or type the modified text here..."
              className="w-full h-64 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none focus:outline-none"
              disabled={loading}
            />
            <p className="text-xs text-gray-500 mt-2">{text2.length} characters</p>
          </div>
        </div>

        <div className="flex gap-3 mt-6">
          <button
            onClick={onCompare}
            disabled={loading || !text1.trim() || !text2.trim()}
            className="flex-1 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-semibold py-3 px-6 rounded-lg transition duration-200 disabled:cursor-not-allowed"
          >
            {loading ? 'Comparing...' : 'Compare Texts'}
          </button>
          <button
            onClick={onReset}
            disabled={loading}
            className="flex-1 bg-gray-300 hover:bg-gray-400 disabled:bg-gray-400 text-gray-800 font-semibold py-3 px-6 rounded-lg transition duration-200 disabled:cursor-not-allowed"
          >
            Reset
          </button>
        </div>
      </div>
    </div>
  )
}
