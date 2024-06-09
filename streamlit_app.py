import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

arr = np.random.normal(1, 1, size=100)
fig, ax = plt.subplots()
ax.hist(arr, bins=20)

st.pyplot(fig)
# import streamlit as st
# import pandas as pd
# from io import StringIO
# import openpyxl
# import plotly.express as px
# import matplotlib.pyplot as plt

# # Константы
# MAPBOX_TOKEN = "pk.eyJ1IjoibmJhcnlraW4iLCJhIjoiY2xzc3R2c2ZvMHlweDJscWkxcWc3bG1taiJ9.mO3_ujVU5ZxAOJJrwp_v4w"
# px.set_mapbox_access_token(MAPBOX_TOKEN)

# data = pd.read_excel("агрегированные_сделки.xlsx")

# # Карта
# for target_object_type in ["здание", "нежилое помещение", "земельный участок"]:
#     target_entries = data[data["Тип объекта"] == target_object_type]

#     target_entries = target_entries[~target_entries["Начальная цена за квадратный метр"].isna()]

#     fig = px.density_mapbox(
#       target_entries,
#       lat="Широта",
#       lon="Долгота",
#       z="Начальная цена за квадратный метр",
#       center=dict(lat=59.95, lon=30.4), 
#       zoom=9,
#       radius=20,
#       title=f"Тип объекта: {target_object_type}",
#       color_continuous_scale = px.colors.sequential.Plasma,
#       opacity=0.8,
#       mapbox_style="open-street-map"
#     )
    
#     st.plotly_chart(fig, use_container_width=True)
#     fig.update_layout(mapbox_style="open-street-map")

# # Относительный рост
# MONTH_NAMES = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]

# data["Относительный рост цены"] = data["Итоговая цена"] / data['Начальная цена']
# target = data[~(data["Относительный рост цены"].isna() | data["Дата сделки"].isna())]
# target["Месяц сделки"] = target["Дата сделки"].dt.month

# groupped = target[["Месяц сделки", "Относительный рост цены"]].groupby("Месяц сделки").mean()
# groupped.sort_index(inplace=True)

# plt.figure(figsize=(14, 6))

# month_number_to_name = lambda number: MONTH_NAMES[number - 1]

# plt.bar(list(map(month_number_to_name, groupped.index)),
#         groupped["Относительный рост цены"], color="red", label=f"Кол-во сделок: {len(target)}")

# plt.legend()

# plt.title("Средний рост цены с начала торгов")

# st.pyplot()
