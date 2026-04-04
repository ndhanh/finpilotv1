'use client'

import { useEffect } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { usePlanContext } from '@/context/PlanContext'
import { getTemplate, getTemplateStartRoute } from '@/lib/templates'

/**
 * Plan Wizard Page
 *
 * Route guard page that:
 * 1. Checks if user has selected a template
 * 2. Redirects to template selection if not
 * 3. Starts the template-specific wizard if template is selected
 */
export default function PlanPage() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const { planData, setSelectedTemplate } = usePlanContext()

  useEffect(() => {
    // Check if template is in URL params (e.g., ?template=home_purchase)
    const templateIdFromUrl = searchParams.get('template')
    const selectedTemplate = planData.selectedTemplate

    // If template in URL but not in context, set it
    if (templateIdFromUrl && !selectedTemplate) {
      const template = getTemplate(templateIdFromUrl)
      if (template) {
        setSelectedTemplate(template)
        // Navigate to template's start route
        const startRoute = getTemplateStartRoute(templateIdFromUrl)
        router.push(startRoute)
      } else {
        // Invalid template ID, redirect to template selection
        router.push('/plan-templates')
      }
      return
    }

    // If we have a selected template, navigate to its first step
    if (selectedTemplate) {
      const startRoute = getTemplateStartRoute(selectedTemplate.id)
      router.push(startRoute)
      return
    }

    // No template selected and no template in URL → redirect to template selection
    router.push('/plan-templates')
  }, [planData.selectedTemplate, searchParams, router, setSelectedTemplate])

  // Show loading state while redirecting
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
      <div className="text-center">
        <div className="inline-flex items-center justify-center mb-4">
          <div className="w-8 h-8 border-4 border-blue-500 border-t-blue-600 rounded-full animate-spin"></div>
        </div>
        <p className="text-gray-600">Đang tải kế hoạch của bạn...</p>
      </div>
    </div>
  )
}
