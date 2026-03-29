const features = [
  {
    title: 'Lập kế hoạch theo mục tiêu',
    description:
      'Gắn mọi con số với một đích rõ ràng — mua nhà, quỹ dự phòng hay chuẩn bị nghỉ hưu — thay vì chỉ theo dõi số dư.',
    icon: (
      <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={2}
          d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"
        />
      </svg>
    ),
  },
  {
    title: 'Mô phỏng kịch bản',
    description:
      'Hình dung nhiều tình huống (ý tưởng tương tự Monte Carlo: nhiều kịch bản thay vì một con số duy nhất). Trên nền tảng, bạn xem xu hướng và độ nhạy của kế hoạch.',
    icon: (
      <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={2}
          d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z"
        />
      </svg>
    ),
  },
  {
    title: 'Gợi ý theo bối cảnh & thời điểm',
    description:
      'Nhắc điều chỉnh khi thu nhập thay đổi, khi có pha chi tiêu lớn (Tết, học phí…) — giữ kế hoạch sát thực tế.',
    icon: (
      <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={2}
          d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
        />
      </svg>
    ),
  },
  {
    title: 'Lập kế hoạch cho cặp đôi / hộ gia đình',
    description:
      'Gộp mục tiêu chung và phân vai tích lũy — phù hợp khi hai người cùng hướng tới mua nhà hoặc quỹ dự phòng gia đình.',
    icon: (
      <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={2}
          d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"
        />
      </svg>
    ),
  },
]

export function FeatureSection() {
  return (
    <section className="bg-slate-50 py-16 md:py-24">
      <div className="mx-auto max-w-6xl px-4">
        <h2 className="text-center text-3xl font-bold text-slate-900 md:text-4xl">
          Những gì FinPilot hướng tới
        </h2>
        <p className="mx-auto mt-4 max-w-2xl text-center text-slate-600">
          Bốn trụ cột giúp bạn duy trì động lực và điều chỉnh kế hoạch theo đời sống thực.
        </p>
        <div className="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {features.map((f) => (
            <article
              key={f.title}
              className="group rounded-2xl border border-slate-100 bg-white p-6 shadow-sm transition hover:border-primary-200 hover:shadow-md"
            >
              <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary-50 text-primary-600 transition group-hover:bg-primary-100">
                {f.icon}
              </div>
              <h3 className="mt-4 font-semibold text-slate-900">{f.title}</h3>
              <p className="mt-2 text-sm leading-relaxed text-slate-600">{f.description}</p>
            </article>
          ))}
        </div>
      </div>
    </section>
  )
}
