import streamlit as st
import google.generativeai as genai

# 1. 페이지 기본 설정
st.set_page_config(page_title="AI 맞춤법 선생님", page_icon="✍️", layout="wide")

# 2. 사이드바: API 키 입력창 생성
with st.sidebar:
    st.title("🔑 보안 설정")
    # type="password"로 설정하면 입력할 때 별표(***)로 표시되어 안전합니다.
    user_api_key = st.text_input("Gemini API Key를 입력하세요", type="password")
    
    st.markdown("---")
    st.markdown("""
    **사용 방법:**
    1. [Google AI Studio](https://aistudio.google.com/app/apikey) 접속
    2. API Key 발급 (무료)
    3. 위 칸에 복사/붙여넣기
    """)
    st.caption("v1.0 - 키는 어디에도 저장되지 않고 세션 중에만 유지됩니다.")

# 3. 메인 화면 UI
st.title("✍️ AI 맞춤법 & 띄어쓰기 교정기")
st.write("문장을 입력하면 AI가 맞춤법과 띄어쓰기를 완벽하게 교정해 드립니다.")

# 4. 핵심 로직
if user_api_key:
    # 사용자가 키를 입력했을 때만 실행
    try:
        genai.configure(api_key=user_api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')

        user_input = st.text_area(
            "교정받을 문장을 입력하세요:", 
            placeholder="예: 오늘 날씨 가 참좋내요 점심 머먹 을까요?",
            height=200
        )

        if st.button("AI 선생님에게 검사받기 ✨"):
            if user_input.strip():
                with st.spinner('AI가 열심히 문장을 읽고 있습니다...'):
                    # 프롬프트를 구체적으로 작성하여 결과 품질을 높임
                    prompt = (
                        f"너는 전문 한국어 교열 작가야. 다음 문장의 맞춤법과 띄어쓰기를 교정해줘.\n"
                        f"결과는 '교정된 문장'과 '수정된 부분들에 대한 간단한 설명'을 포함해서 보기 좋게 출력해줘.\n\n"
                        f"입력 문장: {user_input}"
                    )
                    
                    response = model.generate_content(prompt)
                    
                    st.success("분석을 완료했습니다!")
                    st.subheader("✅ 교정 결과")
                    st.info(response.text)
            else:
                st.warning("교정할 문장을 먼저 입력해 주세요.")

    except Exception as e:
        # 키가 잘못되었거나 서버 오류가 날 경우 처리
        st.error(f"오류가 발생했습니다: {e}")
        st.info("입력하신 API 키가 정확한지 다시 확인해 보세요.")

else:
    # 사용자가 키를 입력하지 않았을 때 보여줄 화면
    st.divider()
    st.warning("⚠️ 시작하기 전에 왼쪽 사이드바에 API 키를 입력해 주세요.")
    st.image("https://images.unsplash.com/photo-1455390582262-044cdead277a?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80", caption="글쓰기를 도와주는 AI")
