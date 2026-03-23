import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:5000"

st.title("🎮 Tic-Tac-Toe (Streamlit + Flask)")

# Session state for game
if "board" not in st.session_state:
    st.session_state.board = [" " for _ in range(9)]
if "current_player" not in st.session_state:
    st.session_state.current_player = None
if "game_started" not in st.session_state:
    st.session_state.game_started = False

# Player inputs
player1 = st.text_input("Player 1 Name")
player2 = st.text_input("Player 2 Name")
symbol = st.radio("Player 1, choose your symbol:", ["X", "O"])

if st.button("Start Game"):
    if not player1 or not player2:
        st.error("Please enter both player names")
    else:
        res = requests.post(f"{BACKEND_URL}/start-game", json={
            "player1": player1,
            "player2": player2,
            "symbol": symbol
        }).json()

        st.session_state.player1 = res["player1"]
        st.session_state.player2 = res["player2"]
        st.session_state.p1_symbol = res["player1_symbol"]
        st.session_state.p2_symbol = res["player2_symbol"]
        st.session_state.current_player = res["first_player"]
        st.session_state.board = [" " for _ in range(9)]
        st.session_state.game_started = True

        st.success(f"{res['first_player']} starts first!")

# Game UI
if st.session_state.game_started:
    st.write(f"**{st.session_state.player1}** is {st.session_state.p1_symbol}")
    st.write(f"**{st.session_state.player2}** is {st.session_state.p2_symbol}")
    st.write(f"### Turn: {st.session_state.current_player}")

    def check_winner(sym):
        b = st.session_state.board
        wins = [
            (0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)
        ]
        for a,b1,c in wins:
            if b[a] == b[b1] == b[c] == sym:
                return True
        return False

    cols = st.columns(3)
    for i in range(9):
        if i % 3 == 0:
            cols = st.columns(3)

        if cols[i % 3].button(st.session_state.board[i] if st.session_state.board[i] != " " else " ", key=i):
            if st.session_state.board[i] == " ":
                sym = st.session_state.p1_symbol if st.session_state.current_player == st.session_state.player1 else st.session_state.p2_symbol
                st.session_state.board[i] = sym

                # Check win
                if check_winner(sym):
                    st.success(f"🎉 {st.session_state.current_player} wins!")

                    # Save result
                    requests.post(f"{BACKEND_URL}/save-result", json={
                        "player1": st.session_state.player1,
                        "player2": st.session_state.player2,
                        "player1_symbol": st.session_state.p1_symbol,
                        "player2_symbol": st.session_state.p2_symbol,
                        "first_player": st.session_state.current_player,
                        "winner": st.session_state.current_player
                    })

                    st.session_state.game_started = False
                    st.stop()

                # Check draw
                if " " not in st.session_state.board:
                    st.info("🤝 It's a draw!")

                    requests.post(f"{BACKEND_URL}/save-result", json={
                        "player1": st.session_state.player1,
                        "player2": st.session_state.player2,
                        "player1_symbol": st.session_state.p1_symbol,
                        "player2_symbol": st.session_state.p2_symbol,
                        "first_player": st.session_state.current_player,
                        "winner": "Draw"
                    })

                    st.session_state.game_started = False
                    st.stop()

                # Switch player
                st.session_state.current_player = (
                    st.session_state.player2
                    if st.session_state.current_player == st.session_state.player1
                    else st.session_state.player1
                )

                st.rerun()