.PHONY: bootstrap seed-scenario export-scenario smoke-test

bootstrap:
	bash scripts/bootstrap.sh

seed-scenario:
	bash scripts/seed_scenario.sh

export-scenario:
	bash scripts/export_scenario.sh

smoke-test:
	bash scripts/smoke_test.sh
