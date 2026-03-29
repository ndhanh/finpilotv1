import { CtaButton } from './CtaButton'

type Props = {
  planUrl: string
}

export function HeroSection({ planUrl }: Props) {
  return (
    <section className="relative overflow-hidden bg-gradient-to-b from-slate-50 via-white to-blue-50/60">
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_80%_50%_at_50%_-20%,rgba(59,130,246,0.15),transparent)]" />
      <div className="relative mx-auto max-w-6xl px-4 pb-20 pt-12 md:pb-28 md:pt-16">
        <div className="grid items-center gap-12 lg:grid-cols-2 lg:gap-16">
          <div>
            <p className="mb-4 inline-block rounded-full bg-primary-50 px-3 py-1 text-sm font-medium text-primary-700">
              Dành cho người Việt — không cần đăng nhập để thử
            </p>
            <h1 className="text-4xl font-bold tracking-tight text-slate-900 md:text-5xl lg:text-[2.75rem] lg:leading-[1.15]">
              Tự do tài chính bắt đầu từ một{' '}
              <span className="text-primary-600">kế hoạch rõ ràng</span>
            </h1>
            <p className="mt-5 max-w-xl text-lg text-slate-600 md:text-xl">
              FinPilot giúp bạn đặt mục tiêu (mua nhà, tiết kiệm, nghỉ hưu) và xem trước lộ
              trình tài chính — minh bạch, gần gũi với bối cảnh Việt Nam.
            </p>
            <div className="mt-8 flex flex-wrap items-center gap-4">
              <CtaButton href={planUrl} />
              <span className="text-sm text-slate-500">Miễn phí bước đầu · Không cần tài khoản</span>
            </div>
          </div>

          <div className="relative">
            <div className="rounded-2xl border border-slate-200/80 bg-white p-6 shadow-xl shadow-slate-200/50 ring-1 ring-slate-900/5">
              <p className="text-xs font-medium uppercase tracking-wide text-slate-400">
                Xem trước giao diện
              </p>
              <div className="mt-4 grid gap-3 sm:grid-cols-2">
                <div className="rounded-xl bg-slate-50 p-4 ring-1 ring-slate-100">
                  <p className="text-xs text-slate-500">Mục tiêu</p>
                  <p className="mt-1 font-semibold text-slate-900">Mua nhà lần đầu</p>
                  <div className="mt-3 h-2 overflow-hidden rounded-full bg-slate-200">
                    <div className="h-full w-[62%] rounded-full bg-primary-500" />
                  </div>
                  <p className="mt-2 text-xs text-slate-500">Tiến độ ước tính: 62%</p>
                </div>
                <div className="rounded-xl bg-slate-50 p-4 ring-1 ring-slate-100">
                  <p className="text-xs text-slate-500">Tích lũy hàng tháng (gợi ý)</p>
                  <p className="mt-1 text-2xl font-bold text-slate-900">12,5 triệu</p>
                  <p className="text-xs text-slate-500">Điều chỉnh theo thu nhập của bạn</p>
                </div>
                <div className="sm:col-span-2 rounded-xl border border-dashed border-primary-200 bg-primary-50/50 p-4">
                  <p className="text-xs font-medium text-primary-800">Lộ trình gợi ý</p>
                  <p className="mt-1 text-sm text-primary-900/90">
                    Ước tính đủ vốn đặt cọc trong ~6 năm nếu duy trì mức tiết kiệm này (số minh họa).
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
