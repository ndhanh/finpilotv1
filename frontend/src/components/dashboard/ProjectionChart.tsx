/**
 * Projection Chart Component
 *
 * Visualizes financial projection data using Recharts.
 * Shows net worth growth over time with savings and debt breakdown.
 */

'use client'

import React, { useMemo } from 'react'
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ComposedChart,
} from 'recharts'
import { formatVND } from '@/lib/formatting'
import { MonthlyProjectionData } from '@/types/projection'

interface ProjectionChartProps {
  data: MonthlyProjectionData[]
  title?: string
  height?: number
  isAchievable?: boolean
  targetAmount?: number
}

interface ChartDataPoint {
  month: number
  year: number
  monthLabel: string
  savings_balance: number
  debt_balance: number
  net_worth: number
  investment_growth: number
}

/**
 * Custom tooltip for chart
 */
const CustomTooltip: React.FC<any> = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    const data = payload[0].payload

    return (
      <div className="bg-white p-3 border border-gray-300 rounded shadow-lg">
        <p className="text-sm font-medium text-gray-900">
          Tháng {data.month}, Năm {data.year}
        </p>

        {payload.map((entry: any, index: number) => (
          <p key={index} style={{ color: entry.color }} className="text-sm">
            {entry.name}: {formatVND(entry.value)}
          </p>
        ))}
      </div>
    )
  }

  return null
}

/**
 * Main projection chart component
 */
export const ProjectionChart: React.FC<ProjectionChartProps> = ({
  data,
  title = 'Dự báo tài chính',
  height = 400,
  isAchievable = true,
  targetAmount,
}) => {
  // Prepare chart data with friendly labels
  const chartData: ChartDataPoint[] = useMemo(() => {
    return data.map((point) => ({
      month: point.month,
      year: point.year,
      monthLabel: `T${point.month}/${point.year}`,
      savings_balance: point.savings_balance,
      debt_balance: point.debt_balance,
      net_worth: point.net_worth,
      investment_growth: point.investment_growth,
    }))
  }, [data])

  // Select a subset of data points for cleaner visualization (every 3rd month)
  const displayData = useMemo(() => {
    if (chartData.length <= 12) {
      return chartData
    }

    // Show every 3rd month for longer projections
    return chartData.filter(
      (_, index) => index % 3 === 0 || index === chartData.length - 1
    )
  }, [chartData])

  return (
    <div className="w-full">
      {title && (
        <h3 className="text-lg font-semibold mb-4 text-gray-900">{title}</h3>
      )}

      {!isAchievable && (
        <div className="mb-4 p-3 bg-yellow-50 border border-yellow-200 rounded text-sm text-yellow-800">
          ⚠️ Mục tiêu không đạt được với các giả định hiện tại. Cần tăng khoản
          tiết kiệm hàng tháng.
        </div>
      )}

      <ResponsiveContainer width="100%" height={height}>
        <ComposedChart data={displayData}>
          <defs>
            <linearGradient id="colorNetWorth" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.8} />
              <stop offset="95%" stopColor="#3b82f6" stopOpacity={0.1} />
            </linearGradient>

            <linearGradient id="colorSavings" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#10b981" stopOpacity={0.8} />
              <stop offset="95%" stopColor="#10b981" stopOpacity={0.1} />
            </linearGradient>
          </defs>

          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />

          <XAxis
            dataKey="monthLabel"
            tick={{ fontSize: 12 }}
            interval={Math.floor(displayData.length / 6)}
          />

          <YAxis
            tick={{ fontSize: 12 }}
            tickFormatter={(value) => `${(value / 1_000_000).toFixed(0)}M`}
          />

          <Tooltip content={<CustomTooltip />} />

          <Legend
            wrapperStyle={{ fontSize: 12 }}
            formatter={(value) => {
              const labels: Record<string, string> = {
                savings_balance: 'Tiết kiệm',
                net_worth: 'Giá trị ròng',
                debt_balance: 'Nợ',
              }
              return labels[value] || value
            }}
          />

          <Area
            type="monotone"
            dataKey="savings_balance"
            fill="url(#colorSavings)"
            stroke="#10b981"
            strokeWidth={2}
            name="Tiết kiệm"
            isAnimationActive={true}
          />

          <Line
            type="monotone"
            dataKey="net_worth"
            stroke="#3b82f6"
            strokeWidth={3}
            name="Giá trị ròng"
            connectNulls
            dot={{ fill: '#3b82f6', r: 3 }}
            activeDot={{ r: 5 }}
          />

          {/* Show target line if provided */}
          {targetAmount && (
            <Line
              type="monotone"
              dataKey={() => targetAmount}
              stroke="#ef4444"
              strokeWidth={2}
              strokeDasharray="5 5"
              name="Mục tiêu"
              dot={false}
            />
          )}
        </ComposedChart>
      </ResponsiveContainer>

      <div className="mt-4 text-sm text-gray-600">
        <p>📊 Biểu đồ hiển thị dự báo giá trị ròng theo thời gian</p>
        <p>
          💚 Đường xanh lục: tiền tiết kiệm &nbsp; | &nbsp; 🔵 Đường xanh dương:
          giá trị ròng
        </p>
      </div>
    </div>
  )
}

export default ProjectionChart
