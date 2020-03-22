from prometheus_client import generate_latest, Gauge, CollectorRegistry
from metrics import PyMSSQL
from flask import Response, Flask



app = Flask(__name__)

@app.route("/")
def index():
    return 'prometheus mssql exporter'


@app.route("/metrics")
def mssqlResponse():
    # Type: Gauge
    max_conn.set(conn.mssql_max_conn())
    active_conn.set(conn.mssql_active_conn())
    cache_hit.set(conn.mssql_cache_hit())
    mssql_dead_lock.set(conn.mssql_dead_lock())
    mssql_lock.set(conn.mssql_lock())
    mssql_query_num.set(conn.mssql_query_num())
    mssql_process_total.set(conn.mssql_process_total())
    mssql_process_wait.set(conn.mssql_process_wait())

    return Response(generate_latest(REGISTRY), mimetype="text/plain")



if __name__ == '__main__':
    REGISTRY = CollectorRegistry(auto_describe=False)
    # MSSQL metrics
    conn = PyMSSQL(host='100.115.87.42', username='sa', port = 1433, password='123456')
    max_conn = Gauge('mssql_max_conn', 'mssql max connections', registry=REGISTRY)
    active_conn = Gauge('mssql_active_conn', 'mssql active connections', registry=REGISTRY)
    cache_hit = Gauge('mssql_cache_hit', 'mssql cache hit rate', registry=REGISTRY)
    mssql_dead_lock = Gauge('mssql_dead_lock', 'num of mssql dead lock', registry=REGISTRY)
    mssql_lock = Gauge('mssql_lock_total', 'num of mssql dead lock', registry=REGISTRY)
    mssql_query_num = Gauge('mssql_query_num', 'num of mssql query', registry=REGISTRY)
    mssql_process_total = Gauge('mssql_process_total', 'mssql process total', registry=REGISTRY)
    mssql_process_wait = Gauge('mssql_process_wait', 'mssql process waiting', registry=REGISTRY)
    
    app.run(host="0.0.0.0")