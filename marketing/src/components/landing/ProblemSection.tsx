const items = [
  {
    title: 'Giá nhà và chi phí sinh hoạt tăng nhanh',
    body: 'Khó hình dung cần tích lũy bao nhiêu và trong bao lâu nếu không có con số cụ thể.',
  },
  {
    title: 'Thu nhập thất thường, nhiều nguồn',
    body: 'Freelance, kinh doanh nhỏ hay lương cố định — khó gộp thành một bức tranh để quyết định.',
  },
  {
    title: 'Công cụ nước ngoài không phù hợp bối cảnh Việt Nam',
    body: 'Đơn vị, thói quen chi tiêu và mục tiêu (như mua nhà) cần được diễn đạt gần với đời thực.',
  },
]

export function ProblemSection() {
  return (
    <section className="border-t border-slate-100 bg-white py-16 md:py-24">
      <div className="mx-auto max-w-6xl px-4">
        <h2 className="text-center text-3xl font-bold text-slate-900 md:text-4xl">
          Tại sao chỉ “tiết kiệm khi nhớ” thường không đủ?
        </h2>
        <p className="mx-auto mt-4 max-w-2xl text-center text-slate-600">
          Nhiều người có ý định tốt nhưng thiếu bức tranh tổng thể — dễ trì hoãn hoặc đặt kỳ vọng
          không thực tế.
        </p>
        <ul className="mt-12 grid gap-6 md:grid-cols-3">
          {items.map((item) => (
            <li
              key={item.title}
              className="rounded-2xl border border-slate-100 bg-slate-50/80 p-6 shadow-sm transition hover:border-slate-200 hover:shadow-md"
            >
              <div className="mb-3 flex h-10 w-10 items-center justify-center rounded-lg bg-amber-100 text-amber-700">
                <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                  />
                </svg>
              </div>
              <h3 className="font-semibold text-slate-900">{item.title}</h3>
              <p className="mt-2 text-sm leading-relaxed text-slate-600">{item.body}</p>
            </li>
          ))}
        </ul>
      </div>
    </section>
  )
}
