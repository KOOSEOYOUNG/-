import streamlit as st
import google.generativeai as genai

# API 키 설정
API_KEY = "AIzaSyCag1FU7gbaMCkk1aJLxuaT03og9cDSBHU"
genai.configure(api_key=API_KEY)

# 최신 방식: 모델을 지정할 때 버전 오류가 안 나게 모델명만 깔끔하게 넣습니다.
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="AI 맞춤법 선생님")
st.title("✍️ AI 맞춤법 & 띄어쓰기 교정기")

user_input = st.text_area("문장을 입력하세요:", placeholder="예: 안녕 하세요 점심 먹었 나요?")

if st.button("AI 선생님에게 검사받기 ✨"):
    if user_input.strip():
        with st.spinner('분석 중...'):
            try:
                # 여기서 에러가 안 나게 가장 기본적인 호출을 사용합니다.
                response = model.generate_content(f"다음 문장의 맞춤법을 고치고 이유를 설명해줘: {user_input}")
                st.success("완료!")
                st.markdown(response.text)
            except Exception as e:
                # 에러 메시지가 너무 길면 보기 싫으니 핵심만 띄웁니다.
                st.error(f"오류가 발생했습니다. API 키나 모델 설정을 확인해주세요. ({e})")
