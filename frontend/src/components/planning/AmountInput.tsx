/**
 * Amount Input Component
 *
 * Reusable component for capturing VND amounts from users.
 * Includes formatting, validation, and helpful guidance.
 */

import React, { useState, useCallback } from 'react'
import { formatVND, parseVND } from '@/lib/formatting'

interface AmountInputProps {
  label: string
  value: number | null
  onChange: (amount: number) => void
  placeholder?: string
  hint?: string
  error?: string
  disabled?: boolean
  min?: number
  max?: number
  required?: boolean
  example?: string
}

export const AmountInput: React.FC<AmountInputProps> = ({
  label,
  value,
  onChange,
  placeholder = '0 ₫',
  hint,
  error,
  disabled = false,
  min = 0,
  max,
  required = false,
  example,
}) => {
  const [displayValue, setDisplayValue] = useState(
    value ? formatVND(value, false) : ''
  )

  const handleChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const input = e.target.value
      setDisplayValue(input)

      // Parse the input to get numeric value
      const parsed = parseVND(input)

      // Validate bounds
      if (parsed >= min && (!max || parsed <= max)) {
        onChange(parsed)
      }
    },
    [onChange, min, max]
  )

  const handleBlur = useCallback(() => {
    if (displayValue && value) {
      setDisplayValue(formatVND(value, false))
    }
  }, [displayValue, value])

  return (
    <div className="mb-4">
      <label className="block text-sm font-medium text-gray-900 mb-2">
        {label} {required && <span className="text-red-500">*</span>}
      </label>

      <div className="relative">
        <input
          type="text"
          value={displayValue}
          onChange={handleChange}
          onBlur={handleBlur}
          placeholder={placeholder}
          disabled={disabled}
          className={`
            w-full px-3 py-2 pr-8 border rounded-lg text-right
            transition-colors duration-200
            ${
              error
                ? 'border-red-500 bg-red-50'
                : 'border-gray-300 focus:border-blue-500 focus:ring-1 focus:ring-blue-500'
            }
            ${disabled ? 'bg-gray-100 cursor-not-allowed' : 'bg-white'}
          `}
        />
        <span className="absolute right-3 top-2.5 text-gray-500 text-sm">
          ₫
        </span>
      </div>

      {error && <p className="mt-1 text-sm text-red-600">{error}</p>}

      {hint && <p className="mt-1 text-sm text-gray-600">{hint}</p>}

      {example && (
        <p className="mt-1 text-xs text-gray-500">Ví dụ: {example}</p>
      )}
    </div>
  )
}

export default AmountInput
