## Код для Grafana-панелей

**SQL-запросы будут работать только если таблицы были созданы командами из этого репозитория в противном случае - правьте имена столбцов и таблиц.**

### Панель General info
#### Block C

```
SELECT  
    count(job_name) AS 'Jobs failed'
FROM jobs_results
WHERE id IN (
    SELECT MAX(id)
    FROM jobs_results
    WHERE pipeline_id = (SELECT MAX(pipeline_id) FROM jobs_results WHERE branch_name = 'master') AND job_status = 'FAIL'
    GROUP BY job_name
);
```

#### Block D

```
SELECT  
    count(pipeline_id) AS 'Tests passed' 
FROM results
WHERE id IN (
    SELECT MAX(id)
    FROM results
    WHERE pipeline_id = (SELECT MAX(pipeline_id) FROM results WHERE branch_name = 'master') AND test_status = 'PASS'
    GROUP BY test_name
);
```

#### Block A

```
SELECT  
    count(job_name) AS 'Jobs passed'
FROM jobs_results
WHERE id IN (
    SELECT MAX(id)
    FROM jobs_results
    WHERE pipeline_id = (SELECT MAX(pipeline_id) FROM jobs_results WHERE branch_name = 'master') AND job_status = 'PASS'
    GROUP BY job_name
);
```

#### Block B

```
SELECT  
    count(job_name) AS 'Jobs reruned'
FROM jobs_results
WHERE id IN (
    SELECT MAX(id)
    FROM jobs_results
    WHERE pipeline_id = (SELECT MAX(pipeline_id) FROM jobs_results WHERE branch_name = 'master') AND job_status = 'RERUNED'
    GROUP BY job_name
);
```

#### Block E
```
SELECT  
    count(test_name) AS 'Tests failed'
FROM results
WHERE id IN (
    SELECT MAX(id)
    FROM results
    WHERE pipeline_id = (SELECT MAX(pipeline_id) FROM results WHERE branch_name = 'master') AND test_status = 'FAIL'
    GROUP BY test_name
);
```

#### Block F
```
SELECT
    pipeline_id as 'Pipeline ID'
FROM results
WHERE pipeline_id = (SELECT MAX(pipeline_id) FROM results WHERE branch_name = 'master');
```

### Диаграмма Passed to failed jobs

#### Block A

```
SELECT  
    now() as 'time_sec', count(pipeline_id) AS 'Jobs passed'
FROM jobs_results
WHERE id IN (
    SELECT MAX(id)
    FROM jobs_results
    WHERE pipeline_id = (SELECT MAX(pipeline_id) FROM jobs_results WHERE branch_name = 'master') AND job_status = 'PASS'
    GROUP BY job_name
);
```

### Block C

```
SELECT  
    now() as 'time_sec', count(pipeline_id) AS 'Jobs failed'
FROM jobs_results
WHERE id IN (
    SELECT MAX(id)
    FROM jobs_results
    WHERE pipeline_id = (SELECT MAX(pipeline_id) FROM jobs_results WHERE branch_name = 'master') AND job_status = 'FAIL'
    GROUP BY job_name
);
```

### Block B

```
SELECT  
    now() as 'time_sec', count(pipeline_id) AS 'Jobs reruned'
FROM jobs_results
WHERE id IN (
    SELECT MAX(id)
    FROM jobs_results
    WHERE pipeline_id = (SELECT MAX(pipeline_id) FROM jobs_results WHERE branch_name = 'master') AND job_status = 'RERUNED'
    GROUP BY job_name
);
```
