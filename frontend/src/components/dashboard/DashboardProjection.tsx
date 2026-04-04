'use client'

import React, { useEffect, useState, useCallback } from 'react'
import { useRouter } from 'next/navigation'
import { usePlanContext } from '@/context/PlanContext'
import { projectionsApi, goalsApi } from '@/lib/api'
import { DEMO_USER_ID } from '@/lib/constants'
import {
  readWizardPlanFromStorage,
  snapshotToGoalCreateBody,
  snapshotToProjectionInput,
} from '@/lib/plan-from-storage'
import { ProjectionResult } from '@/types/projection'
import { ProjectionDashboardView } from './ProjectionDashboardView'

export function DashboardProjection() {
  const router = useRouter()
  const plan = usePlanContext()
  const [snapshot, setSnapshot] = useState<ReturnType<
    typeof readWizardPlanFromStorage
  > | null>(null)
  const [checked, setChecked] = useState(false)
  const [result, setResult] = useState<ProjectionResult | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const hydratePlanFromWizard = useCallback(
    (snap: NonNullable<ReturnType<typeof readWizardPlanFromStorage>>) => {
      plan.updateMultiple({
        goalType: snap.goalType,
        goalName: snap.goalLabel,
        targetAmount: snap.targetAmount,
        currentSavings: snap.currentSavings,
        currentDebt: snap.currentDebt,
        monthlyContribution: snap.monthlyContribution,
        targetDate: snap.targetDateIso,
        timelineYears: snap.timelineMonths / 12,
        expectedReturnRate: 0.07,
        inflationRate: 0.04,
        debtInterestRate: 0.12,
      })
    },
    [plan]
  )

  useEffect(() => {
    const snap = readWizardPlanFromStorage()
    if (!snap) {
      router.replace('/plan/goal')
      return
    }
    setSnapshot(snap)
    hydratePlanFromWizard(snap)
    setChecked(true)
  }, [router, hydratePlanFromWizard])

  useEffect(() => {
    if (!checked || !snapshot) return

    const run = async () => {
      try {
        const goalBody = snapshotToGoalCreateBody(snapshot)
        const goalResponse = await goalsApi.create(DEMO_USER_ID, goalBody)

        if (goalResponse.error) {
          throw new Error(goalResponse.error)
        }

        const goalId = goalResponse.data?.id as number | undefined
        if (!goalId) {
          throw new Error('Không nhận được ID mục tiêu từ máy chủ')
        }

        const projectionInput = snapshotToProjectionInput(snapshot)
        const projectionResponse = await projectionsApi.calculate(
          goalId,
          DEMO_USER_ID,
          projectionInput
        )

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

    run()
  }, [checked, snapshot])

  if (!checked || !snapshot) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4" />
          <p className="text-gray-600">Đang chuẩn bị...</p>
        </div>
      </div>
    )
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4" />
          <p className="text-gray-600">Đang tính toán dự báo trên máy chủ...</p>
        </div>
      </div>
    )
  }

  if (error || !result) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-red-50 to-pink-100 flex items-center justify-center px-4">
        <div className="text-center max-w-md">
          <div className="text-6xl mb-4">⚠️</div>
          <h1 className="text-2xl font-bold text-red-900 mb-2">
            Không thể hiển thị dự báo
          </h1>
          <p className="text-red-700 mb-6">{error ?? 'Thiếu dữ liệu'}</p>
          <button
            type="button"
            onClick={() => router.push('/plan/goal')}
            className="px-6 py-3 bg-red-600 text-white rounded-lg font-medium hover:bg-red-700 transition-colors"
          >
            Bắt đầu lập kế hoạch
          </button>
        </div>
      </div>
    )
  }

  return (
    <ProjectionDashboardView
      result={result}
      targetAmount={snapshot.targetAmount}
      monthlyContribution={snapshot.monthlyContribution}
      selectedTemplate={plan.planData.selectedTemplate}
    />
  )
}
