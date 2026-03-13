import streamlit as st
import pandas as pd
import plotly.express as px

from utils.session_state import SessionState
from utils.api_client import APIClient

st.title("Классификационный анализ")

client = APIClient()
client.set_token(SessionState.get_token())

tab_knn, tab_automl = st.tabs(["KNN классификация", "AutoML классификация"])


with tab_knn:

    st.subheader("KNN классификация")

    target_column = st.text_input("Целевая колонка", key="knn_target")
    feature_columns = st.text_input(
        "Фичи (через запятую)", key="knn_features"
    )

    k = st.slider("Количество соседей (k)", 1, 50, 5)
    test_size = st.slider("Размер тестовой выборки", 0.1, 0.5, 0.25)

    if st.button("Запустить KNN", key="btn_knn"):

        if not target_column or not feature_columns:
            st.warning("Заполните все поля")
            st.stop()

        features = [c.strip() for c in feature_columns.split(",")]

        try:

            res = client.knn_classification(
                target_column=target_column,
                feature_columns=features,
                k=k,
                test_size=test_size
            )

            st.success("KNN анализ выполнен")

            cols = st.columns(3)
            cols[0].metric("Accuracy", f"{res['accuracy']:.3f}")
            cols[1].metric("Train size", res["n_train"])
            cols[2].metric("Test size", res["n_test"])

            st.subheader("Confusion Matrix")

            cm = pd.DataFrame(
                res["confusion_matrix"],
                columns=res["class_names"],
                index=res["class_names"]
            )

            fig_cm = px.imshow(
                cm,
                text_auto=True,
                labels=dict(x="Predicted", y="Actual"),
                title="Confusion Matrix"
            )

            st.plotly_chart(fig_cm, use_container_width=True)

            st.subheader("Classification report")

            report_df = pd.DataFrame(res["classification_report"]).transpose()

            st.dataframe(report_df, use_container_width=True)

        except Exception as e:
            st.error(f"KNN error: {str(e)}")

with tab_automl:

    st.subheader("AutoML классификация")

    target_column = st.text_input("Целевая колонка", key="automl_target")
    feature_columns = st.text_input(
        "Фичи (через запятую)", key="automl_features"
    )

    test_size = st.slider("Test size", 0.1, 0.5, 0.25, key="automl_test")

    n_select = st.slider(
        "Сколько лучших моделей показать",
        3,
        15,
        5
    )

    if st.button("Запустить AutoML", key="btn_automl"):

        if not target_column or not feature_columns:
            st.warning("Заполните все поля")
            st.stop()

        features = [c.strip() for c in feature_columns.split(",")]

        try:

            res = client.automl_classification(
                target_column=target_column,
                feature_columns=features,
                test_size=test_size,
                n_select=n_select
            )

            st.success("AutoML анализ выполнен")

            cols = st.columns(3)
            cols[0].metric("Accuracy", f"{res['accuracy']:.3f}")
            cols[1].metric("Train size", res["n_train"])
            cols[2].metric("Test size", res["n_test"])

            st.subheader("Confusion Matrix")

            cm = pd.DataFrame(
                res["confusion_matrix"],
                columns=res["class_names"],
                index=res["class_names"]
            )

            fig_cm = px.imshow(
                cm,
                text_auto=True,
                labels=dict(x="Predicted", y="Actual"),
                title="Confusion Matrix"
            )

            st.plotly_chart(fig_cm, use_container_width=True)

            st.subheader("Classification report")

            report_df = pd.DataFrame(res["classification_report"]).transpose()

            st.dataframe(report_df, use_container_width=True)

            st.subheader("Leaderboard моделей")

            leaderboard = pd.DataFrame(res["leaderboard"])

            if not leaderboard.empty:
                st.dataframe(leaderboard, use_container_width=True)

                fig_lb = px.bar(
                    leaderboard,
                    x="learner",
                    y="best_loss",
                    title="Сравнение моделей (loss)",
                    text="best_loss"
                )

                st.plotly_chart(fig_lb, use_container_width=True)

            else:
                st.info("Нет данных leaderboard")

        except Exception as e:
            st.error(f"AutoML error: {str(e)}")