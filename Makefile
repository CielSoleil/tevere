PREFIX    ?= $(HOME)/.local
INSTALLDIR = $(PREFIX)/bin
BUILDDIR   = build
EXEC       = tevere

.PHONY = build install uninstall

build :
	mkdir -p $(BUILDDIR)
	go compile tevere.go -o $(BUILDDIR)/$(EXEC)

install:
	install -Dm755 $(BUILDDIR)/$(EXEC) $(INSTALLDIR)/$(EXEC)

uninstall:
	rm -f $(INSTALLDIR)/$(EXEC)
