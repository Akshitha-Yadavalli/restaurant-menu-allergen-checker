import streamlit as st
import matplotlib.pyplot as plt
import time
from rag import analyze_menu

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Restaurant Menu Allergen Checker",
    page_icon="🍽",
    layout="wide"
)

# ---------------- SESSION ---------------- #

if "results" not in st.session_state:
    st.session_state.results = []

# ---------------- SIDEBAR ---------------- #

st.sidebar.title("🍽 Restaurant Menu Checker")

st.sidebar.success("🤖 AI Powered using RAG")

st.sidebar.markdown("""
## 📌 Features

✅ Upload Restaurant Menu

✅ Paste Menu

✅ Allergy Detection

✅ Ingredient Retrieval

✅ Risk Analysis

✅ Download Report

---

## 🛠 Technology

- Python
- Streamlit
- RAG (Knowledge Base)
- Matplotlib

---

IBM SkillsBuild Internship Project
""")

# ---------------- HEADER ---------------- #

st.title("🍽 Restaurant Menu Allergen Checker")

st.write(
    "Upload a restaurant menu or paste dishes below. "
    "The system retrieves ingredient information from a "
    "knowledge base and checks it against your allergies."
)

st.markdown("---")

# ---------------- INPUT ---------------- #

uploaded_file = st.file_uploader(
    "📂 Upload Restaurant Menu (.txt)",
    type=["txt"]
)

menu = ""

if uploaded_file is not None:
    menu = uploaded_file.read().decode("utf-8")

menu = st.text_area(
    "📋 Or Paste Restaurant Menu",
    value=menu,
    height=220,
    placeholder="""Cheese Pizza
Chicken Burger
Chocolate Cake
Shrimp Curry
Peanut Noodles
Veg Salad
Butter Chicken
Paneer Butter Masala
Margherita Pizza
Veg Fried Rice"""
)

allergies = st.text_input(
    "🤧 Enter Allergies (comma separated)",
    placeholder="Milk, Peanut, Shellfish"
)

# ---------------- ANALYZE ---------------- #

if st.button("🔍 Analyze Menu", use_container_width=True):

    if menu.strip() == "" or allergies.strip() == "":
        st.warning("Please enter both menu and allergies.")
        st.stop()

    progress = st.progress(0)

    for i in range(100):
        time.sleep(0.01)
        progress.progress(i + 1)

    progress.empty()

    with st.spinner("🤖 Retrieving knowledge and analyzing menu..."):
        time.sleep(1)

    results = analyze_menu(menu, allergies)

    st.session_state.results = results

# ---------------- SHOW RESULTS ---------------- #

if st.session_state.results:

    results = st.session_state.results

    total = len(results)

    risky = len(
        [r for r in results if r["status"] == "Risky"]
    )

    safe = total - risky

    risk_percent = round((risky / total) * 100, 2)

    st.markdown("---")

    st.subheader("📊 Analysis Dashboard")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("🍽 Total Dishes", total)
    c2.metric("⚠ Risky", risky)
    c3.metric("✅ Safe", safe)
    c4.metric("📈 Risk %", f"{risk_percent}%")

    fig, ax = plt.subplots(figsize=(4, 4))

    ax.pie(
        [safe, risky],
        labels=["Safe", "Risky"],
        autopct="%1.1f%%",
        startangle=90
    )

    st.pyplot(fig)

    st.markdown("---")

    search = st.text_input("🔍 Search Dish")

    if search:

        results = [
            r for r in results
            if search.lower() in r["dish"].lower()
        ]

    st.subheader("🍴 Dish Analysis")

    report = ""

    for item in results:

        if item["status"] == "Risky":

            icon = "🔴" if item["risk"] == "High" else "🟡"

            st.error(f"""
### ⚠ {item['dish']}

**Status:** {item['status']}

**Risk Level:** {icon} {item['risk']}

**Ingredients Retrieved:**
{item['ingredients']}

**Matched Ingredients:**
{item['matched']}

**Detected Allergens:**
{item['allergens']}

**Recommendation:**
{item['suggestion']}
""")

        else:

            st.success(f"""
### ✅ {item['dish']}

**Status:** Safe

**Risk Level:** 🟢 Low

**Ingredients Retrieved:**
{item['ingredients']}

**Recommendation:**
{item['suggestion']}
""")

        report += f"""
Dish : {item['dish']}
Status : {item['status']}
Risk : {item['risk']}
Ingredients : {item['ingredients']}
Matched : {item['matched']}
Allergens : {item['allergens']}
Recommendation : {item['suggestion']}

----------------------------------------------------
"""

    st.download_button(
        "📥 Download Report",
        report,
        file_name="Restaurant_Allergen_Report.txt"
    )

    st.markdown("---")

    st.subheader("💬 Ask AI About a Dish")

    question = st.text_input(
        "Example: Is Cheese Pizza safe?"
    )

    if st.button("Ask AI"):

        if question == "":
            st.warning("Enter your question.")

        else:

            found = False

            for item in st.session_state.results:

                if item["dish"].lower() in question.lower():

                    found = True

                    if item["status"] == "Risky":

                        st.chat_message("assistant").write(f"""
⚠ **{item['dish']}**

Risk Level : {item['risk']}

Ingredients :
{item['ingredients']}

Detected Allergens :
{item['allergens']}

Recommendation :
{item['suggestion']}
""")

                    else:

                        st.chat_message("assistant").write(f"""
✅ **{item['dish']}**

Safe to consume.

Ingredients :
{item['ingredients']}
""")

                    break

            if not found:

                st.chat_message("assistant").write(
                    "❌ Dish not found."
                )

st.markdown("---")

st.success("""
## 🤖 RAG Workflow

📄 Menu

⬇

📚 Retrieve Ingredients

⬇

⚠ Compare Allergies

⬇

🤖 Generate Report
""")

st.caption("IBM SkillsBuild Internship Project")