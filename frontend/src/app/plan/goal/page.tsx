'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'

export default function GoalPage() {
  const [selectedGoal, setSelectedGoal] = useState('')
  const router = useRouter()

  const handleContinue = () => {
    if (selectedGoal) {
      // Store in localStorage for now
      localStorage.setItem('finpilot_goal_type', selectedGoal)
      router.push('/plan/timeline')
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="container mx-auto px-4 max-w-2xl">
        <div className="bg-white rounded-lg shadow-sm p-8">
          <div className="mb-6">
            <div className="flex items-center mb-4">
              <div className="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-semibold">
                1
              </div>
              <div className="ml-3 flex-1">
                <div className="text-sm text-gray-500">Step 1 of 6</div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div className="bg-blue-600 h-2 rounded-full w-1/6"></div>
                </div>
              </div>
            </div>
          </div>

          <div className="space-y-6">
            <div>
              <h2 className="text-xl font-semibold text-gray-900 mb-2">
                What's your primary financial goal?
              </h2>
              <p className="text-gray-600 mb-4">
                Choose the main goal you'd like to plan for.
              </p>

              <div className="space-y-3">
                <label className="block">
                  <input
                    type="radio"
                    name="goal"
                    value="house_purchase"
                    checked={selectedGoal === 'house_purchase'}
                    onChange={(e) => setSelectedGoal(e.target.value)}
                    className="mr-3"
                  />
                  <span className="font-medium">Buy a House</span>
                  <br />
                  <span className="text-sm text-gray-600 ml-6">
                    Purchase residential property in Vietnam
                  </span>
                </label>

                <label className="block">
                  <input
                    type="radio"
                    name="goal"
                    value="emergency_fund"
                    checked={selectedGoal === 'emergency_fund'}
                    onChange={(e) => setSelectedGoal(e.target.value)}
                    className="mr-3"
                  />
                  <span className="font-medium">Build Emergency Fund</span>
                  <br />
                  <span className="text-sm text-gray-600 ml-6">
                    Save for unexpected expenses (3-6 months)
                  </span>
                </label>
              </div>
            </div>

            <div className="flex justify-between pt-6">
              <button onClick={() => router.back()} className="btn-secondary">
                Back
              </button>
              <button
                onClick={handleContinue}
                disabled={!selectedGoal}
                className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Continue
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
