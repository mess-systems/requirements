PY ?= python3
OFT ?= oft
.PHONY: validate validate-warn register check trace site clean
validate:      ; $(PY) scripts/validate.py
validate-warn: ; $(PY) scripts/validate.py --mode warn --report violations.md
register:      ; $(PY) scripts/generate.py
check:         ; $(PY) scripts/validate.py && $(PY) scripts/generate.py --check
# OpenFastTrace: требования и код реализации (путь к репо реализации через IMPL=...).
# По умолчанию отчёт строится, а непокрытые требования не валят сборку: примеры покрывают
# только часть требований. TRACE_STRICT=1 включает падение при любом дефекте трассировки.
IMPL ?= examples/impl-repo
TRACE_STRICT ?= 0
trace:
	$(OFT) trace -o html -f trace.html requirements $(IMPL) || true
	$(OFT) trace -c BLACK_AND_WHITE -v failure_summaries requirements $(IMPL) || [ "$(TRACE_STRICT)" = "0" ]
site:
	rm -rf site-src && mkdir -p site-src && cp -r requirements site-src/ && cp -r docs/adr docs/process site-src/ && cp REGISTER.md site-src/ && cp docs/site-index.md site-src/index.md
	mkdocs build --strict
clean: ; rm -rf site site-src trace.html violations.md
