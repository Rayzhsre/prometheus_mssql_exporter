# prometheus_mssql_exporter
prometheus mssql exporter with Python client  

## Metrics

| Metric              | Note                        |
| ------------------- | --------------------------- |
| max_conn            | MSSQL max connection        |
| active_conn         | MSSQL active connections    |
| cache_hit           | MSSQL cache hit rate        |
| mssql_dead_lock     | Number of dead locks        |
| mssql_lock          | Number of  locks            |
| mssql_query_num     | Number of query             |
| mssql_process_total | Number of   processes       |
| mssql_process_wait  | Number of waiting processes |

## Other    

Display data with PromSQL. More data can be obtained by adding SQL.

