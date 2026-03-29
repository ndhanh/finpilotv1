/**
 * Save Plan Prompt Component
 *
 * Modal for saving plan and signup flow
 * Allows users to save their plan to the backend with authentication
 */

'use client'

import React, { useState } from 'react'
import { usePlanContext } from '@/context/PlanContext'
import { plansApi, goalsApi } from '@/lib/api'

export interface SavePlanPromptProps {
  result?: any
  onClose: () => void
}

export const SavePlanPrompt: React.FC<SavePlanPromptProps> = ({
  result,
  onClose,
}) => {
  const plan = usePlanContext()
  const [isLoading, setIsLoading] = useState(false)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [fullName, setFullName] = useState('')
  const [planName, setPlanName] = useState(
    plan.planData.goalName || 'Kế hoạch tài chính'
  )
  const [error, setError] = useState('')
  const [success, setSuccess] = useState(false)

  const handleSavePlan = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError('')

    try {
      console.log('Starting save plan process...')
      // For now, use a dummy user ID (in real app, this would come from auth)
      const userId = 1

      // Create plan
      const planData = {
        name: planName,
        description: `Kế hoạch ${plan.planData.goalType} - ${plan.planData.targetAmount} VND`,
      }
      console.log('Creating plan with data:', planData)

      const planResponse = await plansApi.create(userId, planData)
      console.log('Plan creation response:', planResponse)
      console.log('Plan creation response:', planResponse)

      if (planResponse.error) {
        throw new Error(`Không thể tạo kế hoạch: ${planResponse.error}`)
      }

      const planId = planResponse.data?.id
      console.log('Created plan with ID:', planId)

      // Create goal and associate with plan
      const goalData = {
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
      }
      console.log('Creating goal with data:', goalData)

      const goalResponse = await goalsApi.create(userId, goalData)
      console.log('Goal creation response:', goalResponse)

      if (goalResponse.error) {
        throw new Error(`Không thể tạo mục tiêu: ${goalResponse.error}`)
      }

      const goalId = goalResponse.data?.id
      console.log('Created goal with ID:', goalId)

      // Associate goal with plan
      if (planId && goalId) {
        const associationResponse = await plansApi.addGoal(
          planId,
          goalId,
          userId
        )
        if (associationResponse.error) {
          console.warn(
            'Không thể liên kết mục tiêu với kế hoạch:',
            associationResponse.error
          )
          // Don't fail the whole operation for this
        }
      }

      setSuccess(true)
      plan.clearDraft()

      // In a real app, you might redirect to dashboard or show success message
      setTimeout(() => {
        onClose()
        // Could redirect to dashboard here
      }, 2000)
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Lỗi không xác định khi lưu kế hoạch'
      )
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
        {/* Header */}
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-gray-900">
            {success ? '✓ Thành công!' : 'Lưu Kế Hoạch của Bạn'}
          </h2>
          <p className="text-gray-600 mt-1">
            {success
              ? 'Kế hoạch đã được lưu thành công'
              : 'Tạo tài khoản để lưu kế hoạch tài chính của bạn'}
          </p>
        </div>

        {success ? (
          <div className="space-y-4">
            <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
              <p className="text-green-800 text-center">
                Đang chuyển hướng đến bảng điều khiển...
              </p>
            </div>

            <button
              onClick={onClose}
              className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors"
            >
              Đóng
            </button>
          </div>
        ) : (
          <form onSubmit={handleSavePlan} className="space-y-4">
            {/* Plan Name */}
            <div>
              <label className="block text-sm font-medium text-gray-900 mb-1">
                Tên Kế Hoạch
              </label>
              <input
                type="text"
                value={planName}
                onChange={(e) => setPlanName(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>

            {/* Full Name */}
            <div>
              <label className="block text-sm font-medium text-gray-900 mb-1">
                Họ Tên *
              </label>
              <input
                type="text"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                placeholder="Nguyễn Văn A"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>

            {/* Email */}
            <div>
              <label className="block text-sm font-medium text-gray-900 mb-1">
                Email *
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="your.email@example.com"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>

            {/* Password */}
            <div>
              <label className="block text-sm font-medium text-gray-900 mb-1">
                Mật Khẩu *
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Tối thiểu 8 ký tự"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
                minLength={8}
              />
            </div>

            {/* Error Message */}
            {error && (
              <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
                <p className="text-sm text-red-800">{error}</p>
              </div>
            )}

            {/* Privacy Notice */}
            <div className="flex items-start gap-2 text-xs text-gray-600">
              <input
                type="checkbox"
                id="agree"
                defaultChecked
                className="mt-1"
              />
              <label htmlFor="agree">
                Tôi đồng ý với{' '}
                <a href="#" className="text-blue-600 hover:underline">
                  Điều khoản sử dụng
                </a>{' '}
                và{' '}
                <a href="#" className="text-blue-600 hover:underline">
                  Chính sách bảo mật
                </a>
              </label>
            </div>

            {/* Buttons */}
            <div className="flex gap-3 pt-4">
              <button
                type="button"
                onClick={onClose}
                disabled={isLoading}
                className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg font-medium hover:bg-gray-50 disabled:opacity-50 transition-colors"
              >
                Hủy
              </button>

              <button
                type="submit"
                disabled={isLoading}
                className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50 transition-colors"
              >
                {isLoading ? 'Đang lưu...' : 'Lưu Kế Hoạch'}
              </button>
            </div>
          </form>
        )}

        {/* Close Button */}
        <button
          onClick={onClose}
          disabled={success}
          className="absolute top-4 right-4 text-gray-500 hover:text-gray-700 disabled:opacity-50"
        >
          ✕
        </button>
      </div>
    </div>
  )
}

export default SavePlanPrompt
