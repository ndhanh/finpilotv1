'use client'

import React, { useCallback } from 'react'
import { useRouter } from 'next/navigation'
import { useTemplateSelection } from '@/hooks/useTemplateSelection'
import { TemplateSelectionCard } from './TemplateSelectionCard'
import { usePlan } from '@/hooks/usePlan'

/**
 * Page component for selecting a plan template
 *
 * Displays available plan templates in a responsive grid
 * and handles template selection and navigation to the planning wizard
 */
export function TemplateSelectionPage() {
  const router = useRouter()
  const { templates, loading, error } = useTemplateSelection()
  const { setSelectedTemplate } = usePlan()

  const handleTemplateSelect = useCallback(
    (templateId: string) => {
      const template = templates.find((t) => t.id === templateId)
      if (template) {
        // Store selected template in plan context
        setSelectedTemplate(template)

        // Navigate to planning wizard start route
        // This would be template-specific, e.g., /plan/purchase-home/income
        router.push(`/plan/${templateId}/income`)
      }
    },
    [templates, setSelectedTemplate, router]
  )

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center py-12">
          <div className="inline-flex items-center justify-center">
            <div className="w-8 h-8 border-4 border-blue-500 border-t-blue-600 rounded-full animate-spin"></div>
          </div>
          <p className="mt-4 text-gray-600">Đang tải các mẫu kế hoạch...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center py-12 px-4 max-w-md">
          <div className="text-4xl mb-4">⚠️</div>
          <h1 className="text-2xl font-bold text-gray-900 mb-2">
            Có lỗi xảy ra
          </h1>
          <p className="text-gray-600 mb-6">
            Không thể tải các mẫu kế hoạch. Vui lòng thử lại sau.
          </p>
          <button
            onClick={() => window.location.reload()}
            className="bg-blue-500 text-white px-6 py-2 rounded-md font-semibold hover:bg-blue-600"
          >
            Thử lại
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4 sm:px-6 lg:px-8">
      {/* Header */}
      <div className="max-w-6xl mx-auto mb-12">
        <h1 className="text-4xl sm:text-5xl font-bold text-gray-900 mb-4">
          Chọn kế hoạch của bạn
        </h1>
        <p className="text-lg text-gray-600">
          Chọn một mẫu kế hoạch để bắt đầu quản lý tài chính của bạn
        </p>
      </div>

      {/* Templates Grid */}
      <div className="max-w-6xl mx-auto">
        {templates.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-500">Không có mẫu kế hoạch nào</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {templates.map((template) => (
              <TemplateSelectionCard
                key={template.id}
                template={template}
                onClick={handleTemplateSelect}
              />
            ))}
          </div>
        )}
      </div>

      {/* Footer Info */}
      <div className="max-w-6xl mx-auto mt-16 pt-8 border-t border-gray-300">
        <p className="text-center text-gray-600 text-sm">
          Bạn có thể thay đổi lựa chọn của mình bất cứ lúc nào trong các cài đặt
        </p>
      </div>
    </div>
  )
}

export default TemplateSelectionPage
