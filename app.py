import streamlit as st
from PIL import Image
from ocr import extract_text
from verifier import verify_label

st.set_page_config(
    page_title="AI Alcohol Label Verification",
    page_icon="🍾",
    layout="wide"
)

st.title("🍾 AI Alcohol Label Verification")

st.write(
    "Upload an alcohol label image and compare it against expected application data "
    "using OCR and intelligent text matching."
)

with st.expander("Prototype Notes"):
    st.write(
        "This prototype is designed as a standalone proof-of-concept. "
        "It uses OCR and fuzzy matching to assist label review, but final compliance decisions "
        "should remain with trained reviewers."
    )

uploaded_file = st.file_uploader(
    "Upload Label Image",
    type=["png", "jpg", "jpeg"]
)

st.header("Expected Application Data")

col1, col2 = st.columns(2)

with col1:
    brand_name = st.text_input(
        "Brand Name",
        value=st.session_state.get("brand_name", ""),
        placeholder="OLD TOM DISTILLERY",
        key="brand_name"
    )

    class_type = st.text_input(
        "Class/Type",
        value=st.session_state.get("class_type", ""),
        placeholder="Kentucky Straight Bourbon Whiskey",
        key="class_type"
    )

with col2:
    alcohol_content = st.text_input(
        "Alcohol Content",
        value=st.session_state.get("alcohol_content", ""),
        placeholder="45% Alc./Vol. or 90 Proof",
        key="alcohol_content"
    )

    net_contents = st.text_input(
        "Net Contents",
        value=st.session_state.get("net_contents", ""),
        placeholder="750 mL",
        key="net_contents"
    )

if uploaded_file:
    st.subheader("Uploaded Label Preview")
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)

if st.button("Verify Label"):
    if not uploaded_file:
        st.error("Please upload a label image first.")
    else:
        with st.spinner("Extracting label text and verifying fields..."):
            extracted_text = extract_text(uploaded_file)

            expected_data = {
                "brand_name": brand_name,
                "class_type": class_type,
                "alcohol_content": alcohol_content,
                "net_contents": net_contents
            }

            results = verify_label(expected_data, extracted_text)

        st.header("Verification Results")

        pass_count = sum(1 for r in results.values() if r["status"] == "PASS")
        review_count = sum(1 for r in results.values() if r["status"] == "REVIEW")
        fail_count = sum(1 for r in results.values() if r["status"] == "FAIL")

        if fail_count == 0 and review_count == 0:
            st.success("Overall Status: PASS")
        elif fail_count == 0:
            st.warning("Overall Status: REVIEW")
        else:
            st.error("Overall Status: FAIL")

        st.write(f"Passed: {pass_count} | Review: {review_count} | Failed: {fail_count}")

        for field, result in results.items():
            status = result["status"]
            score = result["score"]

            if status == "PASS":
                st.success(f"{field}: PASS — {score}%")
            elif status == "REVIEW":
                st.warning(f"{field}: REVIEW — {score}%")
            elif status == "FAIL":
                st.error(f"{field}: FAIL — {score}%")
            else:
                st.info(f"{field}: {status}")

            st.caption(result["note"])

        st.subheader("Extracted OCR Text")
        st.text_area("Detected text from label", extracted_text, height=300)