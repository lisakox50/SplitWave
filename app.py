import streamlit as st

st.set_page_config(page_title="SplitWave - Flexible Bill Splitter", layout="centered")

st.title("🌊 SplitWave — Flexible Bill Splitter")

# Ввод общей суммы
total_amount = st.number_input("Enter total bill amount (USD)", min_value=0.01, format="%.2f")

if "participants" not in st.session_state:
    st.session_state.participants = {}  # {name: {'amount': float, 'paid': bool}}

st.header("Add participants and their payment amounts")

with st.form("add_participant_form", clear_on_submit=True):
    pname = st.text_input("Participant name")
    pamount = st.number_input("Amount to pay (USD)", min_value=0.01, format="%.2f")
    submitted = st.form_submit_button("Add participant")
    if submitted:
        if pname.strip() == "":
            st.error("Please enter a participant name.")
        elif pname in st.session_state.participants:
            st.error("This participant already exists.")
        else:
            st.session_state.participants[pname] = {"amount": pamount, "paid": False}
            st.success(f"Added participant {pname} with amount ${pamount:.2f}")

if st.session_state.participants:
    st.header("Participants and payment status")

    total_assigned = sum(p['amount'] for p in st.session_state.participants.values())
    st.write(f"Total bill amount: **${total_amount:.2f}**")
    st.write(f"Sum of participants' assigned payments: **${total_assigned:.2f}**")

    if abs(total_amount - total_assigned) > 0.01:
        st.warning("Warning: The sum of participants' payments does not match the total bill amount.")

    for name, data in st.session_state.participants.items():
        col1, col2, col3 = st.columns([3, 2, 2])
        with col1:
            st.write(f"**{name}**")
        with col2:
            st.write(f"Amount: ${data['amount']:.2f}")
        with col3:
            if not data['paid']:
                if st.button(f"Mark {name} as Paid", key=f"pay_{name}"):
                    st.session_state.participants[name]['paid'] = True
                    st.experimental_rerun()
            else:
                st.write("✅ Paid")

    total_paid = sum(p['amount'] for p in st.session_state.participants.values() if p['paid'])
    total_left = total_amount - total_paid

    st.markdown("---")
    st.write(f"**Total paid: ${total_paid:.2f}**")
    st.write(f"**Total left to pay: ${max(total_left, 0):.2f}**")

    if total_left <= 0 and total_assigned >= total_amount:
        st.balloons()
        st.success("All payments collected! 🎉")

    if st.button("Reset all participants and payments"):
        st.session_state.participants = {}
        st.experimental_rerun()

else:
    st.info("Add participants above to start tracking payments.")
