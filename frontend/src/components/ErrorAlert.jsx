export default function ErrorAlert({ message, onDismiss }) {
  return (
    <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4 flex items-start justify-between">
      <div className="flex items-start gap-3">
        <div className="text-red-600 font-bold text-xl mt-0.5">⚠</div>
        <div>
          <h3 className="font-semibold text-red-900">Error</h3>
          <p className="text-red-800 text-sm mt-1">{message}</p>
        </div>
      </div>
      <button
        onClick={onDismiss}
        className="text-red-600 hover:text-red-800 font-bold text-xl"
        aria-label="Close"
      >
        ×
      </button>
    </div>
  )
}
