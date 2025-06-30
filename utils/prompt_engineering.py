# utils/prompt_engineering.py
def build_prompt(question: str, lang: str) -> str:
    """
    viT5 / mBART-50 전용 최소 프롬프트.
    - 장황한 역할·규칙 문구 제거
    - 'Câu hỏi:' / 'Hỏi:' 같은 접두사도 생략
    - 마지막에 'Trả lời:'(VI) 또는 '答:'(ZH)만 두고 모델이 이어서 생성
    """
    if lang == "vi":
        return f"{question}\n\nTrả lời:"
    else:
        return f"{question}\n\n答:"
