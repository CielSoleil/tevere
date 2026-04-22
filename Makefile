PREFIX    ?= $(HOME)/.local
EXEC       = tver
INSTALLDIR = $(PREFIX)/bin

.PHONY: install uninstall

install:
	@echo "Installing $(EXEC) to $(INSTALLDIR)"
	install -Dm755 $(EXEC) $(INSTALLDIR)/$(EXEC)
	@echo "Done. Restart your terminal."

uninstall:
	@echo "Removing $(EXEC) from $(INSTALLDIR)"
	rm -f $(INSTALLDIR)/$(EXEC)
