import streamlit as st
import pandas as pd
import plotly.express as px
from utils.session_state import SessionState
from utils.api_client import APIClient

st.title("Анализ данных")

client = APIClient()
client.set_token(SessionState.get_token())

tab_uni, tab_cat = st.tabs(["Унивариантный анализ", "Категориальный анализ"])

with tab_uni:
    st.subheader("Унивариантный анализ числовой переменной")

    col_name = st.text_input("Название числовой колонки", key="uni_col_name")

    if st.button("Выполнить анализ", key="btn_uni"):
        if not col_name.strip():
            st.warning("Введите название колонки")
            st.stop()

        try:
            res = client.get_univariate_analysis(col_name.strip())

            desc = res.get("describe", {})
            st.subheader("Основные статистики")
            cols = st.columns([1, 1, 1, 1, 1, 1])
            cols[0].metric("Количество", int(desc.get("count", 0)))
            cols[1].metric("Среднее", f"{desc.get('mean', '—'):.3g}" if desc.get("mean") is not None else "—")
            cols[2].metric("Медиана", f"{desc.get('50%', '—'):.3g}" if desc.get("50%") is not None else "—")
            cols[3].metric("Минимум", f"{desc.get('min', '—'):.3g}" if desc.get("min") is not None else "—")
            cols[4].metric("Максимум", f"{desc.get('max', '—'):.3g}" if desc.get("max") is not None else "—")
            cols[5].metric("Стд. отклонение", f"{desc.get('std', '—'):.3g}" if desc.get("std") is not None else "—")

            extra_cols = st.columns(3)
            extra_cols[0].metric("Пропуски", res.get("missing", 0))
            extra_cols[1].metric("Уникальных", res.get("unique", 0))
            extra_cols[2].metric("Мода", ", ".join(map(str, res.get("mode", []))) or "—")
            if "histogram_bins" in res and res["histogram_bins"]:
                hist_data = res["histogram_bins"]
                try:
                    bins = list(hist_data.keys())
                    counts = list(hist_data.values())
                    fig_hist = px.bar(
                        x=bins,
                        y=counts,
                        labels={"x": col_name, "y": "Количество наблюдений"},
                        title="Гистограмма распределения"
                    )
                    fig_hist.update_layout(xaxis_tickangle=-45)
                    st.plotly_chart(fig_hist, use_container_width=True)
                except Exception as e:
                    st.info("Не удалось построить гистограмму (нестандартный формат интервалов)", e)

            st.caption("Данные получены из бэкенда • пропуски исключены при расчёте гистограммы")

        except Exception as e:
            st.error(f"Ошибка при анализе: {str(e)}")

with tab_cat:
    st.subheader("Анализ категориальной / номинальной переменной")

    col_name = st.text_input("Название категориальной колонки", key="cat_col_name")

    top_n = st.slider("Показывать топ-N категорий в таблице и графике", 5, 30, 10, step=5)

    if st.button("Выполнить анализ", key="btn_cat"):
        if not col_name.strip():
            st.warning("Введите название колонки")
            st.stop()

        try:
            res = client.get_categorical_analysis(col_name.strip())

            vc = res.get("value_counts", {})
            if not vc:
                st.info("Нет данных по категориям")
                st.stop()

            missing = res.get("missing", 0)
            unique  = res.get("unique", 0)

            cols = st.columns(3)
            cols[0].metric("Уникальных значений", unique)
            cols[1].metric("Пропущенных значений", missing)
            cols[2].metric("Заполненных наблюдений", sum(vc.values()))

            if len(vc) > top_n:
                top_vc = dict(sorted(vc.items(), key=lambda x: x[1], reverse=True)[:top_n])
                other_sum = sum(vc.values()) - sum(top_vc.values())
                top_vc["Остальные"] = other_sum
            else:
                top_vc = vc.copy()

            fig_pie = px.pie(
                values=list(top_vc.values()),
                names=list(top_vc.keys()),
                title=f"Распределение (топ-{len(top_vc)} категорий)",
                hole=0.35
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)

            df_bar = pd.DataFrame({
                "Категория": list(vc.keys()),
                "Количество": list(vc.values())
            }).sort_values("Количество", ascending=False).head(20)

            fig_bar = px.bar(
                df_bar,
                x="Количество",
                y="Категория",
                orientation="h",
                title="Топ-20 категорий по частоте",
                text="Количество",
                color="Количество",
                color_continuous_scale="Blues"
            )
            fig_bar.update_traces(textposition="auto")
            fig_bar.update_layout(yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig_bar, use_container_width=True)

            df_table = pd.DataFrame({
                "Категория": list(vc.keys()),
                "Количество": list(vc.values()),
                "%": [f"{v/sum(vc.values())*100:.1f}%" for v in vc.values()]
            }).sort_values("Количество", ascending=False)

            st.subheader("Таблица распределения")
            st.dataframe(
                df_table.head(30).style.format({"Количество": "{:,}", "%": "{}"}),
                use_container_width=True,
                hide_index=True
            )

            if len(vc) > 30:
                st.caption(f"... и ещё {len(vc)-30} категорий с малой частотой")

        except Exception as e:
            st.error(f"Ошибка анализа: {str(e)}")