/**
 * Full projection dashboard: metrics + Recharts visualization.
 */

'use client'

import React, { useState } from 'react'
import {
  formatVND,
  formatProgress,
} from '@/lib/formatting'
import { ProjectionChart } from '@/components/dashboard/ProjectionChart'
import SavePlanPrompt from '@/components/dashboard/SavePlanPrompt'
import { ProjectionResult } from '@/types/projection'

export interface ProjectionDashboardViewProps {
  result: ProjectionResult
  targetAmount: number
  monthlyContribution: number
}

export function ProjectionDashboardView({
  result,
  targetAmount,
  monthlyContribution,
}: ProjectionDashboardViewProps) {
  const [showSavePrompt, setShowSavePrompt] = useState(false)

  const monthsToGoal =
    result.is_achievable && result.break_even_month != null
      ? result.break_even_month
      : result.total_months

  const yearsToTarget = Math.floor(monthsToGoal / 12)
  const remainingMonths = monthsToGoal % 12

  const timePhrase =
    yearsToTarget > 0
      ? `${yearsToTarget} năm${remainingMonths > 0 ? ` ${remainingMonths} tháng` : ''}`
      : `${remainingMonths} tháng`

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-6xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Kết quả dự báo tài chính
          </h1>
          <p className="text-gray-600">
            Phân tích từ máy chủ FinPilot dựa trên thông tin bạn đã nhập
          </p>
        </div>

        <div
          className={`mb-8 p-6 rounded-lg border-2 ${
            result.is_achievable
              ? 'border-green-500 bg-green-50'
              : 'border-yellow-500 bg-yellow-50'
          }`}
        >
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
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
                  Với {formatVND(monthlyContribution)} tiết kiệm hàng tháng, ước tính đạt
                  mục tiêu sau khoảng {timePhrase}.
                </p>
              ) : (
                <div>
                  <p className="text-yellow-800 mb-2">
                    Với {formatVND(monthlyContribution)} tiết kiệm hàng tháng, còn thiếu{' '}
                    {formatVND(result.shortfall_amount)} để đạt mục tiêu trong kỳ hạn đã chọn.
                  </p>
                  <p className="text-yellow-800 font-medium">
                    Gợi ý: tăng tiết kiệm hàng tháng lên ít nhất{' '}
                    {formatVND(monthlyContribution + result.recommended_monthly_increase)}
                  </p>
                </div>
              )}
            </div>

            <div className="text-right sm:shrink-0">
              <div className="text-4xl font-bold text-blue-600">
                {formatProgress((result.final_net_worth / targetAmount) * 100)}
              </div>
              <p className="text-gray-600 text-sm">Tiến độ (ước tính)</p>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <p className="text-gray-600 text-sm mb-2">Tiết kiệm cuối kỳ</p>
            <p className="text-2xl font-bold text-blue-600">
              {formatVND(result.final_savings)}
            </p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <p className="text-gray-600 text-sm mb-2">Nợ cuối kỳ</p>
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

        <div className="bg-white rounded-lg shadow p-8 mb-8">
          <ProjectionChart
            data={result.monthly_projections}
            title="Biểu đồ dự báo"
            height={400}
            isAchievable={result.is_achievable}
            targetAmount={targetAmount}
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Phân tích đóng góp
            </h3>
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-gray-600">Tiền tiết kiệm:</span>
                <span className="font-semibold text-gray-900">
                  {formatVND(result.total_contributions)}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Tăng trưởng đầu tư (ước tính):</span>
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
                <span className="text-gray-600">Thời gian mô phỏng:</span>
                <span className="font-semibold text-gray-900">
                  {Math.floor(result.total_months / 12)} năm{' '}
                  {result.total_months % 12} tháng
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
                  <span className="text-gray-600">Chênh so với mục tiêu:</span>
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

        <div className="flex flex-wrap gap-4 justify-center">
          <button
            type="button"
            onClick={() => window.history.back()}
            className="px-6 py-3 border border-gray-300 rounded-lg text-gray-700 font-medium hover:bg-gray-50 transition-colors"
          >
            Quay lại
          </button>
          <button
            type="button"
            onClick={() => setShowSavePrompt(true)}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors"
          >
            Lưu kế hoạch
          </button>
        </div>

        {showSavePrompt && (
          <SavePlanPrompt result={result} onClose={() => setShowSavePrompt(false)} />
        )}
      </div>
    </div>
  )
}
