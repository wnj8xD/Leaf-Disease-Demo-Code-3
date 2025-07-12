# diagnose.py - hiện thông tin bệnh
import json
import streamlit as st

import streamlit as st
import json

def load_disease_info():
    # Nếu bạn đã lưu cái JSON đó thành file disease_info.json,
    # thì có thể mở file; nếu không, bạn có thể paste thẳng dict vào đây.
    # Ví dụ với dict trực tiếp:
    return {
      "coffee_leaf_rust": {
        "name": "Coffee Leaf Rust",
        "description": "Caused by the fungus Hemileia vastatrix. Orange-yellow spots appear on the underside of the leaves, causing early leaf drop and reduced yield.",
        "solution": "Regularly spray with Mancozeb or Copper Hydroxide. Prune and destroy infected leaves, and keep the plantation well-ventilated."
      },
      "durian_algal_leaf": {
        "name": "Algal Leaf Disease in Durian",
        "description": "Reddish-brown or orange spots appear on the leaves, caused by the alga Cephaleuros virescens.",
        "solution": "Prune affected leaves and spray with a copper-based fungicide."
      },
      "durian_allocaridara_attack": {
        "name": "Durian Damaged by Allocaridara Insects",
        "description": "Allocaridara insects damage young leaf tissues and cause leaf edges to curl.",
        "solution": "Use selective biological or chemical insecticides. Monitor regularly."
      },
      "durian_leaf_blight": {
        "name": "Durian Leaf Blight",
        "description": "Leaf edges are scorched and dry either partially or completely, often caused by fungi or adverse environmental conditions.",
        "solution": "Water appropriately, improve ventilation. Apply antifungal spray if necessary."
      },
      "durian_phomopsis_leaf_spot": {
        "name": "Phomopsis Leaf Spot on Durian",
        "description": "Caused by Phomopsis spp. fungi, creating black circular spots on leaves, which may lead to leaf drop.",
        "solution": "Remove infected leaves and apply fungicides containing carbendazim or mancozeb."
      },
      "lemon_deficiency_leaf": {
        "name": "Nutrient Deficiency in Lemon Leaves",
        "description": "Leaves appear pale yellow with green veins, caused by deficiencies in nitrogen, iron, or magnesium.",
        "solution": "Apply balanced fertilizers. Use foliar fertilizers containing micronutrients."
      },
      "lemon_leaf_anthracnose": {
        "name": "Anthracnose on Lemon Leaves",
        "description": "Caused by Colletotrichum spp. fungi. Leaves develop brown, slightly sunken spots that expand over time.",
        "solution": "Prune diseased branches and leaves. Spray with copper-based fungicides or azoxystrobin."
      },
      "lemon_spider_mite_leaf": {
        "name": "Lemon Leaves Attacked by Spider Mites",
        "description": "Spider mites suck sap from the leaves, causing yellowing, drying, and leaf drop.",
        "solution": "Use high-pressure water to wash off mites. Apply biological miticides or abamectin."
      },
      "coffee_leaf_red_spider_mite": {
        "name": "Coffee Leaves Infested by Red Spider Mites",
        "description": "Red spider mites damage the underside of the leaves, forming yellow spots that reduce photosynthesis and yield.",
        "solution": "Keep soil moisture adequate, spray miticides like abamectin at the right time."
      }
    }

def show_disease_info(predicted_class: str):
    """
    Hiển thị thông tin bệnh dựa trên class trả về từ API.
    predicted_class: chuỗi do API trả, ví dụ "lemon spider mite leaf"
    """
    info = load_disease_info()

    # Chuẩn hoá: chuyển dấu cách thành gạch dưới, và xuống thường
    key = predicted_class.strip().replace(" ", "_").lower()

    if key in info:
        data = info[key]
        name     = data.get("name",        "Chưa có tên bệnh")
        desc     = data.get("description", "Chưa có mô tả.")
        solution = data.get("solution",    "Chưa có giải pháp.")

        st.subheader(f"🔎 Disease name: {name}")
        st.write("**📝 Description:**", desc)
        st.write("**💡 Solution:**", solution)
    else:
        st.warning(
            f"No data was found in class **{predicted_class}** (key='{key}').\n"
            "Please check the class name or the JSON Data."
        )
