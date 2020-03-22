# -*- coding: utf-8 -*-

"""
 Collection of metrics and associated SQL requests
 Created by Rayzh
"""

import pyodbc


class PyMSSQL:
    def __init__(self, host, port, username, password, dbname='master', charset='utf8'):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.dbname = dbname
        self.charset = charset

    def connect(self):
        driver = '{ODBC Driver 17 for SQL Server}'
        conn_info = 'DRIVER=%s;SERVER=%s;PORT=%d;DATABASE=%s;UID=%s;PWD=%s' % (driver,self.host, self.port, self.dbname, self.username, self.password )
        self.conn = pyodbc.connect(conn_info, charset=self.charset)
        cur = self.conn.cursor()
        if not cur:
            raise(NameError,'connect database failed')
        else:
            return cur

    def query(self, sql):
        cur = self.connect()
        cur.execute(sql)
        res = cur.fetchall()

        self.conn.close()
        return res

    # max connections
    def mssql_max_conn(self):
        max_conn_row = self.query("select @@MAX_CONNECTIONS")
        for item in max_conn_row:
            max_conn = item[0]

        return max_conn

    # mssql active connections
    def mssql_active_conn(self):
        active_conn_row = self.query("SELECT COUNT(*) FROM sys.dm_exec_connections")
        for item in active_conn_row:
            active_conn = item[0]

        return active_conn

    # mssql cache hit
    def mssql_cache_hit(self):
        sql = "SELECT (a.cntr_value * 1.0 / b.cntr_value) * 100.0 [BufferCacheHitRatio] FROM (SELECT * FROM sys.dm_os_performance_counters \
                WHERE counter_name = 'Buffer cache hit ratio' AND object_name = CASE WHEN @@SERVICENAME = 'MSSQLSERVER' \
                THEN 'SQLServer:Buffer Manager' ELSE 'MSSQL$' + rtrim(@@SERVICENAME) + ':Buffer Manager' END ) a \
                CROSS JOIN (SELECT * from sys.dm_os_performance_counters WHERE counter_name = 'Buffer cache hit ratio base' \
                and object_name = CASE WHEN @@SERVICENAME = 'MSSQLSERVER' THEN 'SQLServer:Buffer Manager' \
                ELSE 'MSSQL$' + rtrim(@@SERVICENAME) + ':Buffer Manager' END ) b;"
        cache_hit_row = self.query(sql)
        for item in cache_hit_row:
            cache_hit = round(item[0],2)
        
        return cache_hit

    # num of dead lock
    def mssql_dead_lock(self):
        dead_lock_row = self.query("select cntr_value FROM sys.dm_os_performance_counters WHERE counter_name like 'Number of Deadlock%' and instance_name = '_Total'")
        for item in dead_lock_row:
            dead_lock = item[0]

        return dead_lock

    # num of lock
    def mssql_lock(self):
        lock_row = self.query("select count(*) from sys.dm_tran_locks")
        for item in lock_row:
            lock = item[0]

        return lock

    # num of current query
    def mssql_query_num(self):
        query_num_row = self.query("select cntr_value from sys.dm_os_performance_counters where counter_name='Batch Requests/sec'")
        for item in query_num_row:
            query_num = item[0]

        return query_num

    # num of total process
    def mssql_process_total(self):
        process_total_row = self.query("select COUNT(*) from master.dbo.sysprocesses")
        for item in process_total_row:
            process_total = item[0]

        return process_total

    # num of waiting process
    def mssql_process_wait(self):
        process_wait_row = self.query("select COUNT(*) from master.dbo.sysprocesses where status in ('runnable','suspended')")
        for item in process_wait_row:
            process_wait = item[0]

        return process_wait