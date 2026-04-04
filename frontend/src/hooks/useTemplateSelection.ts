/**
 * Hook for template selection and management
 *
 * Provides fetching and caching of planning templates from the backend API
 * with loading and error state management.
 */

import { useState, useEffect } from 'react'
import { PlanTemplate } from '@/types/template'
import { templatesApi } from '@/lib/api'
import { getAllTemplates, getTemplate } from '@/lib/templates'

interface UseTemplateSelectionReturn {
  templates: PlanTemplate[]
  loading: boolean
  error: string | null
  getTemplate: (id: string) => PlanTemplate | undefined
}

/**
 * Hook to fetch and manage plan templates
 *
 * Fetches templates from backend on mount, falls back to local definitions
 * if API is unavailable. Provides template list and lookup utilities.
 *
 * @returns Object with templates, loading state, error state, and lookup function
 */
export function useTemplateSelection(): UseTemplateSelectionReturn {
  const [templates, setTemplates] = useState<PlanTemplate[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchTemplates = async () => {
      try {
        setLoading(true)
        const response = await templatesApi.getAll()

        if (response.data) {
          setTemplates(response.data.templates)
          setError(null)
        } else {
          // Fallback to local templates if API fails
          console.warn(
            'Failed to fetch templates from API, using local definitions'
          )
          setTemplates(getAllTemplates())
          setError(response.error || 'Failed to load templates')
        }
      } catch (err) {
        console.error('Error fetching templates:', err)
        // Fallback to local templates
        setTemplates(getAllTemplates())
        setError('Unable to load templates')
      } finally {
        setLoading(false)
      }
    }

    fetchTemplates()
  }, [])

  return {
    templates,
    loading,
    error,
    getTemplate,
  }
}
