import streamlit as st
import google.generativeai as genai

# 1. 새로 발급받은 API 키 설정
API_KEY = "AIzaSyBVUiEBAgYiDzM6ILzjk-9m0eRoR1MgE94"
genai.configure(api_key=API_KEY)

# 웹 화면 설정
st.set_page_config(page_title="AI 맞춤법 선생님", page_icon="✍️")
st.title("✍️ AI 맞춤법 & 띄어쓰기 교정기")

# 2. 모델 설정 (에러 방지를 위해 사용 가능한 모델을 자동으로 찾습니다)
try:
    # 현재 계정에서 사용 가능한 모델 목록 가져오기
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    # gemini-1.5-flash가 있으면 우선 사용, 없으면 목록의 첫 번째 모델 사용
    if 'models/gemini-1.5-flash' in available_models:
        model_name = 'models/gemini-1.5-flash'
    elif 'models/gemini-pro' in available_models:
        model_name = 'models/gemini-pro'
    else:
        model_name = available_models[0]
        
    model = genai.GenerativeModel(model_name)
except Exception as e:
    st.error(f"모델을 초기화하는 중 오류가 발생했습니다: {e}")

# 입력창
user_input = st.text_area("교정받을 문장을 입력하세요:", placeholder="예: 안녕 하세요 점심 먹었 나요?")

if st.button("AI 선생님에게 검사받기 ✨"):
    if user_input.strip() == "":
        st.warning("문장을 입력해주세요!")
    else:
        with st.spinner('AI 선생님이 분석 중입니다...'):
            try:
                # AI에게 교정 요청
                prompt = f"다음 문장의 맞춤법과 띄어쓰기를 교정하고, 그 이유를 친절하게 설명해줘:\n\n{user_input}"
                response = model.generate_content(prompt)
                
                st.success(f"분석 완료! (사용된 모델: {model_name})")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")

st.markdown("---")
st.caption("2026 AI 실무 과제 - Gemini API 활용")
