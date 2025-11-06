# train_model.py
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from joblib import dump
import os

DB = "hospital.db"
MODEL_FILE = "model.pkl"

def load_citas():
    conn = sqlite3.connect(DB)
    df = pd.read_sql_query("""
      SELECT fecha, hora
      FROM citas
    """, conn)
    conn.close()
   
    df['fecha'] = pd.to_datetime(df['fecha']).dt.date
    return df

def build_daily_counts(df):
  
    counts = df.groupby('fecha').size().rename('count').reset_index()
    counts['fecha'] = pd.to_datetime(counts['fecha'])
    return counts

def make_features(df):
    df = df.copy()
    df['dow'] = df['fecha'].dt.weekda
    df['day'] = df['fecha'].dt.day
    df['month'] = df['fecha'].dt.month
    
    df['count_lag1'] = df['count'].shift(1).fillna(method='bfill')
    df['count_lag7'] = df['count'].shift(7).fillna(method='bfill')
    return df

def train_and_save():
    df_raw = load_citas()
    counts = build_daily_counts(df_raw)


    date_range = pd.date_range(counts['fecha'].min(), counts['fecha'].max())
    counts = counts.set_index('fecha').reindex(date_range, fill_value=0).rename_axis('fecha').reset_index()
    counts['count'] = counts['count'].astype(int)

    df = make_features(counts)

    features = ['dow','day','month','count_lag1','count_lag7']
    X = df[features]
    y = df['count']

    if len(df) < 10:
        print("Pocos datos históricos — el modelo será muy aproximado (se recomienda más datos).")

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    score = model.score(X_test, y_test)
    print(f"Modelo entrenado. R^2 en test: {score:.3f}")

    dump(model, MODEL_FILE)
    print(f"Modelo guardado en {MODEL_FILE}")

if __name__ == "__main__":
    if not os.path.exists(DB):
        raise SystemExit("No encuentro hospital.db. Ejecuta init_db.py primero.")
    train_and_save()
