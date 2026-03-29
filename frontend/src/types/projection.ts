/**
 * Shared TypeScript types for the FinPilot frontend
 */

export interface ProjectionInput {
  target_amount: number
  timeline_months: number
  monthly_contribution: number
  current_savings: number
  current_debt: number
  expected_return_rate: number
  inflation_rate: number
  debt_interest_rate: number
}

export interface ProjectionResult {
  is_achievable: boolean
  total_months: number
  final_savings: number
  final_debt: number
  final_net_worth: number
  total_contributions: number
  total_investment_growth: number
  monthly_projections: MonthlyProjectionData[]
  shortfall_amount: number
  recommended_monthly_increase: number
  break_even_month?: number
}

export interface MonthlyProjectionData {
  month: number
  year: number
  savings_balance: number
  debt_balance: number
  net_worth: number
  monthly_contribution: number
  investment_growth: number
  debt_payment: number
  cumulative_savings: number
  cumulative_investments: number
}
