import streamlit as st

from login import login
from detector import detect_image
from similarity import compare_images
from generator import make_real

st.set_page_config(
page_title="AI Detection System",
layout="wide"
)

st.title("AI Image Detection and Similarity System")

if "logged" not in st.session_state:
    st.session_state.logged=False

if st.session_state.logged==False:

    st.subheader("Login")

    username=st.text_input("Username")
    password=st.text_input(
    "Password",
    type="password"
    )

    if st.button("Login"):

        if login(username,password):

            st.success("Login Successful")

            st.session_state.logged=True
            st.rerun()

        else:

            st.error("Wrong credentials")

else:

    tab1,tab2=st.tabs(
    ["AI Detection",
    "Similarity"]
    )

    with tab1:

        st.header("Upload Image")

        image=st.file_uploader(
        "Upload Image",
        type=["jpg","png","jpeg"]
        )

        if image:

            result,score,img=detect_image(image)

            st.image(img)

            st.write("Result:",result)
            st.write("Confidence:",score)

            if result=="AI Generated":

                st.warning(
                "AI Image Detected"
                )

                generated=make_real(image)

                st.image(
                generated,
                caption="Human version"
                )

    with tab2:

        st.header(
        "Image Similarity"
        )

        img1=st.file_uploader(
        "First Image",
        key=1
        )

        img2=st.file_uploader(
        "Second Image",
        key=2
        )

        if img1 and img2:

            sim=compare_images(
            img1,
            img2
            )

            st.metric(
            "Similarity %",
            str(sim)+"%"
            )
