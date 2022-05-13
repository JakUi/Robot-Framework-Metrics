from robot.libraries.BuiltIn import BuiltIn
from datetime import datetime
import mysql.connector
import os
import yaml


class WriteResultToDatabase:

    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        self.built_in = BuiltIn()
        self.working_dir = os.getcwd().replace(os.sep, '/')
        with open(f'{self.working_dir}/Configs/infra_info.yaml') as config_file: # Значения для переменных получаем из файла
            self.config = yaml.load(config_file, Loader=yaml.FullLoader)
        self.host = self.config["infra_info"]["tests_results_db_host"] # путь к базе данных
        self.user = self.config["infra_info"]["user"] # логин пользователя для записи в БД
        self.password = self.config["infra_info"]["password"] # пароль пользователя для записи в БД
        self.database = self.config["infra_info"]["db_tests_results"] # название БД в которую пишем результаты
        self.port = self.config["infra_info"]["port"] # порт на котором слушает БД
        self.job_name = os.environ['CI_JOB_NAME'] # переменная окружения получаем в ходе выполнения pipeline
        self.pipeline_id = os.environ['CI_PIPELINE_ID'] # переменная окружения получаем в ходе выполнения pipeline
        self.branch_name = os.environ['CI_COMMIT_BRANCH'] # переменная окружения получаем в ходе выполнения pipeline
        self.keyword, self.test_message = "NULL", "NULL" 
        self.business_libs = []
        self._get_business_libs_list()

    def _get_business_libs_list(self):
        for address, dirs, files in os.walk(f'{self.working_dir}/Resources'):
            for file in files:
                if '.robot' in file:
                    self.business_libs.append(file.replace('.robot', ''))

    def _connect_to_database(self):
        self.connection_to_db = mysql.connector.connect(
                                                        host=self.host, user=self.user, password=self.password, 
                                                        database=self.database, port=self.port
                                                       )

    def _query_for_tests_results(self):
        query = """INSERT INTO results (pipeline_id, started_at, branch_name, job_name, suite_name, test_name, test_status, 
        response_code, keyword_name, test_message, test_elapsed_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
        values = (
                  self.pipeline_id, self.started_at, self.branch_name, self.job_name, self.suite_name, self.test_name,
                  self.test_status, self.response_code, self.keyword, self.test_message, self.test_elapsed_time
                 )

        return query, values

    def _query_for_suite_results(self):
        query = """INSERT INTO suites_results (pipeline_id, branch_name, job_name, suite_name, suite_status,
                suite_elapsed_time) VALUES (%s, %s, %s, %s, %s, %s) """
        values = (self.pipeline_id, self.branch_name, self.job_name, self.suite_name, self.suite_status,
                  self.suite_elapsed_time)
        return query, values

    def _write_results_in_db(self, query, values):
        self._connect_to_database()
        cursor = self.connection_to_db.cursor()
        cursor.execute(query, values)
        self.connection_to_db.commit()
        cursor.close()
        self.connection_to_db.close()

    def start_suite(self, name, attrs):
        self.suite_name = name

    def end_keyword(self, name, attrs):
        if attrs['status'] == 'FAIL':
            if attrs['libname'] in self.business_libs:
                self.keyword = name

    def start_test(self, name, attrs):
        self.started_at = int(datetime.now().timestamp())

    def end_test(self, name, attrs):
        built_in = BuiltIn()
        try:
            self.response_code = built_in.get_variable_value('${RESP.status_code}')
        except:
            self.response_code = None
        self.test_name = name
        self.test_message = attrs["message"]
        self.test_elapsed_time = attrs["elapsedtime"]
        self.test_status = attrs["status"]
        query, values = self._query_for_tests_results()
        self._write_results_in_db(query, values)

    def end_suite(self, name, attrs):
        self.suite_status = attrs["status"]
        self.suite_elapsed_time = attrs["elapsedtime"]
        query, values = self._query_for_suite_results()
        self._write_results_in_db(query, values)
