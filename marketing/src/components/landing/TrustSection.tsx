const principles = [
  {
    title: 'Không thổi phồng độ chính xác',
    body: 'Chúng tôi ưu tiên giả định rõ ràng và khoảng tin cậy hợp lý thay vì cam kết “chính xác từng đồng”.',
  },
  {
    title: 'Bạn hiểu vì sao ra con số đó',
    body: 'Mọi bước gợi ý đều có thể được giải thích bằng ngôn ngữ thường ngày.',
  },
  {
    title: 'Thiết kế cho người Việt',
    body: 'Ví dụ và cách diễn đạt bám sát mục tiêu phổ biến tại Việt Nam (nhà ở, dự phòng, gia đình).',
  },
]

export function TrustSection() {
  return (
    <section className="border-t border-slate-100 bg-white py-16 md:py-24">
      <div className="mx-auto max-w-6xl px-4">
        <h2 className="text-center text-3xl font-bold text-slate-900 md:text-4xl">
          Niềm tin xây trên sự minh bạch
        </h2>
        <p className="mx-auto mt-4 max-w-2xl text-center text-slate-600">
          FinPilot được xây dựng để bạn yên tâm thử nghiệm — không ép buộc, không che giấu giả định.
        </p>
        <div className="mt-12 grid gap-6 md:grid-cols-3">
          {principles.map((p) => (
            <div
              key={p.title}
              className="rounded-2xl border border-emerald-100 bg-emerald-50/40 p-6 text-center md:text-left"
            >
              <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-emerald-100 text-emerald-700 md:mx-0">
                <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"
                  />
                </svg>
              </div>
              <h3 className="font-semibold text-slate-900">{p.title}</h3>
              <p className="mt-2 text-sm text-slate-600">{p.body}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
