'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'

export default function SavingsPage() {
  const [savings, setSavings] = useState('')
  const [isClient, setIsClient] = useState(false)
  const router = useRouter()

  useEffect(() => {
    setIsClient(true)
    // Check if previous steps are completed
    if (typeof window !== 'undefined') {
      const goalType = localStorage.getItem('finpilot_goal_type')
      const timeline = localStorage.getItem('finpilot_timeline')
      const amount = localStorage.getItem('finpilot_amount')
      if (!goalType || !timeline || !amount) {
        router.push('/plan/goal')
      }
    }
  }, [router])

  const formatCurrency = (value: string) => {
    const numericValue = value.replace(/[^0-9]/g, '')
    return numericValue.replace(/\B(?=(\d{3})+(?!\d))/g, ',')
  }

  const handleSavingsChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const rawValue = e.target.value.replace(/,/g, '')
    if (/^\d*$/.test(rawValue)) {
      setSavings(rawValue)
    }
  }

  const handleContinue = () => {
    if (isClient && savings) {
      localStorage.setItem('finpilot_savings', savings)
      router.push('/plan/assets')
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="container mx-auto px-4 max-w-2xl">
        <div className="bg-white rounded-lg shadow-sm p-8">
          <div className="mb-6">
            <div className="flex items-center mb-4">
              <div className="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-semibold">
                4
              </div>
              <div className="ml-3 flex-1">
                <div className="text-sm text-gray-500">Step 4 of 6</div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div className="bg-blue-600 h-2 rounded-full w-4/6"></div>
                </div>
              </div>
            </div>
          </div>

          <div className="space-y-6">
            <div>
              <h2 className="text-xl font-semibold text-gray-900 mb-2">
                How much can you save monthly?
              </h2>
              <p className="text-gray-600 mb-4">
                This is your monthly surplus after expenses. Be realistic about
                what you can consistently save.
              </p>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Monthly savings amount (VND)
                </label>
                <div className="relative">
                  <input
                    type="text"
                    value={formatCurrency(savings)}
                    onChange={handleSavingsChange}
                    placeholder="15,000,000"
                    className="input-field pl-12"
                  />
                  <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500">
                    ₫
                  </span>
                </div>
                <p className="text-sm text-gray-500 mt-2">
                  Tip: Calculate this as (monthly income - monthly expenses)
                </p>
              </div>
            </div>

            <div className="flex justify-between pt-6">
              <button onClick={() => router.back()} className="btn-secondary">
                Back
              </button>
              <button
                onClick={handleContinue}
                disabled={!savings}
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
