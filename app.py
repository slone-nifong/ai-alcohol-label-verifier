import streamlit as st

st.set_page_config(
    page_title="AI Alcohol Label Verification",
    page_icon="🍾"
)

st.title("🍾 AI Alcohol Label Verification")

st.write(
    "Upload an alcohol label image and compare it "
    "against the expected application information."
)

uploaded_file = st.file_uploader(
    "Upload Label Image",
    type=["png", "jpg", "jpeg"]
)

st.header("Expected Application Data")

brand = st.text_input("Brand Name")
class_type = st.text_input("Class/Type")
abv = st.text_input("Alcohol Content")
net_contents = st.text_input("Net Contents")

if st.button("Verify Label"):
    if uploaded_file:
        st.success("Label uploaded successfully!")
        st.info("OCR and verification engine coming next.")
    else:
        st.error("Please upload a label image.")
