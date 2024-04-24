# Запуск тестов
test:
	python -m pytest -v

# Запуск тестов с формированием отчетов allure
test-allure:
	python -m pytest -v --alluredir allure-results

# Запуск allure web server на http://localhost:8000/
allure-server:
	allure serve allure-results --host "localhost" --port "8000"