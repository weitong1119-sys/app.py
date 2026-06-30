import streamlit as st
from streamlit_autorefresh import st_autorefresh

# 這行指令會讓網頁每 2 秒自動重新抓取一次資料，達成同步效果
st_autorefresh(interval=2000, key="datarefresh")

# 初始化設定
if 'votes' not in st.session_state:
    st.session_state.votes = {}
if 'alive' not in st.session_state:
    st.session_state.alive = {i: True for i in range(1, 13)}

st.title("🐺 狼人殺投票系統 (自動同步版)")

# 法官控制台
with st.sidebar:
    st.header("法官操作區")
    for i in range(1, 13):
        st.session_state.alive[i] = st.checkbox(f"{i}號 玩家", value=st.session_state.alive[i])
    
    if st.button("清除本輪投票"):
        st.session_state.votes = {}
        st.rerun()

# 玩家投票介面
st.subheader("請投下你的一票")
player_id = st.selectbox("請選擇你的號碼", range(1, 13))

if st.session_state.alive.get(player_id):
    vote = st.radio("你要投給誰？", [0] + list(range(1, 13)), format_func=lambda x: "棄票" if x == 0 else f"{x}號")
    if st.button("確認投票"):
        st.session_state.votes[player_id] = vote
        st.success(f"已記錄您的投票")
        st.rerun()
else:
    st.error("您目前已出局，無法投票")

# 統計區域
st.divider()
st.subheader("目前即時票數")
if st.session_state.votes:
    results = {}
    for v in st.session_state.votes.values():
        results[v] = results.get(v, 0) + 1
    st.write(results)
else:
    st.write("目前還沒人投票")
