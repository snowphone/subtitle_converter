SHELL := /bin/bash
DESTDIR=$$HOME/.local/bin

TARGET=$(DESTDIR)/smi2srt

install:
	# https://stackoverflow.com/a/5165468
	mkdir -p $(DESTDIR)
	cp smi2srt.py __main__.py
	zip - {__main__,smi,srt}.py | cat <(echo '#!/usr/bin/env python3') - > $(TARGET)
	$(RM) __main__.py
	chmod +x $(TARGET)

.PHONY: test coverage uninstall

test:
	pytest --verbose .

coverage:
	pytest --cov .

uninstall:
	$(RM) $(TARGET)
