const faqs = [
  {
    q: 'FinPilot có lưu dữ liệu của tôi không?',
    a: 'Luồng ban đầu được thiết kế để bạn thử nhanh; chi tiết lưu trữ phụ thuộc phiên bản sản phẩm và chính sách bạn đồng ý. Trên trang bắt đầu, bạn không bắt buộc tạo tài khoản.',
  },
  {
    q: 'Con số hiển thị có phải “đảm bảo” không?',
    a: 'Không. Đây là công cụ lập kế hoạch và mô phỏng dựa trên giả định bạn cung cấp. Thực tế thị trường, lãi suất và chi tiêu luôn thay đổi — FinPilot giúp bạn định hướng, không thay thế tư vấn pháp lý hay đầu tư cá nhân hóa.',
  },
  {
    q: 'Tôi chưa rõ thu nhập chính xác thì dùng được không?',
    a: 'Có. Bạn có thể bắt đầu với ước lượng và điều chỉnh dần; mục tiêu là có khung thảo luận tốt hơn là chờ “đủ dữ liệu hoàn hảo”.',
  },
  {
    q: 'FinPilot khác gì app ghi chép chi tiêu?',
    a: 'Trọng tâm là mục tiêu dài hạn và lộ trình (khi nào, cần tích lũy khoảng bao nhiêu), không chỉ theo dõi từng giao dịch hàng ngày.',
  },
]

export function FAQSection() {
  return (
    <section id="faq" className="bg-slate-50 py-16 md:py-24 scroll-mt-20">
      <div className="mx-auto max-w-3xl px-4">
        <h2 className="text-center text-3xl font-bold text-slate-900 md:text-4xl">
          Câu hỏi thường gặp
        </h2>
        <p className="mt-4 text-center text-slate-600">
          Ngắn gọn — nếu cần thêm, đội ngũ sẽ bổ sung theo phản hồi người dùng.
        </p>
        <div className="mt-10 space-y-3">
          {faqs.map((item) => (
            <details
              key={item.q}
              className="group rounded-2xl border border-slate-200 bg-white px-5 py-4 shadow-sm open:shadow-md"
            >
              <summary className="cursor-pointer list-none font-medium text-slate-900 [&::-webkit-details-marker]:hidden">
                <span className="flex items-center justify-between gap-4">
                  {item.q}
                  <span className="shrink-0 text-slate-400 transition group-open:rotate-180">
                    <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M19 9l-7 7-7-7"
                      />
                    </svg>
                  </span>
                </span>
              </summary>
              <p className="mt-3 border-t border-slate-100 pt-3 text-sm leading-relaxed text-slate-600">
                {item.a}
              </p>
            </details>
          ))}
        </div>
      </div>
    </section>
  )
}
