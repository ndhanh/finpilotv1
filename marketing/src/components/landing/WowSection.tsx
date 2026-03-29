import {
  projectionAges,
  savingsWithPlanning,
  savingsWithoutPlanning,
  timelineMilestones,
  wowExampleSubtitle,
  wowExampleTitle,
} from '@/lib/landing-mock'

function BarGroup({
  label,
  value,
  max,
  colorClass,
}: {
  label: string
  value: number
  max: number
  colorClass: string
}) {
  const pct = max > 0 ? Math.round((value / max) * 100) : 0
  return (
    <div>
      <div className="mb-1 flex justify-between text-xs text-slate-600">
        <span>{label}</span>
        <span className="font-medium text-slate-800">{value} tr</span>
      </div>
      <div className="h-3 overflow-hidden rounded-full bg-slate-100">
        <div
          className={`h-full rounded-full transition-all ${colorClass}`}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  )
}

export function WowSection() {
  const maxVal = Math.max(...savingsWithPlanning, ...savingsWithoutPlanning)

  return (
    <section className="border-t border-slate-100 bg-white py-16 md:py-24">
      <div className="mx-auto max-w-6xl px-4">
        <div className="mx-auto max-w-3xl text-center">
          <h2 className="text-3xl font-bold text-slate-900 md:text-4xl">{wowExampleTitle}</h2>
          <p className="mt-4 text-lg text-slate-600">{wowExampleSubtitle}</p>
        </div>

        <div className="mt-12 rounded-2xl border border-slate-200 bg-gradient-to-br from-white to-slate-50 p-6 shadow-lg md:p-10">
          <p className="text-center text-sm font-medium text-slate-500">
            Số dư tích lũy theo tuổi (triệu đồng — minh họa)
          </p>
          <div className="mt-8 grid gap-8 lg:grid-cols-2">
            <div>
              <p className="mb-4 text-sm font-semibold text-primary-700">Có kế hoạch rõ ràng</p>
              <div className="space-y-4">
                {projectionAges.map((age, i) => (
                  <BarGroup
                    key={`w-${age}`}
                    label={`Tuổi ${age}`}
                    value={savingsWithPlanning[i]!}
                    max={maxVal}
                    colorClass="bg-primary-500"
                  />
                ))}
              </div>
            </div>
            <div>
              <p className="mb-4 text-sm font-semibold text-slate-500">Không có kế hoạch cụ thể</p>
              <div className="space-y-4">
                {projectionAges.map((age, i) => (
                  <BarGroup
                    key={`wo-${age}`}
                    label={`Tuổi ${age}`}
                    value={savingsWithoutPlanning[i]!}
                    max={maxVal}
                    colorClass="bg-slate-400"
                  />
                ))}
              </div>
            </div>
          </div>
          <p className="mt-8 text-center text-xs text-slate-500">
            Số liệu mang tính minh họa; kết quả thực tế phụ thuộc thu nhập, chi tiêu và lãi suất.
          </p>
        </div>

        <div className="mt-16">
          <h3 className="text-center text-xl font-bold text-slate-900 md:text-2xl">
            Mốc trên hành trình (minh họa)
          </h3>
          <ul className="relative mx-auto mt-10 max-w-2xl border-l-2 border-slate-200 pl-8">
            {timelineMilestones.map((m) => (
              <li key={m.age} className="relative pb-10 last:pb-0">
                <span className="absolute -left-[39px] top-0 flex h-8 w-8 items-center justify-center rounded-full border-4 border-white bg-primary-500 text-xs font-bold text-white shadow">
                  {m.age}
                </span>
                <div className="rounded-xl border border-slate-100 bg-slate-50/80 p-5 shadow-sm">
                  <h4 className="font-semibold text-slate-900">{m.title}</h4>
                  <p className="mt-2 text-sm text-slate-600">{m.description}</p>
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </section>
  )
}
