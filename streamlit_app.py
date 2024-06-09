import streamlit as st
import pandas as pd
from io import StringIO
import openpyxl

uploaded_file = st.file_uploader("Choose a file")
data = None
if uploaded_file is not None:

    # Can be used wherever a "file-like" object is accepted:
    data = pd.read_excel(uploaded_file)
    st.write(dataframe)

for target_object_type in ["здание", "нежилое помещение", "земельный участок"]:
  target_entries = data[data["Тип объекта"] == target_object_type]

  target_entries = target_entries[~target_entries["Начальная цена за квадратный метр"].isna()]

  fig = px.density_mapbox(
      target_entries,
      lat="Широта",
      lon="Долгота",
      z="Начальная цена за квадратный метр",
      radius=20,
      zoom=0,
      title=f"Тип объекта: {target_object_type}",
      color_continuous_scale = px.colors.sequential.Plasma,
      opacity=0.8,
      mapbox_style="open-street-map"
    )

  # fig = px.scatter_mapbox(
  #     target_entries, lat="Широта", lon="Долгота", color="Начальная цена за квадратный метр",
  #     hover_name="Начальная цена за квадратный метр",
  #     color_continuous_scale = px.colors.sequential.Viridis, opacity=0.5,
  #     title=target_object_type)

  fig.update_layout(mapbox_style="open-street-map")

  st.plotly_chart(fig)

  fig.show(renderer="colab")
