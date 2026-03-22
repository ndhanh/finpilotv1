/**
 * Plan Context
 *
 * Provides global state management for the financial plan data
 * throughout the application, especially during the onboarding flow.
 */

import React, { createContext, useContext, ReactNode } from 'react'
import { usePlan, PlanData } from '@/hooks/usePlan'

interface PlanContextType {
  planData: PlanData
  isDirty: boolean
  updateField: <K extends keyof PlanData>(field: K, value: PlanData[K]) => void
  updateMultiple: (updates: Partial<PlanData>) => void
  completeStep: (stepNumber: number) => void
  clearDraft: () => void
  getProgress: () => number
  isFieldComplete: (field: keyof PlanData) => boolean
  isValidForProjection: () => boolean
  getSummary: () => Partial<PlanData>
}

const PlanContext = createContext<PlanContextType | undefined>(undefined)

interface PlanProviderProps {
  children: ReactNode
}

/**
 * Provider component for PlanContext
 * Wraps the application to provide plan state to all components
 */
export const PlanProvider: React.FC<PlanProviderProps> = ({ children }) => {
  const planHook = usePlan()

  return (
    <PlanContext.Provider value={planHook}>{children}</PlanContext.Provider>
  )
}

/**
 * Hook to use the Plan context
 * @throws Error if used outside of PlanProvider
 */
export const usePlanContext = (): PlanContextType => {
  const context = useContext(PlanContext)

  if (!context) {
    throw new Error(
      'usePlanContext must be used within a PlanProvider. ' +
        'Wrap your component tree with <PlanProvider> at a higher level.'
    )
  }

  return context
}

/**
 * Higher-order component to inject PlanContext
 */
export const withPlanContext = <P extends object>(
  Component: React.ComponentType<P & { plan: PlanContextType }>
): React.FC<P> => {
  return (props: P) => {
    const plan = usePlanContext()
    return <Component {...props} plan={plan} />
  }
}

export default PlanContext
