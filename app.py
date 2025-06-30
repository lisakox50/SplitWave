import streamlit as st
import matplotlib.pyplot as plt

# ---------- CONFIG ----------
st.set_page_config(page_title="SplitWave – Smart Bill Splitter", layout="centered")
st.title("🌊 SplitWave")
st.caption("Smart. Flexible. Borderless bill splitting.")

# ---------- INIT STATE ----------
if "participants" not in st.session_state:
    st.session_state.participants = {}
if "total_bill" not in st.session_state:
    st.session_state.total_bill = 0.0

# ---------- ROLE SELECTION ----------
role = st.radio("Who are you?", ["Organizer", "Participant"], horizontal=True)
st.markdown("---")

# ---------- ORGANIZER VIEW ----------
if role == "Organizer":
    tab1, tab2, tab3 = st.tabs(["💰 Create Bill", "👥 Add Participants", "📊 Track Payments"])

    with tab1:
        st.subheader("💰 Set the total bill amount")
        bill = st.number_input("Total bill (USD)", min_value=0.01, format="%.2f")
        if st.button("Set Bill"):
            st.session_state.total_bill = bill
            st.success(f"Total bill set to ${bill:.2f}")

    with tab2:
        st.subheader("👥 Add participant and their contribution")

        with st.form("add_participant", clear_on_submit=True):
            name = st.text_input("Participant name")
            amount = st.number_input("Amount to pay (USD)", min_value=0.01, format="%.2f")
            add = st.form_submit_button("➕ Add")

            if add:
                if not name.strip():
                    st.warning("Please enter a name.")
                elif name in st.session_state.participants:
                    st.warning("Participant already added.")
                else:
                    st.session_state.participants[name] = {"amount": amount, "paid": False}
                    st.success(f"{name} added with ${amount:.2f}")

    with tab3:
        st.subheader("📊 Payment Status")

        total_bill = st.session_state.total_bill
        participants = st.session_state.participants
        total_paid = sum(p["amount"] for p in participants.values() if p["paid"])
        total_remaining = max(total_bill - total_paid, 0)
        total_assigned = sum(p["amount"] for p in participants.values())

        # METRICS
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Bill", f"${total_bill:.2f}")
        col2.metric("Paid", f"${total_paid:.2f}")
        col3.metric("Remaining", f"${total_remaining:.2f}")

        if abs(total_assigned - total_bill) > 0.01:
            st.warning("⚠️ Sum of participant payments does not match total bill.")

        st.markdown("### 🧾 Participant List")

        for name, data in participants.items():
            col1, col2, col3 = st.columns([4, 3, 2])
            col1.write(f"**{name}**")
            col2.write(f"${data['amount']:.2f}")
            if data["paid"]:
                col3.write("✅ Paid")
            else:
                if col3.button("Mark as Paid", key=f"pay_{name}"):
                    st.session_state.participants[name]["paid"] = True
                    st.experimental_rerun()

        # Donut chart
        st.markdown("### 📈 Progress")
        if total_bill > 0:
            fig, ax = plt.subplots()
            ax.pie(
                [total_paid, max(total_bill - total_paid, 0)],
                labels=["Paid", "Unpaid"],
                colors=["#4CAF50", "#FF9800"],
                startangle=90,
                counterclock=False,
                wedgeprops=dict(width=0.5),
                autopct="%1.1f%%"
            )
            st.pyplot(fig)

        if total_paid >= total_bill and total_bill > 0:
            st.balloons()
            st.success("🎉 All payments complete!")

        if st.button("🔄 Reset All"):
            st.session_state.participants = {}
            st.session_state.total_bill = 0.0
            st.experimental_rerun()

# ---------- PARTICIPANT VIEW ----------
else:
    st.subheader("🙋‍♀️ Participant Payment")
    total_bill = st.session_state.total_bill

    if total_bill == 0:
        st.warning("Organizer hasn't set the bill yet.")
    else:
        name = st.text_input("Enter your name")
        if name in st.session_state.participants:
            data = st.session_state.participants[name]
            st.info(f"You were assigned: **${data['amount']:.2f}**")

            if data["paid"]:
                st.success("✅ You have already marked as paid.")
            else:
                if st.button("Mark as Paid"):
                    st.session_state.participants[name]["paid"] = True
                    st.success("✅ Marked as paid!")
                    st.experimental_rerun()
        else:
            st.warning("Your name is not found in the participant list. Ask the organizer to add you.")
