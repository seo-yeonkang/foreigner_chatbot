# =============================================================================
# utils/prompt_engineering.py   (chat 지시 → n-shot Q&A 패턴으로 축소)
# =============================================================================
from textwrap import dedent

# ───────────────────────── VIETNAMESE ──────────────────────────
_VI_ROLE = (
    "Bạn là luật sư am hiểu Luật Lao động và Xuất nhập cảnh Hàn Quốc. "
    "Trả lời ngắn gọn, dễ hiểu, tối đa 6 câu."
)

# 2 개의 데모 Q&A로 불안정성 완화
_VI_EXAMPLES = [
    (
        "Tôi phải khai báo tạm trú như thế nào?",
        "Theo Điều 33 Luật Nhập cảnh Hàn Quốc, người nước ngoài "
        "phải khai báo tạm trú trong vòng 14 ngày kể từ khi thay đổi "
        "địa chỉ. Hãy nộp đơn tại văn phòng xuất nhập cảnh địa phương "
        "hoặc qua hệ thống Hi-Korea."
    ),
    (
        "Người lao động nước ngoài có chuyển visa E-9 sang E-7 được không?",
        "Có, nhưng phải đáp ứng tiêu chí nghề nghiệp theo Điều 25 Luật "
        "Việc làm Người nước ngoài và đạt mức lương tối thiểu do Bộ Tư pháp quy định."
    ),
]

# ───────────────────────── CHINESE ─────────────────────────────
_ZH_ROLE = (
    "你是一名熟悉韩国劳动法和出入境管理法规的中文法律顾问，"
    "回答务必简洁，控制在 6 句以内。"
)

_ZH_EXAMPLES = [
    (
        "外国人如何申请延长 E-9 签证？",
        "根据《外国人就业法》第18条，持E-9签证者需在签证到期前"
        "1个月向出入境事务所申请延长，并提交雇佣合同等材料。"
    ),
    (
        "韩国最低工资适用于外国工人吗？",
        "适用。《最低工资法》第5条规定，不论国籍，所有劳动者"
        "均享有最低工资保障。雇主不得以签证类型为由低于标准支付薪资。"
    ),
]

def _build_nshot(question: str, role: str, examples: list[tuple[str, str]]) -> str:
    prompt = [role, ""]
    for q, a in examples:
        prompt.append(f"Hỏi: {q}" if "Hỏi:" not in q and role.startswith("Bạn") else f"问：{q}")
        prompt.append(f"Đáp: {a}" if role.startswith("Bạn") else f"答：{a}")
        prompt.append("")  # 줄바꿈
    prompt.append(f"Hỏi: {question}" if role.startswith("Bạn") else f"问：{question}")
    prompt.append("Đáp:" if role.startswith("Bạn") else "答：")
    return "\n".join(prompt)

def build_prompt(question: str, lang: str) -> str:
    """
    RAG 없이 사용할 n-shot 프롬프트 생성기
    """
    if lang == "vi":
        return _build_nshot(question, _VI_ROLE, _VI_EXAMPLES)
    else:  # zh
        return _build_nshot(question, _ZH_ROLE, _ZH_EXAMPLES)
