/**
 * usePlan Hook
 *
 * Custom hook for managing plan data with progressive capture
 * and localStorage persistence during the onboarding flow.
 */

import { useState, useCallback, useEffect } from 'react'
import { PlanTemplate } from '@/types/template'

export interface PlanData {
  // Template selection
  selectedTemplate?: PlanTemplate | null
  templateId?: string

  // Basic info
  goalType?: string
  goalName?: string
  goalDescription?: string

  // Financial info
  targetAmount?: number
  currentSavings?: number
  currentDebt?: number
  monthlyContribution?: number

  // Timeline
  targetDate?: string // ISO date string
  timelineYears?: number

  // Assumptions
  expectedReturnRate?: number // 0-1 scale (e.g., 0.07 = 7%)
  inflationRate?: number
  debtInterestRate?: number

  // Step tracking
  completedSteps?: number[]
  currentStep?: number
}

const STORAGE_KEY = 'finpilot_plan_draft'

export const usePlan = () => {
  const [planData, setPlanData] = useState<PlanData>(() => {
    // Initialize from localStorage if available
    if (typeof window !== 'undefined') {
      const saved = localStorage.getItem(STORAGE_KEY)
      return saved ? JSON.parse(saved) : {}
    }
    return {}
  })

  const [isDirty, setIsDirty] = useState(false)

  // Persist to localStorage whenever planData changes
  useEffect(() => {
    if (typeof window !== 'undefined' && isDirty) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(planData))
    }
  }, [planData, isDirty])

  // Update a single field
  const updateField = useCallback(
    <K extends keyof PlanData>(field: K, value: PlanData[K]) => {
      setPlanData((prev) => ({
        ...prev,
        [field]: value,
      }))
      setIsDirty(true)
    },
    []
  )

  // Update multiple fields at once
  const updateMultiple = useCallback((updates: Partial<PlanData>) => {
    setPlanData((prev) => ({
      ...prev,
      ...updates,
    }))
    setIsDirty(true)
  }, [])

  // Mark a step as completed
  const completeStep = useCallback((stepNumber: number) => {
    setPlanData((prev) => {
      const completed = [...(prev.completedSteps || [])]
      if (!completed.includes(stepNumber)) {
        completed.push(stepNumber)
      }
      return {
        ...prev,
        completedSteps: completed,
        currentStep: stepNumber + 1,
      }
    })
    setIsDirty(true)
  }, [])

  // Get progress as percentage
  const getProgress = useCallback((): number => {
    const totalSteps = 6 // Total number of onboarding steps
    const completed = planData.completedSteps?.length || 0
    return Math.round((completed / totalSteps) * 100)
  }, [planData.completedSteps])

  // Check if a field is complete
  const isFieldComplete = useCallback(
    (field: keyof PlanData): boolean => {
      const value = planData[field]
      return value !== undefined && value !== null && value !== ''
    },
    [planData]
  )

  // Set selected template
  const setSelectedTemplate = useCallback((template: PlanTemplate | null) => {
    setPlanData((prev) => ({
      ...prev,
      selectedTemplate: template,
      templateId: template?.id || undefined,
    }))
    setIsDirty(true)
  }, [])

  // Validate plan has minimum required data
  const isValidForProjection = useCallback((): boolean => {
    return (
      isFieldComplete('targetAmount') &&
      isFieldComplete('currentSavings') &&
      isFieldComplete('monthlyContribution') &&
      isFieldComplete('targetDate') &&
      planData.targetAmount! > 0 &&
      planData.monthlyContribution! >= 0
    )
  }, [planData, isFieldComplete])

  // Clear draft (for new plan or after save)
  const clearDraft = useCallback(() => {
    setPlanData({})
    setIsDirty(false)
    if (typeof window !== 'undefined') {
      localStorage.removeItem(STORAGE_KEY)
    }
  }, [])

  // Get summary of plan data
  const getSummary = useCallback((): Partial<PlanData> => {
    return {
      goalType: planData.goalType,
      goalName: planData.goalName,
      targetAmount: planData.targetAmount,
      currentSavings: planData.currentSavings,
      monthlyContribution: planData.monthlyContribution,
      targetDate: planData.targetDate,
    }
  }, [planData])

  return {
    // State
    planData,
    isDirty,

    // Actions
    updateField,
    updateMultiple,
    completeStep,
    clearDraft,
    setSelectedTemplate,

    // Queries
    getProgress,
    isFieldComplete,
    isValidForProjection,
    getSummary,
  }
}

export default usePlan
