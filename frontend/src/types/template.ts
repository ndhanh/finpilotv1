/**
 * Template type definitions for plan template selection
 */

export interface PlanTemplate {
  id: string
  name_vi: string
  description_vi: string
  icon: string
  status: 'available' | 'coming_soon'
  wizard_steps: string[]
}

export type TemplateId = 'home_purchase' | 'emergency_fund'

export interface TemplatesResponse {
  templates: PlanTemplate[]
  total_count: number
}
