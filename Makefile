DESTDIR=$$HOME/.local/bin

TARGET=$(DESTDIR)/smi2srt

install:
	mkdir -p $(DESTDIR)
	cp ./smi2srt.py $(TARGET)
	chmod +x $(TARGET)

.PHONY: test coverage uninstall

test:
	pytest --verbose .

coverage:
	pytest --cov .

uninstall:
	$(RM) $(TARGET)
