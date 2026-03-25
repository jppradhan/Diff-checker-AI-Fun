const typeStyles = {
  add: {
    bg: 'bg-green-50',
    border: 'border-l-4 border-green-500',
    badge: 'bg-green-100 text-green-800',
    icon: 'text-green-600',
  },
  remove: {
    bg: 'bg-red-50',
    border: 'border-l-4 border-red-500',
    badge: 'bg-red-100 text-red-800',
    icon: 'text-red-600',
  },
  change: {
    bg: 'bg-blue-50',
    border: 'border-l-4 border-blue-500',
    badge: 'bg-blue-100 text-blue-800',
    icon: 'text-blue-600',
  },
}

export default function DiffCategory({ title, items, type, icon }) {
  const styles = typeStyles[type]
  const isEmpty = !items || items.length === 0

  return (
    <div className={`rounded-lg overflow-hidden`}>
      <div className={`${styles.badge} px-4 py-2 flex items-center justify-between`}>
        <span className="font-semibold flex items-center gap-2">
          <span className={`${styles.icon} font-bold text-lg`}>{icon}</span>
          {title}
        </span>
        <span className="text-sm font-medium">{items.length}</span>
      </div>

      {isEmpty ? (
        <div className={`${styles.bg} ${styles.border} px-4 py-3 text-sm text-gray-600`}>
          No {title.toLowerCase()} items
        </div>
      ) : (
        <div className={`${styles.bg} ${styles.border}`}>
          <ul className="divide-y divide-gray-200">
            {items.map((item, index) => (
              <li key={index} className="px-4 py-3 text-sm text-gray-700 hover:bg-white transition">
                <div className="break-words font-mono text-xs bg-white bg-opacity-50 rounded p-2 mt-1">
                  {item}
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}
