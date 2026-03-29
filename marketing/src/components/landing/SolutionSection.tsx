const points = [
  {
    title: 'Bắt đầu từ mục tiêu của bạn',
    body: 'Mua nhà, quỹ khẩn cấp hay mục tiêu dài hạn — FinPilot xây khung thảo luận quanh điều bạn thực sự muốn.',
  },
  {
    title: 'Con số minh bạch, dễ hiểu',
    body: 'Ước tính thời gian và mức tích lũy gợi ý, kèm giả định rõ ràng — tránh tạo cảm giác “ảo” chính xác tuyệt đối.',
  },
  {
    title: 'Phù hợp ngữ cảnh Việt Nam',
    body: 'Cách diễn đạt và ví dụ gần với thực tế địa phương, không copy nguyên mô hình nước ngoài.',
  },
]

export function SolutionSection() {
  return (
    <section className="bg-slate-50 py-16 md:py-24">
      <div className="mx-auto max-w-6xl px-4">
        <div className="mx-auto max-w-3xl text-center">
          <h2 className="text-3xl font-bold text-slate-900 md:text-4xl">
            FinPilot đồng hành như một cuộc trò chuyện có cấu trúc
          </h2>
          <p className="mt-4 text-lg text-slate-600">
            Không phải bảng biểu khô khan — mà là lộ trình bạn có thể đọc, chỉnh và tin tưởng từng bước.
          </p>
        </div>
        <ol className="mt-14 space-y-6">
          {points.map((point, i) => (
            <li
              key={point.title}
              className="flex gap-4 rounded-2xl border border-white bg-white p-6 shadow-sm ring-1 ring-slate-900/5 md:items-start"
            >
              <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-primary-600 text-sm font-bold text-white">
                {i + 1}
              </span>
              <div>
                <h3 className="text-lg font-semibold text-slate-900">{point.title}</h3>
                <p className="mt-2 text-slate-600">{point.body}</p>
              </div>
            </li>
          ))}
        </ol>
      </div>
    </section>
  )
}
