import Link from 'next/link'

export default function PlanPage() {
  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="container mx-auto px-4 max-w-2xl">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">
            Let's Plan Your Financial Goal
          </h1>
          <p className="text-gray-600">
            Answer a few questions and get a personalized financial projection
            in minutes. No account required.
          </p>
        </div>

        <div className="bg-white rounded-lg shadow-sm p-8">
          <div className="space-y-6">
            <div>
              <h2 className="text-xl font-semibold text-gray-900 mb-2">
                What would you like to plan for?
              </h2>
              <div className="space-y-3">
                <Link
                  href="/plan/goal"
                  className="block w-full p-4 border border-gray-200 rounded-lg hover:border-blue-300 hover:bg-blue-50 transition-colors text-left"
                >
                  <div className="font-medium text-gray-900">Buy a House</div>
                  <div className="text-sm text-gray-600">
                    Purchase residential property in Vietnam
                  </div>
                </Link>
                <Link
                  href="/plan/goal"
                  className="block w-full p-4 border border-gray-200 rounded-lg hover:border-blue-300 hover:bg-blue-50 transition-colors text-left"
                >
                  <div className="font-medium text-gray-900">
                    Build Emergency Fund
                  </div>
                  <div className="text-sm text-gray-600">
                    Save for unexpected expenses
                  </div>
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
