export default function LoadingSpinner() {
  return (
    <div className="lg:col-span-1 flex items-center justify-center">
      <div className="bg-white rounded-lg shadow-md p-12 text-center">
        <div className="inline-block">
          <div className="w-16 h-16 rounded-full border-4 border-gray-300 border-t-blue-600 animate-spin"></div>
        </div>
        <p className="mt-6 text-gray-700 font-semibold">Analyzing differences...</p>
        <p className="text-gray-500 text-sm mt-2">This may take a few seconds</p>
      </div>
    </div>
  )
}
