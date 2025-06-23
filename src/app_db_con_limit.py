"""DB access and connection limit."""

# ruff: noqa: D103
import time
import warnings

import pandas as pd
import psycopg2  # pip install psycopg2-binary or psycopg2
import psycopg2.extras
import psycopg2.pool
import streamlit as st
from streamlit.logger import get_logger

logger = get_logger("app")
logger.info("Start")


@st.cache_resource
def _get_connection_pool() -> psycopg2.pool.SimpleConnectionPool:
    dns = st.secrets["DB_DNS"]  # read from .streamlit/secrets.toml
    # db_dns = os.environ["DB_DNS"]  #  read from env (better for deployment)

    # simple, using dns
    # return psycopg2.pool.SimpleConnectionPool(dsn=db_dns, minconn=1, maxconn=1)

    # fix for Azure DBs requiring username@hostname as username
    from urllib.parse import urlparse

    p = urlparse(dns)
    return psycopg2.pool.SimpleConnectionPool(
        dbname=p.path[1:],
        user=p.username,
        password=p.password,
        host=p.hostname,
        port=p.port,
        minconn=1,
        maxconn=1,
    )


# no cache here, to prevent duplicated cache
def _db_query(  # noqa: C901, PLR0915
    sql: str, params: tuple[str | int, ...], mode: str
) -> pd.DataFrame | list | dict:
    """Perform DB query, no caching to prevent duplicated cache."""
    if mode not in {"df", "1row", "1col", "list"}:
        msg = f"Invalid mode: {mode}"
        raise ValueError(msg)

    res = pd.DataFrame()

    try:
        pool = _get_connection_pool()
    except psycopg2.pool.PoolError:
        msg = "Error fetching connection pool"
        logger.exception(msg)
        st.error(msg)
        st.stop()
        return pd.DataFrame()

    retry_delay = 1
    while True:  # endless loop to get a free DB connection
        try:
            con = pool.getconn()
            break
        except psycopg2.pool.PoolError:
            msg = "DB connection pool exhausted, retrying"
            logger.warning(msg)
            time.sleep(retry_delay)
            # increase waiting time with each retry up to 15 seconds
            retry_delay = min(retry_delay + 1, 15)

    try:
        if mode == "df":
            # suppress: UserWarning: pandas only support SQLAlchemy
            warnings.simplefilter(action="ignore", category=UserWarning)
            res = pd.read_sql_query(sql=sql, con=con, params=params)
            # df = sqlio.read_sql_query(sql=sql, con=.get_connection(), params=params)  # noqa: E501
            warnings.simplefilter("always")  # Reset warnings
            assert isinstance(res, pd.DataFrame), type(res)

        else:
            cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute(sql, params)
            if mode == "1row":
                res = cur.fetchone()
                res = dict(res) if res else {}
                assert isinstance(res, dict), type(res)
            elif mode == "1col":
                res = cur.fetchall()
                assert isinstance(res, list), type(res)
                res = [r[0] for r in res] if res else []
            elif mode == "list":
                res = cur.fetchall()
                assert isinstance(res, list), type(res)
                res = [dict(r) for r in res] if res else []
            cur.close()

    except psycopg2.Error as e:
        msg = f"Error executing query: {e}"
        logger.exception(msg)
        st.error(msg)
        st.stop()
        return pd.DataFrame()  # only to make editor happy
    finally:
        if con:
            pool.putconn(con)
    return res


@st.cache_data(ttl="1d")
def db_get_data_df(
    plant_id: int,
) -> pd.DataFrame:
    sql = "SELECT * from my_table where id = %s"
    res = _db_query(sql, (plant_id,), mode="df")
    assert isinstance(res, pd.DataFrame), type(res)
    return res


@st.cache_data(ttl="1d")
def db_get_data_dict(
    plant_id: int,
) -> dict:
    sql = "SELECT * from my_table where id = %s"
    res = _db_query(sql, (plant_id,), mode="1row")
    assert isinstance(res, dict), type(res)
    return res


@st.cache_data(ttl="1d")
def db_get_data_col() -> list:
    sql = "SELECT name from my_table"
    res = _db_query(sql, (), mode="1col")
    assert isinstance(res, list), type(res)
    return sorted(res)


@st.cache_data(ttl="1d")
def db_get_data_list() -> list[dict]:
    sql = "SELECT id, name from my_table"
    res = _db_query(sql, (), mode="list")
    assert isinstance(res, list), type(res)
    return res


st.title("Home")

df = db_get_data_df(61)
st.dataframe(data=df, hide_index=True)

d = db_get_data_dict(61)
st.write(d)

col = db_get_data_col()
st.write(col)

lst = db_get_data_list()
st.write(lst)

logger.info("End")
