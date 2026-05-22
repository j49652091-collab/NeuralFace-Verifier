import streamlit as st

from login import login
from detector import detect_image
from similarity import compare_images
from generator import make_real

# ----------------------------
# LOAD CSS (Dark Cyber Theme)
# ----------------------------
def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="AI Detection System",
    layout="wide"
)

st.title("AI Image Detection & Similarity System")

# ----------------------------
# SESSION STATE LOGIN
# ----------------------------
if "logged" not in st.session_state:
    st.session_state.logged = False

# ----------------------------
# LOGIN PAGE
# ----------------------------
if not st.session_state.logged:

    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if login(username, password):

            st.success("Login Successful")
            st.session_state.logged = True
            st.rerun()

        else:
            st.error("Wrong username or password")

# ----------------------------
# MAIN APP
# ----------------------------
else:

    tab1, tab2 = st.tabs(["AI Detection", "Similarity"])

    # =========================
    # TAB 1 - AI DETECTION
    # =========================
    with tab1:

        st.header("Upload Image for AI Detection")

        image = st.file_uploader(
            "Upload Image",
            type=["jpg", "png", "jpeg"]
        )

        if image:

            col1, col2 = st.columns(2)

            with col1:
                st.image(image, caption="Uploaded Image", use_column_width=True)

            result, score, img = detect_image(image)

            with col2:
                st.subheader("Result")
                st.write("Status:", result)
                st.write("Confidence:", score, "%")

            # AI IMAGE HANDLING
            if result == "AI Generated":

                st.warning("AI Image Detected")

                generated = make_real(image)

                st.image(
                    generated,
                    caption="Enhanced Human-Like Version",
                    use_column_width=True
                )

    # =========================
    # TAB 2 - SIMILARITY
    # =========================
    with tab2:

        st.header("Image Similarity Checker")

        col1, col2 = st.columns(2)

        img1 = col1.file_uploader("First Image", key="img1")
        img2 = col2.file_uploader("Second Image", key="img2")

        if img1 and img2:

            col1.image(img1, caption="Image 1", use_column_width=True)
            col2.image(img2, caption="Image 2", use_column_width=True)

            similarity = compare_images(img1, img2)

            st.metric("Similarity Percentage", str(similarity) + "%")
