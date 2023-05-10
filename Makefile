# To autorefresh
# entr -r python app.py

run:
	@echo "--> Running Docker."
	docker compose up

run-debug:
	@echo "--> Running Debug Mode with IPDB"
	docker compose run --service-ports worker

bash:
	docker compose run --rm worker bash