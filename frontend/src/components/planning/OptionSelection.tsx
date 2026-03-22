/**
 * Option Card Selection Component
 *
 * Reusable component for selecting from a set of options.
 * Used for goal type selection and similar multi-choice questions.
 */

import React from 'react'

export interface Option {
  id: string
  label: string
  description?: string
  icon?: React.ReactNode
  disabled?: boolean
}

interface OptionSelectionProps {
  label: string
  options: Option[]
  selected: string | null
  onChange: (optionId: string) => void
  error?: string
  required?: boolean
  columns?: number
}

export const OptionSelection: React.FC<OptionSelectionProps> = ({
  label,
  options,
  selected,
  onChange,
  error,
  required = false,
  columns = 2,
}) => {
  return (
    <div className="mb-4">
      <label className="block text-sm font-medium text-gray-900 mb-4">
        {label} {required && <span className="text-red-500">*</span>}
      </label>

      <div
        className={`grid gap-3`}
        style={{
          gridTemplateColumns: `repeat(${columns}, minmax(0, 1fr))`,
        }}
      >
        {options.map((option) => (
          <button
            key={option.id}
            onClick={() => !option.disabled && onChange(option.id)}
            disabled={option.disabled}
            className={`
              p-4 text-left border rounded-lg transition-all duration-200
              ${
                selected === option.id
                  ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-500'
                  : 'border-gray-300 bg-white hover:border-blue-300'
              }
              ${option.disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
            `}
          >
            {option.icon && <div className="mb-2">{option.icon}</div>}

            <div className="font-medium text-sm text-gray-900">
              {option.label}
            </div>

            {option.description && (
              <div className="text-xs text-gray-600 mt-1">
                {option.description}
              </div>
            )}
          </button>
        ))}
      </div>

      {error && <p className="mt-2 text-sm text-red-600">{error}</p>}
    </div>
  )
}

export default OptionSelection
