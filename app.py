import streamlit as st
import tempfile

from login import login
from detector import detect_image
from generator import make_real
from face_recognition import compare_faces

# ----------------------------
# LOAD CSS
# ----------------------------
def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="AI Forensic Security System",
    layout="wide"
)

st.title("🧬 AI Forensic & Face Recognition System")

# ----------------------------
# SESSION STATE
# ----------------------------
if "logged" not in st.session_state:
    st.session_state.logged = False

# ----------------------------
# LOGIN
# ----------------------------
if not st.session_state.logged:

    st.subheader("Login Panel")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if login(username, password):
            st.success("Login Successful")
            st.session_state.logged = True
            st.rerun()
        else:
            st.error("Invalid credentials")

# ----------------------------
# MAIN APP
# ----------------------------
else:

    tab1, tab2 = st.tabs([
        "🧬 AI Forensics Detection",
        "👤 Face Recognition"
    ])

    # =========================
    # TAB 1 - FORENSIC DETECTION
    # =========================
    with tab1:

        st.header("Upload Image for Forensic Analysis")

        image = st.file_uploader(
            "Upload Image",
            type=["jpg", "png", "jpeg"]
        )

        if image:

            col1, col2 = st.columns(2)

            with col1:
                st.image(image, caption="Uploaded Image", use_container_width=True)

            status, score, img = detect_image(image)

            with col2:
                st.subheader("Forensic Result")
                st.write("Status:", status)
                st.write("Digital Signature Score:", score, "%")

            # If AI detected → enhance image
            if "AI" in status:

                st.warning("Synthetic / AI Modified Image Detected")

                enhanced = make_real(image)

                st.image(
                    enhanced,
                    caption="Enhanced Human-Like Output",
                    use_container_width=True
                )

    # =========================
    # TAB 2 - FACE RECOGNITION
    # =========================
    with tab2:

        st.header("Face Recognition (DeepFace Embeddings)")

        col1, col2 = st.columns(2)

        img1 = col1.file_uploader("First Face Image", type=["jpg", "png", "jpeg"])
        img2 = col2.file_uploader("Second Face Image", type=["jpg", "png", "jpeg"])

        if img1 and img2:

            col1.image(img1, caption="Image 1", use_container_width=True)
            col2.image(img2, caption="Image 2", use_container_width=True)

            # save temporary files for DeepFace
            def save_temp(file):
                temp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
                temp.write(file.read())
                temp.close()
                return temp.name

            path1 = save_temp(img1)
            path2 = save_temp(img2)

            similarity = compare_faces(path1, path2)

            st.metric("Face Similarity Score", str(similarity) + "%")
