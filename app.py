# =============================================================================
# app.py – Streamlit 메인 (RAG-less)
# =============================================================================
import streamlit as st
from pathlib import Path
import sys
from langdetect import detect, DetectorFactory
import config
from utils import load_tokenizer, build_prompt, generate_answer
from utils.generator import load_generation_models

# 프로젝트 루트 추가
sys.path.append(str(Path(__file__).parent))
DetectorFactory.seed = 0     # langdetect 재현성

# ────────────────────────────── ① Streamlit 기본 설정 ──────────────────────────
st.set_page_config(
    page_title=config.PAGE_TITLE,
    page_icon=config.PAGE_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(f"# {config.PAGE_ICON} {config.PAGE_TITLE}\n"
            "중국어·베트남어 노동법 상담 챗봇 (RAG 제거 버전)")

with st.sidebar:
    st.markdown("### 사용 방법")
    st.markdown("1. 중국어 또는 베트남어로 질문 입력\n"
                "2. AI가 직접 답변(내부 RAG 미사용)\n"
                "⚠️ 참고용이며, 정확성 미보장")

# ────────────────────────────── ② 모델 & 토크나이저 로드 ──────────────────────
@st.cache_resource(show_spinner=False)
def get_models():
    zh_model, vi_model = load_generation_models()
    return {"zh": zh_model, "vi": vi_model}

@st.cache_resource(show_spinner=False)
def get_tokenizers():
    return {"zh": load_tokenizer("zh"), "vi": load_tokenizer("vi")}

models = get_models()
tokenizers = get_tokenizers()

# ────────────────────────────── ③ 언어 감지 유틸 ───────────────────────────────
import regex as re
def safe_detect(text: str) -> str:
    try:
        lang = detect(text)
    except:
        lang = "unknown"
    if re.search(r"\p{Han}", text):
        return "zh"
    if re.search(r"[ăâđêôơưĂÂĐÊÔƠƯ]", text):
        return "vi"
    return lang

# ────────────────────────────── ④ 메인 입력/출력 로직 ──────────────────────────
st.markdown("## 질문 입력")
question = st.text_input(
    "질문",
    label_visibility="collapsed",
    placeholder="중국어 또는 베트남어로 법률 관련 질문을 입력하세요...",
)

if st.button("질문하기") and question.strip():
    lang = safe_detect(question)
    if lang not in ("zh", "vi"):
        st.warning("⚠️ 중국어 또는 베트남어로 입력해 주세요.")
        st.stop()

    st.info(f"감지된 언어: {'중국어' if lang=='zh' else '베트남어'}")

    tokenizer = tokenizers[lang]
    model = models[lang]

    if tokenizer is None or model is None:
        st.error("모델 또는 토크나이저가 준비되지 않았습니다.")
        st.stop()

    prompt = build_prompt(question, lang)

    with st.spinner("AI 답변 생성 중…"):
        answer = generate_answer(prompt, model, tokenizer)

    st.markdown("### AI 법률 상담 답변")
    st.write(answer)
    st.markdown("---\n⚠️ **면책조항:** 본 답변은 참고용 정보입니다. 중요한 사안은 변호사와 상의하세요.")
