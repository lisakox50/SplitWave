import streamlit as st
import matplotlib.pyplot as plt

# --- PAGE CONFIG ---
st.set_page_config(page_title="SplitWave – Bill Splitter", layout="centered")

st.title("🌊 SplitWave")
st.caption("Smart. Flexible. Borderless.")

# --- INIT STATE ---
if "participants" not in st.session_state:
    st.session_state.participants = {}
if "total_bill" not in st.session_state:
    st.session_state.total_bill = 0.0

# --- ROLE ---
role = st.radio("Who are you?", ["Organizer", "Participant"], horizontal=True)
st.markdown("---")

# --- ORGANIZER VIEW ---
if role == "Organizer":
    st.header("💰 Step 1: Set Total Bill")
    total = st.number_input("Total bill (USD)", min_value=0.01, format="%.2f", value=st.session_state.total_bill)
    if st.button("✅ Confirm Total Bill"):
        st.session_state.total_bill = total
        st.success(f"Total bill set to ${total:.2f}")

    st.header("👥 Step 2: Add Participants")
    with st.form("add_form", clear_on_submit=True):
        name = st.text_input("Name")
        amount = st.number_input("Amount (USD)", min_value=0.01, format="%.2f")
        submit = st.form_submit_button("➕ Add Participant")
        if submit:
            if name in st.session_state.participants:
                st.warning("Participant already exists.")
            else:
                st.session_state.participants[name] = {"amount": amount, "paid": False}
                st.success(f"{name} added.")

    if st.session_state.participants:
        st.header("📊 Step 3: Track Payments")
        participants = st.session_state.participants
        total_paid = sum(p["amount"] for p in participants.values() if p["paid"])
        total_bill = st.session_state.total_bill
        remaining = max(total_bill - total_paid, 0)

        st.metric("Total Bill", f"${total_bill:.2f}")
        st.metric("Paid", f"${total_paid:.2f}")
        st.metric("Remaining", f"${remaining:.2f}")

        st.subheader("Participants:")
        for name, data in participants.items():
            col1, col2, col3 = st.columns([3, 2, 2])
            col1.write(f"**{name}**")
            col2.write(f"${data['amount']:.2f}")
            if data["paid"]:
                col3.write("✅ Paid")
            else:
                if col3.button(f"Mark {name} as Paid", key=f"paid_{name}"):
                    st.session_state.participants[name]["paid"] = True
                    st.experimental_rerun()

        # --- Donut Chart ---
        st.subheader("📈 Progress")
        if total_bill > 0:
            fig, ax = plt.subplots()
            paid = total_paid
            unpaid = total_bill - paid
            ax.pie([paid, unpaid], labels=["Paid", "Unpaid"], startangle=90,
                   colors=["#4CAF50", "#FFC107"], autopct="%1.1f%%", wedgeprops=dict(width=0.4))
            st.pyplot(fig)

        if total_paid >= total_bill:
            st.balloons()
            st.success("🎉 All paid!")

        if st.button("🔁 Reset All"):
            st.session_state.participants = {}
            st.session_state.total_bill = 0.0
            st.experimental_rerun()

# --- PARTICIPANT VIEW ---
else:
    st.header("🙋 Participant Payment")
    if st.session_state.total_bill == 0:
        st.warning("Organizer has not set the bill yet.")
    else:
        name = st.text_input("Enter your name")
        if name in st.session_state.participants:
            amount = st.session_state.participants[name]["amount"]
            paid = st.session_state.participants[name]["paid"]

            st.info(f"You owe: ${amount:.2f}")
            if paid:
                st.success("✅ You have already marked as paid.")
            else:
                if st.button("Mark as Paid"):
                    st.session_state.participants[name]["paid"] = True
                    st.success("Marked as paid!")
                    st.experimental_rerun()
        else:
            st.warning("You're not in the participant list. Ask the organizer to add you.")
