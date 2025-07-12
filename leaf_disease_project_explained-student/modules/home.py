import streamlit as st
import requests
import io
import base64
from PIL import Image
from modules import feedback
from modules.ai_assistant import get_disease_info
from modules.chatbot import ask_bot, reset_chat
from modules.history import save_history

# 👉 Hàm định dạng nội dung bệnh đẹp hơn
def format_disease_info(disease_info_raw: str) -> str:
    from textwrap import dedent

    seen = set()
    lines = []
    for line in disease_info_raw.splitlines():
        line = line.strip()
        if line and line not in seen:
            seen.add(line)
            lines.append(line)

    disease = ""
    cause = ""
    symptoms = ""
    treatment = ""

    for line in lines:
        if "Disease:" in line:
            disease = line.replace("Disease:", "").strip()
        elif "Cause:" in line:
            cause += "- " + line.replace("Cause:", "").strip() + "\n"
        elif "Symptoms:" in line:
            symptoms += "- " + line.replace("Symptoms:", "").strip() + "\n"
        elif "Treatment" in line or "Prevention" in line:
            treatment += "- " + line.replace("Treatment & Prevention:", "").strip() + "\n"

    formatted = f"""
### 📌 Disease:
{disease or '- No information provided'}

### 💥 Cause:
{cause or '- No cause info provided'}

### 😷 Symptoms:
{symptoms or '- No symptom info provided'}

### 💊 Treatment & Prevention:
{treatment or '- No treatment info provided'}
    """
    return dedent(formatted).strip()

def show_home(username):
    st.markdown("📱 Take or upload **one** image of a plant leaf using the **Browse files** button below.")
    st.markdown("We'll identify the plant species and any diseases present based on the image.")

    uploaded_file = st.file_uploader("📤 Upload image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="🖼️ Uploaded successfully", use_container_width=True)

        if st.button("🔍 Identify plant type and diseases"):
            buffered = io.BytesIO()
            image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode()

            # STEP 1: Leaf type detection
            st.subheader("🧬 Step 1: Identify the type of leaf...")
            leaf_type_url = "https://serverless.roboflow.com/infer/workflows/object-detection-8ndcf/leaf-type"
            leaf_type_key = "KcD4RWCv9OORn2uZ4LFv"
            leaf_payload = {
                "api_key": leaf_type_key,
                "inputs": {"image": {"type": "base64", "value": img_str}}
            }

            try:
                leaf_response = requests.post(leaf_type_url, json=leaf_payload)
                leaf_result = leaf_response.json()
                st.expander("📦 Leaf Type API Raw Response").json(leaf_result)

                predictions = (
                    leaf_result.get("outputs", [{}])[0]
                    .get("predictions", {}).get("predictions", [])
                )
                print(leaf_result)
                print(predictions)
                if not predictions:
                    st.warning("⚠️ Could not identify plant type, skipping to disease detection anyway...")
                    leaf_type = "unknown"
                else:
                    top_class = sorted(predictions, key=lambda x: x['confidence'], reverse=True)[0]['class']
                    leaf = top_class[0]
                    leaf_type = top_class.split("_")[0]
                    st.success(f"📗🍃 Detected plant type: **{leaf_type.upper()}**")
                    

            except Exception as e:
                st.error("❌ Failed to identify plant type.")
                st.exception(e)
                leaf_type = "unknown"

            # STEP 2: Detect Diseases
            st.subheader("🦠 Step 2: Detecting disease...")
            leaf_disease_url = "https://serverless.roboflow.com/infer/workflows/object-detection-8ndcf/leaf-disease-detection"
            leaf_disease_key = "KcD4RWCv9OORn2uZ4LFv"
            leaf_disease_payload = {
                "api_key": leaf_disease_key,
                "inputs": {"image": {"type": "base64", "value": img_str},
                           "type" : leaf_type,
                            }
            }
            

            try:
                disease_response = requests.post(leaf_disease_url, json = leaf_disease_payload)
                disease_result = disease_response.json()
                st.expander("📦 Disease API Raw Response").json(disease_result)
                print(disease_result) 
                # First try to get the predictions for the detected plant type
                key = f"{leaf_type}_predictions"
                if disease_response.status_code == 200:
                    disease_json = disease_response.json()
                    output = disease_json["outputs"][0]
                    print(key)
                    if key in output and output[key] is not None:
                        preds = output[key]["predictions"]
                        print(preds)
                    else:
                # Fallback: collect any detections across all crops
                        preds = []
                        for val in output.values():
                            if isinstance(val, dict) and val.get("predictions"):
                                preds.extend(val["predictions"]) 
                st.session_state["preds"] = preds
                st.session_state["last_leaf_type"] = leaf_type   
         
                if preds:
                    st.subheader("📌 Diseases detected on leaf:")
                    for pred in preds:
                        disease_class = pred["class"]
                        confidence = pred["confidence"]

                        st.markdown(f"✅ **{disease_class}** ({confidence*100:.2f}%)")
                        
                        # AI phân tích
                        disease_info = get_disease_info(disease_class, leaf_type)
                        summary = format_disease_info(disease_info)

                        with st.expander(f"🔎 Learn more about **{disease_class}**", expanded=True):
                            st.markdown(summary)
                        
                        # Lưu session + lịch sử
                        st.session_state["last_disease_summary"] = summary
                        st.session_state["last_disease_class"] = disease_class
                        st.session_state["last_confidence"] = confidence
                        st.session_state["last_leaf_type"] = leaf_type

                        save_history(username, leaf_type, disease_class, confidence, summary)
                
                else:
                    st.info("🧼 No visible disease was detected on this leaf.")
                
            except Exception as e:
                st.error("❌ Error occurred during disease detection.")
                st.exception(e)
                print(e)

    # 👉 Chatbot hiển thị sau khi đã có kết quả bệnh
    if "last_disease_summary" in st.session_state:
        st.divider()
        st.subheader("🤖 Ask the AI about your plant or disease")

        user_input = st.text_input("💬 Ask anything (e.g. how to treat the disease?)")

        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("🔁 Reset"):
                reset_chat()

        with col2:
            if st.button("Ask") and user_input:
                try:
                    # ─── re-display detected diseases so they never disappear ───
                    preds = st.session_state.get("preds", [])
                    leaf_type = st.session_state.get("last_leaf_type", "")
                    if preds:
                        st.subheader(f"📌 Diseases detected on {leaf_type} leaf:")
                        for pred in preds:
                            st.markdown(f"- **{pred['class']}** ({pred['confidence']*100:.2f}%)")
                    context = st.session_state.get("last_disease_summary", "")
                    response = ask_bot(user_input, context)
                    st.markdown(f"**You:** {user_input}")
                    st.markdown(f"**AI:** {response}")

                except Exception as e:
                    st.warning("⚠️ Chatbot error.")
                    st.exception(e)
