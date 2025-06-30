import streamlit as st

# ---------- CONFIG ----------
st.set_page_config(page_title="SplitWave – Smart Bill Splitter", layout="centered")

# ---------- TITLE ----------
st.title("🌊 SplitWave")
st.caption("Smart, flexible, and borderless bill splitting")

# ---------- STATE ----------
if "participants" not in st.session_state:
    st.session_state.participants = {}

# ---------- SECTION 1: BILL CREATION ----------
st.subheader("1. Set the total bill")

total_amount = st.number_input("Total bill amount (USD)", min_value=0.01, format="%.2f")

st.markdown("---")

# ---------- SECTION 2: ADD PARTICIPANTS ----------
st.subheader("2. Add participants and their contributions")

with st.form("add_form", clear_on_submit=True):
    name = st.text_input("Participant name")
    amount = st.number_input("Amount to contribute (USD)", min_value=0.01, format="%.2f")
    submit = st.form_submit_button("➕ Add participant")

    if submit:
        if name.strip() == "":
            st.warning("Name cannot be empty.")
        elif name in st.session_state.participants:
            st.warning("This participant is already added.")
        else:
            st.session_state.participants[name] = {"amount": amount, "paid": False}
            st.success(f"{name} added successfully!")

# ---------- SECTION 3: STATUS ----------
if st.session_state.participants:
    st.markdown("---")
    st.subheader("3. Track payments")

    total_assigned = sum(p["amount"] for p in st.session_state.participants.values())
    total_paid = sum(p["amount"] for p in st.session_state.participants.values() if p["paid"])
    total_remaining = max(total_amount - total_paid, 0)

    st.write(f"💰 **Total bill:** ${total_amount:.2f}")
    st.write(f"🧾 **Assigned among participants:** ${total_assigned:.2f}")
    st.write(f"✅ **Paid:** ${total_paid:.2f}")
    st.write(f"🕐 **Remaining:** ${total_remaining:.2f}")

    # Progress bar
    progress = min(total_paid / total_amount, 1.0) if total_amount else 0
    st.progress(progress)

    st.markdown("### Participants")

    for name, data in st.session_state.participants.items():
        col1, col2, col3 = st.columns([4, 3, 2])
        with col1:
            st.write(f"**{name}**")
        with col2:
            st.write(f"${data['amount']:.2f}")
        with col3:
            if not data["paid"]:
                if st.button("Mark as Paid", key=f"pay_{name}"):
                    st.session_state.participants[name]["paid"] = True
                    st.success(f"{name} marked as paid.")
            else:
                st.write("✅ Paid")

    # All paid
    if total_paid >= total_amount:
        st.success("🎉 All payments collected!")
        st.balloons()

    # Reset
    st.markdown("---")
    if st.button("🔄 Reset all"):
        st.session_state.participants = {}
        st.experimental_rerun()

else:
    st.info("Add at least one participant to begin tracking.")
