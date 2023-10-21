# 以下を「app.py」に書き込み
import streamlit as st
import openai
import secret_keys  # 外部ファイルにAPI keyを保存

openai.api_key = secret_keys.openai_api_key

system_prompt = """
You are an excellent French teacher.
You are expected to give advice on French composition, French conversation, listening and reading, etc., to help students improve their French language skills according to their needs.
Your role is to improve your students' French language skills, so please do not answer any non-French questions, for example

* 旅行
* 料理
* 芸能人
* 映画
* 科学
* 歴史
"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title(" 「フランス語講師」ボット")
st.image("/content/DALL·E 2023-10-21 21.08.45 - illustration of a beautiful woman, dressed in a chic and sophisticated attire, holding a French textbook and gesturing gracefully as she teaches, with.png")
st.write("Apprécions le français !")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
