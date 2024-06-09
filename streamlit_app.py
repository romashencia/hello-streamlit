import streamlit as st
import pandas as pd
from io import StringIO
import openpyxl
import plotly.express as px
import matplotlib.pyplot as plt
import warnings
import numpy as np
import seaborn as sns

warnings.filterwarnings('ignore')

# Константы
MAPBOX_TOKEN = "pk.eyJ1IjoibmJhcnlraW4iLCJhIjoiY2xzc3R2c2ZvMHlweDJscWkxcWc3bG1taiJ9.mO3_ujVU5ZxAOJJrwp_v4w"
px.set_mapbox_access_token(MAPBOX_TOKEN)

data = pd.read_excel("агрегированные_сделки.xlsx")

# Карта

target_object_type = st.radio("Зависимость цены от расположения для типа", ["здание", "нежилое помещение", "земельный участок"])
if target_object_type is not None:
    target_entries = data[data["Тип объекта"] == target_object_type]

    target_entries = target_entries[~target_entries["Начальная цена за квадратный метр"].isna()]

    fig = px.density_mapbox(
      target_entries,
      lat="Широта",
      lon="Долгота",
      z="Начальная цена за квадратный метр",
      center=dict(lat=59.95, lon=30.4), 
      zoom=9,
      radius=20,
      title=f"Тип объекта: {target_object_type}",
      color_continuous_scale = px.colors.sequential.Plasma,
      opacity=0.8,
      mapbox_style="open-street-map"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    fig.update_layout(mapbox_style="open-street-map")

# Относительный рост
MONTH_NAMES = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]

data["Относительный рост цены"] = data["Итоговая цена"] / data['Начальная цена']
target = data[~(data["Относительный рост цены"].isna() | data["Дата сделки"].isna())]
target["Месяц сделки"] = target["Дата сделки"].dt.month

groupped = target[["Месяц сделки", "Относительный рост цены"]].groupby("Месяц сделки").mean()
groupped.sort_index(inplace=True)

plt.figure(figsize=(14, 6))

month_number_to_name = lambda number: MONTH_NAMES[number - 1]

plt.bar(list(map(month_number_to_name, groupped.index)),
        groupped["Относительный рост цены"], color="red", label=f"Кол-во сделок: {len(target)}")

plt.legend()

st.pyplot(plt.gcf())


# Цена от площади

fig, ax = plt.subplots(2, figsize=(12, 10))

for in_cad in [False, True]:
  target_entries = data[data["Внутри КАДа"] == in_cad]

  ax[int(in_cad)].scatter(target_entries["Площадь, м2"], target_entries["Начальная цена"], alpha=0.3)

  # Линейная аппроксимация цены от площади
  linear_approximation = np.polyfit(target_entries["Площадь, м2"], target_entries["Начальная цена"], deg=1)

  approx_xs = np.arange(0, 12000, 1000)
  approx_ys = approx_xs * linear_approximation[0] + linear_approximation[1]

  ax[int(in_cad)].plot(
      approx_xs,
      approx_ys,
      color="orange",
      label=f"{round(linear_approximation[0]):,}x + {round(linear_approximation[1]):,}"
  )

  ax[int(in_cad)].set_title("Внутри КАДа" if in_cad
                            else "За КАДом")

  ax[int(in_cad)].set_xlabel("Площадь, м2")
  ax[int(in_cad)].set_ylabel("Цена в рублях")

  ax[int(in_cad)].legend()

plt.title("Средний рост цены с начала торгов")

st.pyplot(plt.gcf())

# Цена от ВРИ

fig, axs = plt.subplots(1, 2, figsize=(20, 10), sharey=True)

in_cad = st.radio("Зависимость цены от площади для объектов:", ["внутри КАДа", "за КАДом"])
if in_cad is not None:
  in_cad = in_cad == "внутри КАДа"
  ax = axs[int(in_cad)]

  target_entries = data[data["Внутри КАДа"] == in_cad][["ВРИ", "Начальная цена за квадратный метр"]]

  mean_prices = target_entries.groupby('ВРИ').mean().reset_index()
  mean_prices.columns = ['ВРИ', 'Средняя цена']

  # Сокращаем названия, чтобы помещались
  def truncate_labels(label, max_length=50):
      if len(label) > max_length:
          return label[:max_length] + '...'
      return label

  mean_prices['ВРИ'] = mean_prices['ВРИ'].apply(lambda x: truncate_labels(x))

  sns.barplot(x='ВРИ', y='Средняя цена', data=mean_prices, palette='viridis', ax=ax)

  ax.set_ylabel('Средняя цена за квадратный метр')
  ax.set_title("Внутри КАДа" if in_cad
                            else "За КАДом")

  ax.set_xticklabels(mean_prices["ВРИ"], rotation=45, ha="right")

plt.tight_layout()
st.pyplot(plt.gcf())

s = st.radio('Pick one:', ['nose','ear'])
st.write(f"Hello, {s}")
