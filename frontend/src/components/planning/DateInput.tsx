/**
 * Date Input Component
 *
 * Component for selecting target dates in the planning flow.
 * Includes validation to ensure future dates and friendly formatting.
 */

import React, { useCallback } from 'react'

interface DateInputProps {
  label: string
  value: string | null
  onChange: (date: string) => void
  hint?: string
  error?: string
  disabled?: boolean
  required?: boolean
  minDate?: Date
}

export const DateInput: React.FC<DateInputProps> = ({
  label,
  value,
  onChange,
  hint,
  error,
  disabled = false,
  required = false,
  minDate,
}) => {
  const handleChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      onChange(e.target.value)
    },
    [onChange]
  )

  // Default minimum date is today
  const min = minDate
    ? minDate.toISOString().split('T')[0]
    : new Date().toISOString().split('T')[0]

  return (
    <div className="mb-4">
      <label className="block text-sm font-medium text-gray-900 mb-2">
        {label} {required && <span className="text-red-500">*</span>}
      </label>

      <input
        type="date"
        value={value || ''}
        onChange={handleChange}
        disabled={disabled}
        min={min}
        className={`
          w-full px-3 py-2 border rounded-lg
          transition-colors duration-200
          ${
            error
              ? 'border-red-500 bg-red-50'
              : 'border-gray-300 focus:border-blue-500 focus:ring-1 focus:ring-blue-500'
          }
          ${disabled ? 'bg-gray-100 cursor-not-allowed' : 'bg-white'}
        `}
      />

      {error && <p className="mt-1 text-sm text-red-600">{error}</p>}

      {hint && <p className="mt-1 text-sm text-gray-600">{hint}</p>}
    </div>
  )
}

export default DateInput
