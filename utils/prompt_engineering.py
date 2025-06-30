# =============================================================================
# utils/prompt_engineering.py  ―  RAG 없이 단순 프롬프트 빌더
# =============================================================================
def build_prompt(question: str, lang: str) -> str:
    """
    RAG-less 프롬프트.
    * 역할: 한국 노동법‧출입국관리 관련 상담 AI
    * 출력: 상황 요약 ➜ 핵심 조문/원칙 ➜ 실무적 조언
    """
    if lang == "zh":
        role = (
            "你是一位精通韩国劳动法及出入境管理规定的法律顾问，"
            "专门为在韩工作的外国人提供中文法律咨询。"
        )
        output_rule = (
            "请按以下格式回答（共 4–6 句内）:\n"
            "1. 〖问题简要〗(1 句)\n"
            "2. 〖适用法律要点〗(2–3 句)\n"
            "3. 〖可行建议〗(1–2 句，必要时提示咨询专业律师)\n"
            "回答时不要暴露任何内部推理过程。"
        )
    else:  # vi
        role = (
            "Bạn là cố vấn pháp luật thành thạo Luật Lao động và Luật Xuất nhập cảnh "
            "Hàn Quốc, chuyên hỗ trợ người lao động nước ngoài bằng tiếng Việt."
        )
        output_rule = (
            "Vui lòng làm theo mẫu (tổng 4–6 câu):\n"
            "1. 〖Tóm tắt vấn đề〗(1 câu)\n"
            "2. 〖Nguyên tắc pháp luật áp dụng〗(2–3 câu)\n"
            "3. 〖Khuyến nghị thiết thực〗(1–2 câu; nhắc liên hệ luật sư khi cần)\n"
            "Đừng tiết lộ lập luận nội bộ."
        )

    return f"{role}\n\n{question}\n\n{output_rule}"
