import streamlit as st
import tempfile

from login import login
from detector import detect_image
from face_recognition import compare_faces

st.set_page_config(
page_title="AI Forensic System",
layout="wide"
)

with open(
"style.css"
) as f:

    st.markdown(
    f"<style>{f.read()}</style>",
    unsafe_allow_html=True
    )

st.title(
"AI Deepfake & Face Forensic System"
)

if "logged" not in st.session_state:

    st.session_state.logged=False

if not st.session_state.logged:

    st.subheader(
    "Login"
    )

    username=st.text_input(
    "Username"
    )

    password=st.text_input(
    "Password",
    type="password"
    )

    if st.button(
    "Login"
    ):

        if login(
        username,
        password
        ):

            st.session_state.logged=True

            st.rerun()

        else:

            st.error(
            "Wrong credentials"
            )

else:

    tab1,tab2=st.tabs(
    [
    "Forensic Detection",
    "Face Recognition"
    ]
    )

    with tab1:

        image=st.file_uploader(
        "Upload Image"
        )

        if image:

            col1,col2=st.columns(2)

            col1.image(
            image
            )

            status,score,img=detect_image(
            image
            )

            col2.write(
            "Status:",
            status
            )

            col2.metric(
            "Digital Signature Score",
            str(score)+"%"
            )

    with tab2:

        col1,col2=st.columns(2)

        img1=col1.file_uploader(
        "Image 1"
        )

        img2=col2.file_uploader(
        "Image 2"
        )

        if img1 and img2:

            col1.image(
            img1
            )

            col2.image(
            img2
            )

            def save(file):

                temp=tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".jpg"
                )

                temp.write(
                file.read()
                )

                temp.close()

                return temp.name

            path1=save(img1)
            path2=save(img2)

            result=compare_faces(
            path1,
            path2
            )

            st.metric(
            "Similarity",
            str(
            result[
            "similarity"
            ]
            )+"%"
            )

            st.code(
            result[
            "signature"
            ]
            )

            st.success(
            result[
            "status"
            ]
            )
