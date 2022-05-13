## Код для Grafana-панелей

**SQL-запросы будут работать только если таблицы были созданы командами из этого репозитория в противном случае - правьте имена столбцов и таблиц.**

### Gauge `Pipeline success rate`
#### Block A

Здесь `SELECT COUNT(pipeline_id)/70*100` стоит 70 т.к. у нас это среднее кол-во pipelin'ов за неделю. **Подставьте своё число** 

```
SELECT COUNT(pipeline_id)/70*100 FROM pipelines_results WHERE branch_name = 'master' AND pipeline_status = 'PASSED'
AND created_at BETWEEN (FROM_UNIXTIME(unix_timestamp(now()) - 604800)) AND FROM_UNIXTIME(unix_timestamp(now()))
```

### Graph `Job success rate (passed to fail) in one pipeline by a week`

#### Block A

```
SELECT time, (t.p_cnt / (t.p_cnt + t.f_cnt)) * 100 AS ratio 
FROM
((SELECT p.cnt AS p_cnt, f.cnt AS f_cnt, p.time, p.pipeline_id
FROM (
SELECT COUNT(job_name) AS cnt, created_at AS 'time', pipeline_id 
FROM jobs_results LEFT JOIN pipelines_results USING(pipeline_id, branch_name)
WHERE branch_name = 'master' AND created_at IS NOT NULL AND job_status = 'PASS' AND
created_at BETWEEN (from_unixtime(unix_timestamp(now()) - 604800)) AND from_unixtime(unix_timestamp(now()))
GROUP BY pipeline_id) p
JOIN (
SELECT COUNT(job_name) AS cnt, created_at AS 'time', pipeline_id
FROM jobs_results LEFT JOIN pipelines_results USING(pipeline_id, branch_name)
WHERE branch_name = 'master' AND created_at IS NOT NULL AND job_status = 'FAIL' AND
created_at BETWEEN (from_unixtime(unix_timestamp(now()) - 604800)) AND from_unixtime(unix_timestamp(now()))
GROUP BY pipeline_id) f
ON p.pipeline_id = f.pipeline_id)) t;
```

### Table `How many times test/keyword failed (by a week)`

### Block A

```
SELECT test_name AS 'Test name', COUNT(test_name) AS 'Number of FAILs', ((COUNT(test_name) / (SELECT COUNT(DISTINCT pipeline_id)
FROM results 
WHERE branch_name = 'master'
AND started_at BETWEEN (unix_timestamp(now()) - 604800) AND unix_timestamp(now()))) * 100) AS 'Percentage of all pipeline runs'
FROM
(SELECT pipeline_id, test_name, MAX(id), test_status
FROM results
WHERE branch_name = 'master' AND started_at BETWEEN (unix_timestamp(now()) - 604800) AND unix_timestamp(now()) AND test_status = 'FAIL'
GROUP BY test_name, pipeline_id
ORDER BY pipeline_id, test_name, id) tmp
GROUP BY test_name
ORDER BY count(test_name) DESC
limit 100;
```

### Block B

```
SELECT keyword_name AS 'Keyword name', test_message AS 'Error message', COUNT(keyword_name) AS 'Number of FAILs',
((COUNT(keyword_name) / (SELECT COUNT(DISTINCT pipeline_id)
FROM results 
WHERE branch_name = 'master'
AND started_at BETWEEN (unix_timestamp(now()) - 604800) AND unix_timestamp(now()))) * 100) AS 'Percentage of all pipeline runs'
FROM
(SELECT pipeline_id, keyword_name, MAX(id), test_status, test_message
FROM results
WHERE branch_name = 'master' AND started_at BETWEEN (unix_timestamp(now()) - 604800) AND unix_timestamp(now()) AND test_status = 'FAIL'
GROUP BY keyword_name, pipeline_id
ORDER BY pipeline_id, keyword_name, id) tmp
GROUP BY keyword_name
ORDER BY count(keyword_name) DESC
limit 100;
```
