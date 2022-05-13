## Для создания таблиц в базе данных MySQL 8 можно использовать команды:

### Создаём таблицу test_results (записываем информацию о пройденных тестах)

```
CREATE TABLE test_results(id INT PRIMARY KEY AUTO_INCREMENT, started_at INT, pipeline_id INT(10), 
branch_name VARCHAR(100), job_name VARCHAR(100), suite_name TEXT, test_name TEXT, test_status VARCHAR(20), 
response_code INT, keyword_name TEXT,  test_message TEXT, test_elapsed_time INT);
```
### Создаём таблицу jobs_results (записываем информацию о пройденных job)
```
CREATE TABLE jobs_results(id INT PRIMARY KEY AUTO_INCREMENT, pipeline_id INT(10), branch_name VARCHAR(100),
job_name VARCHAR(100), job_status VARCHAR(10));
```
### Создаём таблицу pipeline_results (записываем информацию о пройденных pipeline)
```
CREATE TABLE pipeline_results(id INT PRIMARY KEY AUTO_INCREMENT, created_at TIMESTAMP, pipeline_id INT(10),
 branch_name VARCHAR(100), pipeline_status VARCHAR(15), quantity_failed_jobs INT(5), total_jobs INT(5));
```
### Создаём таблицу suite_results (записываем информацию о пройденных suit'ах)
```
CREATE TABLE suite_results(id INT PRIMARY KEY AUTO_INCREMENT, pipeline_id INT(10), branch_name VARCHAR(100),
 job_name VARCHAR(100), suite_name VARCHAR(300), suite_status VARCHAR(20) suite_elapsed_time INT(10));
```
