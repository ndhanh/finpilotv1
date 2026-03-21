'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'

export default function TimelinePage() {
  const [timeline, setTimeline] = useState('')
  const router = useRouter()

  useEffect(() => {
    // Check if goal is selected
    const goalType = localStorage.getItem('finpilot_goal_type')
    if (!goalType) {
      router.push('/plan/goal')
    }
  }, [router])

  const handleContinue = () => {
    if (timeline) {
      localStorage.setItem('finpilot_timeline', timeline)
      router.push('/plan/amount')
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="container mx-auto px-4 max-w-2xl">
        <div className="bg-white rounded-lg shadow-sm p-8">
          <div className="mb-6">
            <div className="flex items-center mb-4">
              <div className="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-semibold">
                2
              </div>
              <div className="ml-3 flex-1">
                <div className="text-sm text-gray-500">Step 2 of 6</div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div className="bg-blue-600 h-2 rounded-full w-2/6"></div>
                </div>
              </div>
            </div>
          </div>

          <div className="space-y-6">
            <div>
              <h2 className="text-xl font-semibold text-gray-900 mb-2">
                When do you want to achieve this goal?
              </h2>
              <p className="text-gray-600 mb-4">
                Choose a realistic timeline for your goal.
              </p>

              <div className="space-y-3">
                {[
                  { value: '6', label: '6 months' },
                  { value: '12', label: '1 year' },
                  { value: '24', label: '2 years' },
                  { value: '36', label: '3 years' },
                  { value: '60', label: '5 years' },
                  { value: '120', label: '10 years' },
                ].map((option) => (
                  <label key={option.value} className="block">
                    <input
                      type="radio"
                      name="timeline"
                      value={option.value}
                      checked={timeline === option.value}
                      onChange={(e) => setTimeline(e.target.value)}
                      className="mr-3"
                    />
                    <span className="font-medium">{option.label}</span>
                  </label>
                ))}
              </div>
            </div>

            <div className="flex justify-between pt-6">
              <button onClick={() => router.back()} className="btn-secondary">
                Back
              </button>
              <button
                onClick={handleContinue}
                disabled={!timeline}
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
