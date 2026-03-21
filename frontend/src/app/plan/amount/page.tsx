'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'

export default function AmountPage() {
  const [amount, setAmount] = useState('')
  const [isClient, setIsClient] = useState(false)
  const router = useRouter()

  useEffect(() => {
    setIsClient(true)
    // Check if previous steps are completed
    if (typeof window !== 'undefined') {
      const goalType = localStorage.getItem('finpilot_goal_type')
      const timeline = localStorage.getItem('finpilot_timeline')
      if (!goalType || !timeline) {
        router.push('/plan/goal')
      }
    }
  }, [router])

  const formatCurrency = (value: string) => {
    // Remove non-numeric characters
    const numericValue = value.replace(/[^0-9]/g, '')
    // Format with thousands separator
    return numericValue.replace(/\B(?=(\d{3})+(?!\d))/g, ',')
  }

  const handleAmountChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const rawValue = e.target.value.replace(/,/g, '')
    if (/^\d*$/.test(rawValue)) {
      setAmount(rawValue)
    }
  }

  const handleContinue = () => {
    if (isClient && amount) {
      localStorage.setItem('finpilot_amount', amount)
      router.push('/plan/savings')
    }
  }

  const goalType = isClient ? localStorage.getItem('finpilot_goal_type') : null
  const isHousePurchase = goalType === 'house_purchase'

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="container mx-auto px-4 max-w-2xl">
        <div className="bg-white rounded-lg shadow-sm p-8">
          <div className="mb-6">
            <div className="flex items-center mb-4">
              <div className="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-semibold">
                3
              </div>
              <div className="ml-3 flex-1">
                <div className="text-sm text-gray-500">Step 3 of 6</div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div className="bg-blue-600 h-2 rounded-full w-3/6"></div>
                </div>
              </div>
            </div>
          </div>

          <div className="space-y-6">
            <div>
              <h2 className="text-xl font-semibold text-gray-900 mb-2">
                {isHousePurchase
                  ? 'How much will the home cost?'
                  : 'How much emergency fund do you need?'}
              </h2>
              <p className="text-gray-600 mb-4">
                {isHousePurchase
                  ? 'Enter the total property price including any expected appreciation.'
                  : 'Typically 3-6 months of living expenses. Enter your target amount.'}
              </p>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Amount (VND)
                </label>
                <div className="relative">
                  <input
                    type="text"
                    value={formatCurrency(amount)}
                    onChange={handleAmountChange}
                    placeholder={
                      isHousePurchase ? '4,000,000,000' : '50,000,000'
                    }
                    className="input-field pl-12"
                  />
                  <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500">
                    ₫
                  </span>
                </div>
              </div>
            </div>

            <div className="flex justify-between pt-6">
              <button onClick={() => router.back()} className="btn-secondary">
                Back
              </button>
              <button
                onClick={handleContinue}
                disabled={!amount}
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
