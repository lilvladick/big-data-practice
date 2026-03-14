from typing import List, Dict

import numpy as np
import pandas as pd
from flaml.automl import AutoML
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# наверное надо вынести, но пусть вот тут полежит
import json

def _convert_numpy(obj):
    try:
        if isinstance(obj, dict):
            return {k: _convert_numpy(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple, set)):
            return [_convert_numpy(i) for i in obj]
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, (np.integer, np.int64, np.int32)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64, np.float32)):
            return float(obj)
        elif isinstance(obj, np.bool_):
            return bool(obj)
        elif pd.isna(obj):
            return None
        json.dumps(obj)
        return obj
    except (TypeError, ValueError):
        return str(obj)

class AutoMLDataAnalysisService:
    @staticmethod
    def flaml_automl(df: pd.DataFrame, feature_columns: List[str], target_column: str,
                       test_size: float = 0.25, time_budget: int = 300,
                       n_select: int = 5, metric: str = 'accuracy') -> Dict:
        required_cols = feature_columns + [target_column]
        missing = [c for c in required_cols if c not in df.columns]
        if missing:
            raise ValueError(f"Отсутствуют колонки: {', '.join(missing)}")

        sub_df = df[required_cols].dropna().copy()
        if len(sub_df) < 50:
            raise ValueError(f"Слишком мало данных для AutoML: {len(sub_df)} строк")

        if sub_df[target_column].nunique() < 2:
            raise ValueError(f"Целевая переменная '{target_column}' имеет меньше 2 классов")

        X = sub_df[feature_columns]
        y_raw = sub_df[target_column]

        if not np.issubdtype(y_raw.dtype, np.number):
            le = LabelEncoder()
            y = le.fit_transform(y_raw)
            class_names = le.classes_.tolist()
        else:
            y = y_raw.values.astype(int)
            class_names = np.unique(y).tolist()

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )

        automl = AutoML()
        automl.fit(
            X_train, y_train,
            task="classification",
            metric=metric,
            time_budget=time_budget,
            n_jobs=-1
        )

        y_pred = automl.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
        cm = confusion_matrix(y_test, y_pred).tolist()

        try:
            configs = automl.best_config_per_estimator or {}
            losses = automl.best_loss_per_estimator or {}
            rows = []
            for learner_name, cfg in configs.items():
                rows.append({
                    'learner': learner_name,
                    'best_loss': float(losses.get(learner_name, np.nan)),
                    'best_config': _convert_numpy(cfg),
                })
            lb_df = pd.DataFrame(rows)
            if not lb_df.empty:
                lb_df = lb_df.sort_values('best_loss', ascending=True).reset_index(drop=True)
                lb_df['best_config_train_time'] = np.nan
                try:
                    best_learner = automl.best_estimator
                    if best_learner in lb_df['learner'].values:
                        lb_df.loc[lb_df['learner'] == best_learner, 'best_config_train_time'] = float(automl.best_config_train_time or np.nan)
                except Exception:
                    pass
            else:
                lb_df = pd.DataFrame(columns=['learner', 'best_loss', 'best_config', 'best_config_train_time'])

            leaderboard_df = lb_df.head(n_select).copy()
            leaderboard = leaderboard_df.to_dict('records')
        except Exception as e:
            leaderboard = [{
                'learner': automl.best_estimator,
                'best_loss': float(getattr(automl, 'best_loss', np.nan)),
                'best_config': _convert_numpy(getattr(automl, 'best_config', {})),
                'best_config_train_time': float(getattr(automl, 'best_config_train_time', np.nan))
            }]

        result = {
            "accuracy": float(acc),
            "classification_report": _convert_numpy(report),
            "confusion_matrix": cm,
            "n_train": int(len(X_train)),
            "n_test": int(len(X_test)),
            "best_estimator_name": str(automl.best_estimator),
            "target_column": target_column,
            "feature_columns": feature_columns,
            "class_names": [str(c) for c in class_names],
            "leaderboard": _convert_numpy(leaderboard),
            "top_models_info": [
                f"{row['learner']}: best_loss={float(row.get('best_loss', 0.0)):.4f}, time={float(row.get('best_config_train_time', 0.0)):.1f}s"
                for row in leaderboard
            ],
            "best_config": _convert_numpy(automl.best_config),
            "optimize_metric": metric,
            "time_budget": time_budget
        }

        return result