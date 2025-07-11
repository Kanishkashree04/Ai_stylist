import streamlit as st
import random
import numpy as np
from PIL import Image
import io

# --- Extractors (same as before) ---

def get_average_hex_color(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    img = img.resize((50, 50))
    arr = np.array(img)
    avg_color = arr.mean(axis=(0, 1))
    hex_color = '#%02x%02x%02x' % tuple(avg_color.astype(int))
    return hex_color

def extract_hair_eye_skin_colors(image_bytes):
    hex_color = get_average_hex_color(image_bytes)
    r, g, b = int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)
    brightness = (r + g + b) / 3
    if brightness < 80:
        hair_category = "Black"
        skin_category = "Dark"
    elif brightness < 150:
        hair_category = "Brown"
        skin_category = "Medium"
    else:
        hair_category = "Blonde"
        skin_category = "Fair"
    eye_category = "Brown"
    return hair_category, eye_category, skin_category, hex_color, hex_color, hex_color

def extract_vein_color_and_undertone(image_bytes):
    hex_color = get_average_hex_color(image_bytes)
    r, g, b = int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)
    if b > r and b > g:
        undertone = "Cool"
        vein_category = "Blue/Purple"
    elif g > r and g > b:
        undertone = "Warm"
        vein_category = "Greenish"
    else:
        undertone = "Neutral"
        vein_category = "Blue/Purple"
    return vein_category, undertone, hex_color

def extract_body_shape_and_proportion(image_bytes):
    shapes = ['Apple', 'Inverted Triangle', 'Trapezoid', 'Rectangle', 'Hourglass', 'Pear', 'Triangle']
    proportions = ['Balanced', 'Short Torso', 'Long Legs']
    shape = random.choice(shapes)
    proportion = random.choice(proportions)
    return shape, proportion

def predict_clothing(extracted_data):
    possible_dos = {
        'Fitted Blazer': '#2E86C1',
        'Dark Wash Jeans': '#1B2631',
        'V-Neck Tops': '#E74C3C',
        'Midi Skirts': '#F39C12',
        'Tailored Pants': '#27AE60'
    }
    possible_donts = {
        'Baggy Clothes': '#7F8C8D',
        'Neon Colors': '#39FF14',
        'Oversized Jackets': '#5D6D7E',
        'High-Low Hem': '#922B21',
        'Low Waist Jeans': '#4A235A'
    }
    do_preds = random.sample(list(possible_dos.items()), 3)
    do_names = [item for item, _ in do_preds]
    dont_preds = [item for item in possible_donts.keys() if item not in do_names][:3]
    dont_colors = [possible_donts[item] for item in dont_preds]
    return do_preds, list(zip(dont_preds, dont_colors))

# --- Page Config & Title ---
st.set_page_config(page_title="AI Personal Stylist", page_icon=":dress:", layout="centered")
st.markdown(
    "<h1 style='text-align: center; color: #6C3483;'>👗 AI Personal Stylist</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align: center; font-size:18px;'>Upload your images to receive personalized outfit recommendations.</p>",
    unsafe_allow_html=True,
)
st.markdown("---")

# --- Step Navigation State ---
if "step" not in st.session_state:
    st.session_state.step = 0  # Start at 0 for the welcome screen
if "extracted_data" not in st.session_state:
    st.session_state.extracted_data = {}

# --- Step 0: Get Started ---
if st.session_state.step == 0:
    st.markdown(
        """
        <div style='text-align:center; margin-top:40px;'>
            <span style='font-size:48px;'>👗</span>
            <h2 style='color:#6C3483;'>Welcome to AI Personal Stylist!</h2>
            <p style='font-size:20px; color:#444;'>
                Get personalized outfit recommendations.<br>
                Click the button below to get started!
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Get Started", key="get_started_btn"):
        st.session_state.step = 1
        st.experimental_rerun()

# --- Step 1: Passport Photo ---
elif st.session_state.step == 1:
    st.header("📷 Step 1: Upload Passport Photo")
    passport_img = st.file_uploader("Upload your face photo", type=['jpg', 'jpeg', 'png'], key="passport_step1_unique")
    if passport_img:
        hair_cat, eye_cat, skin_cat, hair_hex, eye_hex, skin_hex = extract_hair_eye_skin_colors(passport_img.read())
        st.session_state.extracted_data.update({
            'Hair Color': hair_cat,
            'Eye Color': eye_cat,
            'Skin Tone': skin_cat,
            'Hair Color Hex': hair_hex,
            'Eye Color Hex': eye_hex,
            'Skin Tone Hex': skin_hex
        })
        st.image(passport_img, width=320, caption="Passport Photo")
        st.success("Passport photo uploaded!")
        st.markdown(f"<span class='important-label'>Hair Color:</span> <span class='important-value'>{hair_cat} {hair_hex}</span>", unsafe_allow_html=True)
        st.markdown(f"<span class='important-label'>Eye Color:</span> <span class='important-value'>{eye_cat} {eye_hex}</span>", unsafe_allow_html=True)
        st.markdown(f"<span class='important-label'>Skin Tone:</span> <span class='important-value'>{skin_cat} {skin_hex}</span>", unsafe_allow_html=True)
        if st.button("Next ➡️"):
            st.session_state.step = 2
            st.experimental_rerun()

# --- Step 2: Vein Photo ---
elif st.session_state.step == 2:
    st.header("💪 Step 2: Upload Vein Photo")
    vein_img = st.file_uploader("Upload your wrist/vein photo", type=['jpg', 'jpeg', 'png'], key="vein_step2_unique")
    if vein_img:
        vein_cat, undertone, vein_hex = extract_vein_color_and_undertone(vein_img.read())
        st.session_state.extracted_data.update({
            'Vein Color': vein_cat,
            'Vein Undertone': undertone,
            'Vein Color Hex': vein_hex
        })
        st.image(vein_img, width=320, caption="Vein Photo")
        st.success("Vein photo uploaded!")
        st.markdown(f"<span class='important-label'>Vein Color:</span> <span class='important-value'>{vein_cat} {vein_hex}</span>", unsafe_allow_html=True)
        st.markdown(f"<span class='important-label'>Undertone:</span> <span class='important-value'>{undertone}</span>", unsafe_allow_html=True)
        if st.button("Next ➡️"):
            st.session_state.step = 3
            st.experimental_rerun()
    if st.button("⬅️ Back"):
        st.session_state.step = 1
        st.experimental_rerun()

# --- Step 3: Full Body Photo ---
elif st.session_state.step == 3:
    st.header("🧍 Step 3: Upload Full Body Photo")
    body_img = st.file_uploader("Upload a full body photo", type=['jpg', 'jpeg', 'png'], key="body_step3_unique")
    if body_img:
        shape, proportion = extract_body_shape_and_proportion(body_img.read())
        st.session_state.extracted_data.update({
            'Body Shape': shape,
            'Body Proportion': proportion
        })
        st.image(body_img, width=320, caption="Full Body Photo")
        st.success("Full body photo uploaded!")
        st.markdown(f"<span class='important-label'>Body Shape:</span> <span class='important-value'>{shape}</span>", unsafe_allow_html=True)
        st.markdown(f"<span class='important-label'>Body Proportion:</span> <span class='important-value'>{proportion}</span>", unsafe_allow_html=True)
        if st.button("Next ➡️"):
            st.session_state.step = 4
            st.experimental_rerun()
    if st.button("⬅️ Back"):
        st.session_state.step = 2
        st.experimental_rerun()

# --- Step 4: Recommendations ---
elif st.session_state.step == 4:
    st.header("✨ Get Recommendations")
    required_keys = [
        'Hair Color', 'Eye Color', 'Skin Tone',
        'Hair Color Hex', 'Eye Color Hex', 'Skin Tone Hex',
        'Vein Color', 'Vein Undertone', 'Vein Color Hex',
        'Body Shape', 'Body Proportion'
    ]
    extracted_data = st.session_state.extracted_data
    missing = [k for k in required_keys if k not in extracted_data]
    if missing:
        st.error(f"⚠️ Missing data: {', '.join(missing)}. Please upload all required images in previous steps.")
        if st.button("⬅️ Back"):
            st.session_state.step = 3
            st.experimental_rerun()
    else:
        # --- Only show recommendations, no extracted features preview ---
        if "stylist_predictions" not in st.session_state:
            do_preds, dont_preds = predict_clothing(extracted_data)
            st.session_state.stylist_predictions = (do_preds, dont_preds)
        do_preds, dont_preds = st.session_state.stylist_predictions

        st.markdown("<div class='section-title' style='color:#229954;'>✅ Recommended Do's</div>", unsafe_allow_html=True)
        for item, color in do_preds:
            st.markdown(f"<span class='important-label'>{item}:</span> <span class='important-value'>{color}</span>", unsafe_allow_html=True)

        st.markdown("<div class='section-title' style='color:#CB4335;'>❌ Recommended Don'ts</div>", unsafe_allow_html=True)
        for item, color in dont_preds:
            st.markdown(f"<span class='important-label'>{item}:</span> <span class='important-value'>{color}</span>", unsafe_allow_html=True)
        if st.button("⬅️ Back"):
            st.session_state.step = 3
            st.experimental_rerun()

# --- Custom CSS for a modern look and important fonts ---
st.markdown("""
    <style>
    .stButton>button {
        background-color: #6C3483;
        color: white;
        padding: 10px 24px;
        font-size: 18px;
        border-radius: 8px;
        margin-top: 10px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #229954;
        color: white;
    }
    .important-label {
        font-size: 22px !important;
        font-weight: bold !important;
        color: #6C3483 !important;
        margin-bottom: 2px;
    }
    .important-value {
        font-size: 20px !important;
        font-weight: bold !important;
        color: #229954 !important;
        margin-left: 8px;
    }
    .section-title {
        font-size: 28px !important;
        font-weight: bold !important;
        color: #2874A6 !important;
        margin-top: 18px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)