import streamlit as st

# Currency exchange rates relative to USD
CURRENCY_RATES = {
    "USD": 1,
    "EUR": 0.9,
    "KRW": 1300,
    "INR": 83,
}

st.set_page_config(page_title="SplitWave - Smart Bill Splitter", layout="centered")

st.title("🌊 SplitWave — Next-gen Bill Splitter")

st.markdown("""
Welcome to SplitWave! Create a bill, share it with friends, and track who has paid in their preferred currency.
""")

# --- Bill Creation ---
st.header("1. Create a Bill")

total = st.number_input("Enter total bill amount (USD)", min_value=0.01, format="%.2f")
people = st.number_input("Number of people splitting", min_value=1, step=1, value=2)

if total and people:
    per_person_usd = total / people
    st.write(f"Each person should pay: **${per_person_usd:.2f} USD**")

    if "bill_created" not in st.session_state or not st.session_state.bill_created:
        if st.button("Create Bill"):
            st.session_state.bill_created = True
            st.session_state.payments = {}
            st.success("Bill created! Share this app URL with your friends.")

# --- Join & Pay ---
if st.session_state.get("bill_created", False):
    st.header("2. Join & Mark Your Payment")

    name = st.text_input("Enter your name")
    currency = st.selectbox("Select your currency", list(CURRENCY_RATES.keys()))
    amount_local = per_person_usd * CURRENCY_RATES[currency] if per_person_usd else 0

    if name:
        paid = st.session_state.payments.get(name, False)

        col1, col2 = st.columns([1, 3])
        with col1:
            if not paid and st.button("Mark as Paid"):
                st.session_state.payments[name] = True
                st.success(f"Thank you {name}, you paid {amount_local:.2f} {currency}!")

        with col2:
            st.write(f"You owe: **{amount_local:.2f} {currency}**")
    else:
        st.info("Please enter your name to mark payment.")

    # --- Payment status ---
    st.header("3. Payment Status")

    payments = st.session_state.payments
    if payments:
        paid_count = len(payments)
        st.write(f"**{paid_count} / {people} paid**")
        for p_name in payments:
            st.write(f"- ✅ {p_name}")
        # Show unpaid participants as placeholders (optional)
        unpaid_count = people - paid_count
        if unpaid_count > 0:
            st.write(f"❌ {unpaid_count} person(s) not paid yet")
        if paid_count == people:
            st.balloons()
            st.success("All paid! 🎉")
    else:
        st.write("No payments marked yet.")

    # Reset button
    if st.button("Reset Payments"):
        st.session_state.payments = {}
        st.success("Payments reset, you can start over.")
else:
    st.info("Create a bill above to get started.")
