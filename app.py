import streamlit as st
import google.generativeai as genai

# 1. 사용자가 제공한 API 키 설정
API_KEY = "AIzaSyCag1FU7gbaMCkk1aJLxuaT03og9cDSBHU"
genai.configure(api_key=API_KEY)

# 2. Gemini 모델 설정 (1.5 Flash 모델 사용)
model = genai.GenerativeModel('models/gemini-1.5-flash')

# 3. 웹앱 화면 꾸미기
st.set_page_config(page_title="AI 맞춤법 선생님", page_icon="✍️")

st.title("✍️ AI 맞춤법 & 띄어쓰기 교정기")
st.write("문장을 입력하면 AI가 맞춤법을 고쳐주고, 틀린 이유도 친절하게 설명해줍니다.")

# 입력창 생성
user_input = st.text_area("교정받을 문장을 입력하세요:", placeholder="예: 안녕 하세요 점심 먹었 나요?")

# 버튼 클릭 시 작동
if st.button("AI 선생님에게 검사받기 ✨"):
    if user_input.strip() == "":
        st.warning("문장을 입력해주세요!")
    else:
        with st.spinner('AI 선생님이 분석 중입니다...'):
            try:
                # AI에게 보낼 요청 메시지(프롬프트)
                prompt = f"""
                당신은 친절한 국어 선생님입니다. 
                다음 문장의 맞춤법과 띄어쓰기를 교정해주세요.
                반드시 아래의 형식을 지켜서 답변해주세요:

                ### ✅ 교정된 문장
                (교정된 문장 결과만 여기에 작성)

                ---
                ### 💡 틀린 이유 설명
                (어떤 부분이 왜 틀렸는지 번호를 매겨서 초등학생도 이해하기 쉽게 설명)

                대상 문장: {user_input}
                """
                
                # Gemini 답변 생성
                response = model.generate_content(prompt)
                
                # 결과 출력
                st.success("분석이 완료되었습니다!")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")

# 바닥글
st.markdown("---")
st.caption("2026 AI 실무 과제 - Gemini API를 활용한 맞춤법 검사기")
