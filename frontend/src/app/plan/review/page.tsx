'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'

interface PlanData {
  goalType: string
  timeline: number
  targetAmount: number
  monthlySavings: number
  currentSavings: number
  currentDebt: number
}

export default function ReviewPage() {
  const [planData, setPlanData] = useState<PlanData | null>(null)
  const [isCalculating, setIsCalculating] = useState(false)
  const [isClient, setIsClient] = useState(false)
  const router = useRouter()

  useEffect(() => {
    setIsClient(true)
    // Check if all steps are completed
    if (typeof window !== 'undefined') {
      const goalType = localStorage.getItem('finpilot_goal_type')
      const timeline = localStorage.getItem('finpilot_timeline')
      const amount = localStorage.getItem('finpilot_amount')
      const savings = localStorage.getItem('finpilot_savings')
      const currentSavings = localStorage.getItem('finpilot_current_savings')
      const currentDebt = localStorage.getItem('finpilot_current_debt')

      if (
        !goalType ||
        !timeline ||
        !amount ||
        !savings ||
        currentSavings === null ||
        currentDebt === null
      ) {
        router.push('/plan/goal')
        return
      }

      const data: PlanData = {
        goalType,
        timeline: parseInt(timeline),
        targetAmount: parseInt(amount),
        monthlySavings: parseInt(savings),
        currentSavings: parseInt(currentSavings) || 0,
        currentDebt: parseInt(currentDebt) || 0,
      }

      setPlanData(data)
    }
  }, [router])

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('vi-VN', {
      style: 'currency',
      currency: 'VND',
      minimumFractionDigits: 0,
    }).format(amount)
  }

  const calculateProjection = () => {
    if (!planData) return null

    const {
      targetAmount,
      monthlySavings,
      currentSavings,
      currentDebt,
      timeline,
    } = planData

    // Simple projection calculation (will be replaced with backend API in Phase 2)
    const totalMonths = timeline * 12
    const totalSavings = currentSavings + monthlySavings * totalMonths
    const netPosition = totalSavings - currentDebt
    const shortfall = Math.max(0, targetAmount - netPosition)
    const monthlyShortfall = shortfall / totalMonths

    return {
      totalSavings,
      netPosition,
      shortfall,
      monthlyShortfall,
      isAchievable: netPosition >= targetAmount,
    }
  }

  const handleStartOver = () => {
    localStorage.clear()
    router.push('/plan/goal')
  }

  const handleGetDetailedPlan = () => {
    setIsCalculating(true)
    // In Phase 2, this will call the backend API
    setTimeout(() => {
      router.push('/dashboard')
    }, 2000)
  }

  if (!planData) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading your plan...</p>
        </div>
      </div>
    )
  }

  const projection = calculateProjection()

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="container mx-auto px-4 max-w-4xl">
        <div className="bg-white rounded-lg shadow-sm p-8">
          <div className="text-center mb-8">
            <h1 className="text-2xl font-bold text-gray-900 mb-2">
              Your Financial Plan Summary
            </h1>
            <p className="text-gray-600">
              Here's what we calculated based on your inputs
            </p>
          </div>

          {/* Plan Overview */}
          <div className="grid md:grid-cols-2 gap-6 mb-8">
            <div className="bg-gray-50 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Your Goal
              </h3>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-600">Type:</span>
                  <span className="font-medium capitalize">
                    {planData.goalType.replace('_', ' ')}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Target Amount:</span>
                  <span className="font-medium">
                    {formatCurrency(planData.targetAmount)}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Timeline:</span>
                  <span className="font-medium">{planData.timeline} years</span>
                </div>
              </div>
            </div>

            <div className="bg-gray-50 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Your Current Situation
              </h3>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-600">Monthly Savings:</span>
                  <span className="font-medium">
                    {formatCurrency(planData.monthlySavings)}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Current Savings:</span>
                  <span className="font-medium">
                    {formatCurrency(planData.currentSavings)}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Current Debt:</span>
                  <span className="font-medium">
                    {formatCurrency(planData.currentDebt)}
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Projection Results */}
          {projection && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-8">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Projection Results
              </h3>
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-gray-600">
                      Total Savings in {planData.timeline} years:
                    </span>
                    <span className="font-medium">
                      {formatCurrency(projection.totalSavings)}
                    </span>
                  </div>
                  <div className="flex justify-between mb-2">
                    <span className="text-gray-600">
                      Net Position (Savings - Debt):
                    </span>
                    <span className="font-medium">
                      {formatCurrency(projection.netPosition)}
                    </span>
                  </div>
                </div>
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-gray-600">Shortfall to Goal:</span>
                    <span
                      className={`font-medium ${projection.shortfall > 0 ? 'text-red-600' : 'text-green-600'}`}
                    >
                      {formatCurrency(projection.shortfall)}
                    </span>
                  </div>
                  {projection.shortfall > 0 && (
                    <div className="flex justify-between">
                      <span className="text-gray-600">
                        Additional Monthly Savings Needed:
                      </span>
                      <span className="font-medium text-red-600">
                        {formatCurrency(projection.monthlyShortfall)}
                      </span>
                    </div>
                  )}
                </div>
              </div>

              <div className="mt-4 p-4 rounded-lg bg-white">
                <div
                  className={`text-center font-semibold ${projection.isAchievable ? 'text-green-600' : 'text-orange-600'}`}
                >
                  {projection.isAchievable
                    ? '🎉 Great! You can achieve your goal with your current plan!'
                    : '⚠️ You may need to increase your monthly savings or extend your timeline.'}
                </div>
              </div>
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button onClick={handleStartOver} className="btn-secondary">
              Start Over
            </button>
            <button
              onClick={handleGetDetailedPlan}
              disabled={isCalculating}
              className="btn-primary"
            >
              {isCalculating ? (
                <div className="flex items-center">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Calculating...
                </div>
              ) : (
                'Get Detailed Plan & Dashboard'
              )}
            </button>
          </div>

          <p className="text-center text-sm text-gray-500 mt-4">
            This is a preliminary calculation. The detailed plan will include
            personalized recommendations and visualizations.
          </p>
        </div>
      </div>
    </div>
  )
}
