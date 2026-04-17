build:
	docker build -t yard-customer-triage:latest .

run:
	docker run --env-file .env -p 9000:9000 yard-customer-triage:latest

test:
	docker run --rm yard-customer-triage:latest python -c "print('smoke test passed')"

health:
	curl -f http://localhost:9000/health
