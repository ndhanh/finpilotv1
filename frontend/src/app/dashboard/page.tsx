'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { MARKETING_ORIGIN } from '@/lib/site-urls'

export default function DashboardPage() {
  const [isClient, setIsClient] = useState(false)
  const router = useRouter()

  useEffect(() => {
    setIsClient(true)
    // Check if user has completed the plan
    if (typeof window !== 'undefined') {
      const goalType = localStorage.getItem('finpilot_goal_type')
      if (!goalType) {
        router.push('/plan/goal')
      }
    }
  }, [router])

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-12">
        <div className="max-w-4xl mx-auto">
          <div className="bg-white rounded-lg shadow-sm p-8 text-center">
            <div className="mb-6">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg
                  className="w-8 h-8 text-blue-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
              <h1 className="text-2xl font-bold text-gray-900 mb-2">
                Welcome to Your FinPilot Dashboard!
              </h1>
              <p className="text-gray-600">
                Your personalized financial planning dashboard is coming soon in
                Phase 2.
              </p>
            </div>

            <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">
                What's Next?
              </h3>
              <div className="text-left space-y-2">
                <div className="flex items-center">
                  <div className="w-2 h-2 bg-blue-600 rounded-full mr-3"></div>
                  <span>
                    Advanced calculation engine with deterministic projections
                  </span>
                </div>
                <div className="flex items-center">
                  <div className="w-2 h-2 bg-blue-600 rounded-full mr-3"></div>
                  <span>Interactive charts and visualizations</span>
                </div>
                <div className="flex items-center">
                  <div className="w-2 h-2 bg-blue-600 rounded-full mr-3"></div>
                  <span>Personalized recommendations and insights</span>
                </div>
                <div className="flex items-center">
                  <div className="w-2 h-2 bg-blue-600 rounded-full mr-3"></div>
                  <span>Progress tracking and milestone alerts</span>
                </div>
                <div className="flex items-center">
                  <div className="w-2 h-2 bg-blue-600 rounded-full mr-3"></div>
                  <span>Secure user accounts and data persistence</span>
                </div>
              </div>
            </div>

            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button
                onClick={() => router.push('/plan/goal')}
                className="btn-secondary"
              >
                Create New Plan
              </button>
              <Link href={MARKETING_ORIGIN} className="btn-primary inline-block text-center">
                Back to Home
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
