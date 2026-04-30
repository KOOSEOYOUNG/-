import streamlit as st
import google.generativeai as genai

# 1. API 키 설정 (방금 주신 키)
API_KEY = "AIzaSyDQMnmyoxrVJXZWALPgVQAsrO_MD3_mYms"
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="AI 맞춤법 선생님", page_icon="✍️")
st.title("✍️ AI 맞춤법 & 띄어쓰기 교정기")

# 2. 에러 방지용 모델 자동 선택 로직
@st.cache_resource
def load_model():
    try:
        # 사용 가능한 모델 목록을 싹 다 긁어옵니다.
        model_list = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # 1순위: flash, 2순위: pro, 3순위: 아무거나 첫 번째 놈
        if 'models/gemini-1.5-flash' in model_list:
            final_model = 'models/gemini-1.5-flash'
        elif 'models/gemini-pro' in model_list:
            final_model = 'models/gemini-pro'
        else:
            final_model = model_list[0]
            
        return genai.GenerativeModel(final_model), final_model
    except Exception as e:
        return None, str(e)

model, model_name = load_model()

if model is None:
    st.error(f"모델을 불러오지 못했습니다. 계정 설정이나 키를 확인해주세요. (상세: {model_name})")
else:
    user_input = st.text_area("교정받을 문장을 입력하세요:", placeholder="예: 안녕 하세요 점심 먹었 나요?")

    if st.button("AI 선생님에게 검사받기 ✨"):
        if user_input.strip():
            with st.spinner(f'{model_name} 모델로 분석 중...'):
                try:
                    response = model.generate_content(f"다음 문장의 맞춤법과 띄어쓰기를 고쳐줘: {user_input}")
                    st.success("분석 완료!")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")
        else:
            st.warning("문장을 입력해주세요!")

st.markdown("---")
st.caption(f"현재 활성화된 모델: {model_name}")
