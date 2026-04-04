'use client'

import React from 'react'
import { PlanTemplate } from '@/types/template'

interface TemplateSelectionCardProps {
  template: PlanTemplate
  onClick: (id: string) => void
  disabled?: boolean
}

/**
 * Card component for displaying a plan template option
 *
 * Shows template icon, name, description and appropriate action button
 * (either "Bắt đầu" for available or "Sắp có" for coming soon)
 */
export function TemplateSelectionCard({
  template,
  onClick,
  disabled = false,
}: TemplateSelectionCardProps) {
  const isAvailable = template.status === 'available'
  const isDisabled = disabled || !isAvailable

  const handleClick = () => {
    if (!isDisabled) {
      onClick(template.id)
    }
  }

  return (
    <div
      className={`
        relative overflow-hidden rounded-lg border-2 transition-all
        ${
          isDisabled
            ? 'border-gray-300 bg-gray-50 opacity-75'
            : 'border-blue-500 bg-white hover:shadow-lg hover:border-blue-600'
        }
      `}
    >
      {/* Coming Soon Badge */}
      {!isAvailable && (
        <div className="absolute top-4 right-4 z-10">
          <div className="inline-flex items-center gap-1 rounded-full bg-yellow-100 px-3 py-1">
            <span className="text-xs font-semibold text-yellow-800">
              Sắp có
            </span>
          </div>
        </div>
      )}

      {/* Card Content */}
      <div className="p-6">
        {/* Icon */}
        <div className="text-5xl mb-4">{template.icon}</div>

        {/* Title */}
        <h3 className="text-xl font-bold text-gray-900 mb-2">
          {template.name_vi}
        </h3>

        {/* Description */}
        <p className="text-gray-600 text-sm mb-6 leading-relaxed">
          {template.description_vi}
        </p>

        {/* Button */}
        <button
          onClick={handleClick}
          disabled={isDisabled}
          className={`
            w-full py-2 px-4 rounded-md font-semibold transition-all
            ${
              isDisabled
                ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                : 'bg-blue-500 text-white hover:bg-blue-600 active:bg-blue-700'
            }
          `}
          aria-label={`${isAvailable ? 'Bắt đầu' : 'Sắp có'} ${template.name_vi}`}
        >
          {isAvailable ? 'Bắt đầu' : 'Sắp có'}
        </button>

        {/* Tooltip for coming soon */}
        {!isAvailable && (
          <div className="mt-3 text-xs text-gray-500 text-center">
            Tính năng này sắp được phát hành
          </div>
        )}
      </div>
    </div>
  )
}

export default TemplateSelectionCard
