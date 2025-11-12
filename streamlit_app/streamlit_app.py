import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Biodiversity Predictor", page_icon="🌿", layout="centered")

@st.cache_resource
def load_model(path="biodiversity_model.pkl"):
    return joblib.load(path)

model = load_model()

# Gebruik exact de features waarmee je model is getraind
FEATURES = list(getattr(model, "feature_names_in_", ["HAB","SPP","CS","CP","CW"]))

st.title("🌿 Biodiversity (BD) Predictor")
st.caption("Voorspel BD op basis van ecosysteem- en servicescores.")

with st.form("predict"):
    cols = st.columns(len(FEATURES))
    values = {}
    for i, f in enumerate(FEATURES):
        values[f] = cols[i].slider(f, 0.0, 100.0, 50.0, 0.1)
    submitted = st.form_submit_button("Voorspel")

if submitted:
    X = pd.DataFrame([values], columns=FEATURES)
    pred = float(model.predict(X)[0])
    st.metric("Voorspelde BD", f"{pred:.2f}")

    # Optioneel: toon de input terug
    with st.expander("Invoer"):
        st.write(X)
