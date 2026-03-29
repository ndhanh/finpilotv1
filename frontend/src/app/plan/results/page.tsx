/**
 * Results Dashboard Page
 *
 * Displays projection results, recommendations, and options to save the plan
 */

'use client'

import React, { useState, useEffect } from 'react'
import {
  formatVND,
  formatMonthsRemaining,
  formatProgress,
} from '@/lib/formatting'
import { ProjectionChart } from '@/components/dashboard/ProjectionChart'
import SavePlanPrompt from '@/components/dashboard/SavePlanPrompt'
import { PlanProvider, usePlanContext } from '@/context/PlanContext'
import { projectionsApi, goalsApi } from '@/lib/api'

import { ProjectionResult, MonthlyProjectionData } from '@/types/projection'

interface ResultsDashboardProps {
  result: ProjectionResult
  targetAmount: number
}

const ResultsDashboard: React.FC<ResultsDashboardProps> = ({
  result,
  targetAmount,
}) => {
  const plan = usePlanContext()
  const [showSavePrompt, setShowSavePrompt] = useState(false)

  const monthsToTarget = result.break_even_month
    ? Math.floor(result.break_even_month / 12)
    : Math.floor(result.total_months / 12)

  const yearsToTarget = Math.floor(monthsToTarget / 12)
  const remainingMonths = monthsToTarget % 12

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Kết Quả Dự Báo Tài Chính
          </h1>
          <p className="text-gray-600">
            Phân tích chi tiết về khả năng đạt được mục tiêu của bạn
          </p>
        </div>

        {/* Achievement Status */}
        <div
          className={`mb-8 p-6 rounded-lg border-2 ${
            result.is_achievable
              ? 'border-green-500 bg-green-50'
              : 'border-yellow-500 bg-yellow-50'
          }`}
        >
          <div className="flex items-center justify-between">
            <div>
              <h2
                className={`text-2xl font-bold mb-2 ${
                  result.is_achievable ? 'text-green-900' : 'text-yellow-900'
                }`}
              >
                {result.is_achievable
                  ? '✓ Mục tiêu có thể đạt được'
                  : '⚠ Mục tiêu cần điều chỉnh'}
              </h2>

              {result.is_achievable ? (
                <p className="text-green-800">
                  Với {formatVND(plan.planData.monthlyContribution!)} tiết kiệm
                  hàng tháng, bạn sẽ đạt được mục tiêu trong{' '}
                  {yearsToTarget > 0
                    ? `${yearsToTarget} năm ${remainingMonths} tháng`
                    : `${remainingMonths} tháng`}
                  .
                </p>
              ) : (
                <div>
                  <p className="text-yellow-800 mb-2">
                    Với {formatVND(plan.planData.monthlyContribution!)} tiết
                    kiệm hàng tháng, thiếu {formatVND(result.shortfall_amount)}{' '}
                    để đạt mục tiêu.
                  </p>

                  <p className="text-yellow-800 font-medium">
                    Được cố gắng tăng khoản tiết kiệm hàng tháng lên ít nhất{' '}
                    {formatVND(
                      plan.planData.monthlyContribution! +
                        result.recommended_monthly_increase
                    )}
                  </p>
                </div>
              )}
            </div>

            <div className="text-right">
              <div className="text-4xl font-bold text-blue-600">
                {formatProgress((result.final_net_worth / targetAmount) * 100)}
              </div>
              <p className="text-gray-600 text-sm">Tiến độ</p>
            </div>
          </div>
        </div>

        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <p className="text-gray-600 text-sm mb-2">Tiết kiệm cuối cùng</p>
            <p className="text-2xl font-bold text-blue-600">
              {formatVND(result.final_savings)}
            </p>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <p className="text-gray-600 text-sm mb-2">Nợ cuối cùng</p>
            <p className="text-2xl font-bold text-red-600">
              {formatVND(result.final_debt)}
            </p>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <p className="text-gray-600 text-sm mb-2">Giá trị ròng</p>
            <p className="text-2xl font-bold text-green-600">
              {formatVND(result.final_net_worth)}
            </p>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <p className="text-gray-600 text-sm mb-2">Tổng đóng góp</p>
            <p className="text-2xl font-bold text-indigo-600">
              {formatVND(result.total_contributions)}
            </p>
          </div>
        </div>

        {/* Charts */}
        <div className="bg-white rounded-lg shadow p-8 mb-8">
          <ProjectionChart
            data={result.monthly_projections}
            title="Biểu Đồ Dự Báo"
            height={400}
            isAchievable={result.is_achievable}
            targetAmount={targetAmount}
          />
        </div>

        {/* Breakdown */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Phân Tích Đóng Góp
            </h3>

            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-gray-600">Tiền tiết kiệm:</span>
                <span className="font-semibold text-gray-900">
                  {formatVND(result.total_contributions)}
                </span>
              </div>

              <div className="flex justify-between">
                <span className="text-gray-600">Lợi nhuận đầu tư:</span>
                <span className="font-semibold text-green-600">
                  +{formatVND(result.total_investment_growth)}
                </span>
              </div>

              <hr className="my-3" />

              <div className="flex justify-between text-lg">
                <span className="text-gray-900 font-semibold">Tổng cộng:</span>
                <span className="text-blue-600 font-bold">
                  {formatVND(
                    result.total_contributions + result.total_investment_growth
                  )}
                </span>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Thông tin dự báo
            </h3>

            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-gray-600">Thời gian:</span>
                <span className="font-semibold text-gray-900">
                  {yearsToTarget} năm {remainingMonths} tháng
                </span>
              </div>

              <div className="flex justify-between">
                <span className="text-gray-600">Mục tiêu:</span>
                <span className="font-semibold text-gray-900">
                  {formatVND(targetAmount)}
                </span>
              </div>

              {result.is_achievable && (
                <div className="flex justify-between">
                  <span className="text-gray-600">Vượt mục tiêu:</span>
                  <span className="font-semibold text-green-600">
                    +{formatVND(result.final_net_worth - targetAmount)}
                  </span>
                </div>
              )}

              {!result.is_achievable && (
                <div className="flex justify-between">
                  <span className="text-gray-600">Thiếu:</span>
                  <span className="font-semibold text-red-600">
                    -{formatVND(result.shortfall_amount)}
                  </span>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex gap-4 justify-center">
          <button
            onClick={() => window.history.back()}
            className="px-6 py-3 border border-gray-300 rounded-lg text-gray-700 font-medium hover:bg-gray-50 transition-colors"
          >
            Quay Lại
          </button>

          <button
            onClick={() => setShowSavePrompt(true)}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors"
          >
            💾 Lưu Kế Hoạch
          </button>
        </div>

        {/* Save Prompt Modal */}
        {showSavePrompt && (
          <SavePlanPrompt
            result={result}
            onClose={() => setShowSavePrompt(false)}
          />
        )}
      </div>
    </div>
  )
}

/**
 * Results Page Component
 *
 * Fetches projection data from backend and renders the dashboard
 */
const ResultsPageContent: React.FC = () => {
  const plan = usePlanContext()
  const [result, setResult] = useState<ProjectionResult | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchProjection = async () => {
      if (!plan.isValidForProjection()) {
        setError('Thiếu thông tin cần thiết để tính toán dự báo')
        setLoading(false)
        return
      }

      try {
        console.log('Creating goal with data:', {
          name: plan.planData.goalName || 'Mục tiêu tài chính',
          goal_type: plan.planData.goalType || 'house_purchase',
          target_amount: plan.planData.targetAmount,
          target_date: plan.planData.targetDate,
          current_savings: plan.planData.currentSavings || 0,
        })

        // Create goal first
        const goalResponse = await goalsApi.create(1, {
          // Using dummy user_id for now
          name: plan.planData.goalName || 'Mục tiêu tài chính',
          description: plan.planData.goalDescription,
          goal_type: plan.planData.goalType || 'house_purchase',
          target_amount: plan.planData.targetAmount!,
          target_date: plan.planData.targetDate!,
          current_savings: plan.planData.currentSavings || 0,
          assumptions: {
            expected_return_rate: plan.planData.expectedReturnRate || 0.07,
            inflation_rate: plan.planData.inflationRate || 0.04,
            debt_interest_rate: plan.planData.debtInterestRate || 0.12,
          },
        })

        console.log('Goal creation response:', goalResponse)

        if (goalResponse.error) {
          throw new Error(goalResponse.error)
        }

        const goalId = goalResponse.data?.id
        console.log('Created goal with ID:', goalId)

        // Calculate projection
        const projectionInput = {
          target_amount: plan.planData.targetAmount!,
          timeline_months: plan.planData.timelineYears! * 12,
          monthly_contribution: plan.planData.monthlyContribution!,
          current_savings: plan.planData.currentSavings || 0,
          current_debt: plan.planData.currentDebt || 0,
          expected_return_rate: plan.planData.expectedReturnRate || 0.07,
          inflation_rate: plan.planData.inflationRate || 0.04,
          debt_interest_rate: plan.planData.debtInterestRate || 0.12,
        }
        console.log('Calculating projection with input:', projectionInput)

        const projectionResponse = await projectionsApi.calculate(
          goalId,
          1,
          projectionInput
        )

        console.log('Projection response:', projectionResponse)

        if (projectionResponse.error) {
          throw new Error(projectionResponse.error)
        }

        setResult(projectionResponse.data!)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Lỗi không xác định')
      } finally {
        setLoading(false)
      }
    }

    fetchProjection()
  }, [plan])

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Đang tính toán dự báo tài chính...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-red-50 to-pink-100 flex items-center justify-center">
        <div className="text-center max-w-md">
          <div className="text-6xl mb-4">⚠️</div>
          <h1 className="text-2xl font-bold text-red-900 mb-2">
            Lỗi Tính Toán
          </h1>
          <p className="text-red-700 mb-4">{error}</p>
          <button
            onClick={() => window.history.back()}
            className="px-6 py-3 bg-red-600 text-white rounded-lg font-medium hover:bg-red-700 transition-colors"
          >
            Quay Lại
          </button>
        </div>
      </div>
    )
  }

  if (!result) {
    return null
  }

  return (
    <ResultsDashboard
      result={result}
      targetAmount={plan.planData.targetAmount!}
    />
  )
}

/**
 * Main Results Page Component with PlanProvider
 */
const ResultsPage: React.FC = () => {
  return (
    <PlanProvider>
      <ResultsPageContent />
    </PlanProvider>
  )
}

export default ResultsPage
