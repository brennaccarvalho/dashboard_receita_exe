import pandas as pd
import streamlit as st


def get_connection():
    import psycopg2

    cfg = st.secrets["redshift"]
    return psycopg2.connect(
        host=cfg["host"],
        port=cfg["port"],
        dbname=cfg["database"],
        user=cfg["user"],
        password=cfg["password"],
    )


@st.cache_data(ttl=3600, show_spinner=False)
def run_query(sql: str, params=None) -> pd.DataFrame:
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
        return pd.DataFrame(rows, columns=columns)
    except Exception as exc:
        st.warning(f"Redshift indisponível no momento: {exc}")
        return pd.DataFrame()
    finally:
        if conn is not None:
            conn.close()
