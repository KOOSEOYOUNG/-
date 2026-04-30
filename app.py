import streamlit as st
import google.generativeai as genai

# 1. 새로 주신 API 키 적용
API_KEY = "AIzaSyDQMnmyoxrVJXZWALPgVQAsrO_MD3_mYms"
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="AI 맞춤법 선생님", page_icon="✍️")
st.title("✍️ AI 맞춤법 & 띄어쓰기 교정기")

# 2. 모델 설정 (에러 방지용)
try:
    # 계정 상태에 따라 1.5-flash나 gemini-pro 중 하나를 선택합니다.
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    model = genai.GenerativeModel('gemini-pro')

user_input = st.text_area("교정받을 문장을 입력하세요:", placeholder="예: 안녕 하세요 점심 먹었 나요?")

if st.button("AI 선생님에게 검사받기 ✨"):
    if user_input.strip():
        with st.spinner('AI가 문장을 분석하고 있습니다...'):
            try:
                # AI에게 교정 요청
                prompt = f"다음 문장의 맞춤법과 띄어쓰기를 교정해주고 짧게 설명해줘:\n\n{user_input}"
                response = model.generate_content(prompt)
                
                st.success("분석 완료!")
                st.markdown(response.text)
                
            except Exception as e:
                # 403 에러(사용 제한)가 날 경우를 대비한 친절한 안내
                if "403" in str(e):
                    st.error("🚨 구글 API 키가 아직 승인 대기 중이거나 사용 제한 상태입니다.")
                    st.info("💡 해결 방법: 5~10분 뒤에 다시 시도하거나, 다른 구글 계정으로 키를 새로 만들어보세요.")
                else:
                    st.error(f"오류가 발생했습니다: {e}")
    else:
        st.warning("문장을 입력해주세요!")

st.markdown("---")
st.caption("2026 AI 실무 과제 제출용 - Gemini API 활용")
