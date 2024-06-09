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

# Введение

st.header("Гипотезы и поставленные вопросы")

st.markdown(r"""
1) Гипотеза о том, что разница между начальной ценой 
и конечной у объектов недвижимости выше в летний период

2) Гипотеза о том, что цена на объекты внутри КАДа 
с ростом общей площади растет быстрее, чем на объекты за КАДом

3) Какой ВРИ(вид разрешенного использования) самый 
ценный среди объектов внутри КАДа и за ним?""")

# Карта

st.header("Цена квадратного метра на карте")

target_object_type = st.radio("Тип объекта:", ["здание", "нежилое помещение", "земельный участок"])
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
      radius=10,
      color_continuous_scale = px.colors.sequential.Plasma,
      opacity=0.8,
      mapbox_style="open-street-map"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    fig.update_layout(mapbox_style="open-street-map")

# Относительный рост

st.header("Относительный рост цены с начала торгов")

st.markdown(r"""Я хочу внимательнее посмотреть на таблицы с ГИС торги. 
В основном объекты продаются с помощью электронных аукционов. 
В таблице есть начальная цена и итоговая. Разницу между ними назовем дельта. 
Есть гипотеза, что эта дельта в весенне-летний период выше, чем в остальное время, 
что может быть связано с "игрой гормонов" у покупателей и инвесторов,
чья любовь к риску увеличивается в это время года. 
Давайте проверим это. Будем смотреть на относительные дельты""")

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

st.markdown(r"""Результаты подтверждают мою гипотезу. 
Внушительный рост дельт наблюдается в июне и июле. 
То есть, в это время года инвесторы более склонны соревноваться, 
предлагать более высокую стоимость недвижимости. 
Это также подтверждается статьями, в которых исследуется 
увеличение тяги к риску в определенное время [года](https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=4b81bd6fd3c9acede621ca4db26af2e71b0b7ffa), 
связь риска с [погодой](https://www.sciencedirect.com/science/article/pii/S0929119920302054). 
Это достаточно ценный вывод, который может помочь 
продавцам недвижимости поднять цену на объект. 
Для этого можно просто начинать аукцион летом!""")


# Цена от площади

st.header("Зависимость цены от площади")

st.markdown(r"""Теперь посмотрим на зависимость 
цены на объект от его площади. 
Я делаю предположение, что для объектов
внутри КАДа она растет быстрее с ростом площади.""")

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

st.pyplot(plt.gcf())

st.markdown(r"""Так и получилось. На объекты внутри КАДа цена растет быстрее, 
чем на объекты за КАДом. Это логично, если исходить из общих 
представлений о территориальном размещении объектов коммерческой 
недвижимости(в городе больше людей, лучше развита инфраструктура,
значит больше прибыли будет получено с объекта, 
находящегося внутри города, 
значит он имеет большую ценность для инвесторов).""")

# Цена от ВРИ

st.header("Зависимость цены от ВРИ")

st.markdown(r"""ВРИ - вид разрешенного использования участка. 
От него зависит, что может быть построено на участке, 
какая у него кадастровая стоимость, 
ставка налога и прочее. Например, помещения, 
на которых можно открыть склад, дешевле, чем помещения 
под офисы. Подробнее про ВРИ можно прочитать
[здесь](https://zakon.ru/blog/2022/11/29/neochevidnye_posledstviya_izmeneniya_razreshyonnogo_ispolzovaniya_uchastka#:~:text=%D0%9A%D0%B0%D0%B4%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B2%D0%B0%D1%8F%20%D1%81%D1%82%D0%BE%D0%B8%D0%BC%D0%BE%D1%81%D1%82%D1%8C%20%D1%83%D1%87%D0%B0%D1%81%D1%82%D0%BA%D0%B0%20%D0%B2%20%D0%B7%D0%B0%D0%B2%D0%B8%D1%81%D0%B8%D0%BC%D0%BE%D1%81%D1%82%D0%B8,%D0%BA%20%D1%80%D0%B0%D0%B7%D0%BD%D1%8B%D0%BC%20%D0%B3%D1%80%D1%83%D0%BF%D0%BF%D0%B0%D0%BC%20%D0%B8%D0%BB%D0%B8%20%D0%BF%D0%BE%D0%B4%D0%B3%D1%80%D1%83%D0%BF%D0%BF%D0%B0%D0%BC)""")

fig, axs = plt.subplots(1, 2, figsize=(20, 10), sharey=True)

for in_cad in [False, True]:
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

st.markdown(r"""Для объектов за КАДом самая дорогая недвижимость имеет ВРИ 
"Специальная деятельность": размещение, хранение, захоронение, 
утилизация, накопление, обработка, обезвреживание отходов 
производства и потребления, медицинских отходов, 
биологических отходов, радиоактивных отходов, веществ, 
разрушающих озоновый слой, а также размещение объектов 
размещения отходов, захоронения, хранения, обезвреживания 
таких отходов (скотомогильников, мусоросжигательных 
и мусороперерабатывающих заводов, полигонов 
по захоронению и сортировке бытового мусора и 
отходов, мест сбора вещей для их вторичной переработки)

Это можно объяснить высокими требованиями к 
безопасности и технологии, ограниченным 
количеством таких объектов, административными
барьерами и экономической и экологической выгодой участка.

Внутри КАДа - ВРИ "Стоянка транспортных средств". 
Это также можно объяснить близким расположением
к главным транспортным узлам и трассам, доходностью от
логистических компаний, экономией на затратах
и высоким спросом на стоянки внутри города.""")

st.header("Выводы")

st.markdown(r"""Отвечаю на поставленные вопросы и комментирую выдвинутые гипотезы

1) Дельты между начальной и конечной ценой(для объектов, выставляемых на аукцион) 
действительно выше в июне и июле. это связано с тем, что любовь 
к риску у инвесторов зависит от настроения, погоды, 
времени года(на самом деле, даже от времени суток, но это не вошло в мое исследование)

2) С ростом общей площади цена на объекты внутри 
КАДа растет быстрее, чем цена на объекты за КАДом.

3) Самый "дорогой" ВРИ у объектов внутри КАДа - стоянка 
транспортных средств. У объектов за КАДом - специальная деятельность.""")

