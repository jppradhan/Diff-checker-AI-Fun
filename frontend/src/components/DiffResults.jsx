import DiffCategory from './DiffCategory'

export default function DiffResults({ results }) {
  const { response, more_context } = results

  if (!response) {
    return null
  }

  const hasChanges = 
    (response.added && response.added.length > 0) ||
    (response.removed && response.removed.length > 0) ||
    (response.changed && response.changed.length > 0)

  return (
    <div className="space-y-6 lg:col-span-1">
      <div className="bg-white rounded-lg shadow-md p-6 sticky top-8">
        {!hasChanges ? (
          <div className="text-center py-8">
            <p className="text-gray-600 text-lg">No differences found</p>
            <p className="text-gray-500 text-sm mt-2">The texts are identical.</p>
          </div>
        ) : (
          <div className="space-y-4">
            <DiffCategory
              title="Added"
              items={response.added || []}
              type="add"
              icon="+"
            />
            <DiffCategory
              title="Removed"
              items={response.removed || []}
              type="remove"
              icon="−"
            />
            <DiffCategory
              title="Changed"
              items={response.changed || []}
              type="change"
              icon="~"
            />
          </div>
        )}
      </div>

      {more_context && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="font-semibold text-gray-900 mb-3">Analysis Summary</h3>
          <div className="bg-gray-50 rounded p-4 text-sm text-gray-700 max-h-64 overflow-y-auto">
            <p className="whitespace-pre-wrap">{more_context}</p>
          </div>
        </div>
      )}
    </div>
  )
}
