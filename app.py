import streamlit as st
import google.generativeai as genai

# API 키 설정
API_KEY = "AIzaSyCag1FU7gbaMCkk1aJLxuaT03og9cDSBHU"
genai.configure(api_key=API_KEY)

# 수정 포인트: 모델 이름을 'models/gemini-1.5-flash'로 더 정확하게 부릅니다.
model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')

st.set_page_config(page_title="AI 맞춤법 선생님")
st.title("✍️ AI 맞춤법 & 띄어쓰기 교정기")

user_input = st.text_area("문장을 입력하세요:", placeholder="예: 안녕 하세요 점심 먹었 나요?")

if st.button("AI 선생님에게 검사받기 ✨"):
    if user_input.strip():
        with st.spinner('분석 중...'):
            try:
                # 안전한 호출 방식
                response = model.generate_content(f"다음 문장을 고쳐줘: {user_input}")
                st.success("완료!")
                st.markdown(response.text)
            except Exception as e:
                # 에러 내용을 더 구체적으로 찍어서 범인을 잡아봅시다.
                st.error(f"오류 내용: {e}")
