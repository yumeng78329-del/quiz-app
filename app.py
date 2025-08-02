import streamlit as st
import pandas as pd

st.title("📝 English Quiz System")

uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        required_columns = ["question", "option_A", "option_B", "option_C", "option_D", "answer"]
        if all(col in df.columns for col in required_columns):
            st.success("📄 File successfully loaded!")
            if "index" not in st.session_state:
                st.session_state.index = 0
                st.session_state.score = 0
                st.session_state.answered = False

            if st.session_state.index < len(df):
                row = df.iloc[st.session_state.index]
                st.subheader(f"Question {st.session_state.index + 1}: {row['question']}")
                options = ["A", "B", "C", "D"]
                selected = st.radio(
                    "Choose your answer:",
                    options,
                    format_func=lambda x: f"{x}. {row[f'option_{x}']}"
                )

                if st.button("Submit Answer"):
                    if selected == row["answer"]:
                        st.success("✅ Correct!")
                        st.session_state.score += 1
                    else:
                        correct_option = row[f"option_{row['answer']}"]
                        st.error(f"❌ Wrong! Correct answer is {row['answer']}. {correct_option}")
                    st.session_state.answered = True

                if st.session_state.answered and st.button("Next Question"):
                    st.session_state.index += 1
                    st.session_state.answered = False
            else:
                st.balloons()
                st.success(f"You’ve completed the quiz! Score: {st.session_state.score}/{len(df)}")
        else:
            st.error("Missing required columns in CSV.")
    except Exception as e:
        st.error(f"Error reading file: {e}")
        if st.button("🔄 Restart Quiz"):
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.experimental_rerun()

