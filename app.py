import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정
st.set_page_config(page_title="AI 맞춤법 선생님", page_icon="✍️")

# 2. 사이드바: API 키 입력
with st.sidebar:
    st.title("🔑 설정")
    user_api_key = st.text_input("Gemini API Key를 입력하세요", type="password")
    st.info("키 발급: [Google AI Studio](https://aistudio.google.com/app/apikey)")

st.title("✍️ AI 맞춤법 & 띄어쓰기 교정기")

# 3. 모델 로드 함수 (404 에러 방지 로직)
def get_working_model(api_key):
    try:
        genai.configure(api_key=api_key)
        # 내 계정에서 사용 가능한 모델 리스트 확인
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # 선호하는 순서대로 모델 선택
        if 'models/gemini-1.5-flash' in models:
            return genai.GenerativeModel('gemini-1.5-flash'), 'gemini-1.5-flash'
        elif 'models/gemini-pro' in models:
            return genai.GenerativeModel('gemini-pro'), 'gemini-pro'
        else:
            # 리스트 중 첫 번째 모델 선택
            return genai.GenerativeModel(models[0]), models[0]
    except Exception as e:
        return None, str(e)

# 4. 메인 로직
if user_api_key:
    model, model_name = get_working_model(user_api_key)
    
    if model:
        st.caption(f"현재 연결된 모델: {model_name}")
        user_input = st.text_area("교정받을 문장을 입력하세요:", placeholder="예: 오늘 날씨 가 참좋내요 점심 머먹 을까요?", height=200)

        if st.button("AI 선생님에게 검사받기 ✨"):
            if user_input.strip():
                with st.spinner('분석 중...'):
                    try:
                        prompt = f"너는 전문 교열 작가야. 다음 문장의 맞춤법과 띄어쓰기를 교정해줘. 결과는 '교정 문장'과 '설명'으로 나눠서 보여줘.\n\n문장: {user_input}"
                        response = model.generate_content(prompt)
                        
                        st.success("검사 완료!")
                        st.divider()
                        st.markdown(response.text)
                    except Exception as e:
                        st.error(f"분석 중 오류가 발생했습니다: {e}")
            else:
                st.warning("문장을 입력해주세요.")
    else:
        st.error(f"모델을 불러오지 못했습니다. API 키를 확인해주세요. (상세: {model_name})")

else:
    st.divider()
    st.warning("👈 시작하려면 왼쪽 사이드바에 API 키를 입력해 주세요.")
