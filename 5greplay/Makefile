CC     = gcc
CXX    = g++
RM     = rm -rf
MKDIR  = mkdir -p
CP     = cp -r
MV     = mv
LN     = ln -s

# Name of static library
OUTPUT_LIB   = lib5greplay.a


ifndef MMT_BASE
  MMT_BASE             := /opt/mmt
  NEED_ROOT_PERMISSION := 1
else
  $(info INFO: Set default folder of MMT to $(MMT_BASE))
endif

# directory where MMT-DPI was installed
MMT_DPI_DIR := $(MMT_BASE)/dpi

# get git version abbrev
GIT_VERSION := $(shell git log --format="%h" -n 1)
VERSION     := 0.0.8

CACHE_LINESIZE := 64

# Embed libconfuse as static
LIBS += -l:libconfuse.a

# Set of libraries
LIBS     += -ldl -lpthread

ifdef STATIC_LINK
  CFLAGS += -DSTATIC_LINK
  LIBS   += -l:libxml2.a -l:libicuuc.a -l:libz.a -l:liblzma.a -l:libicudata.a # xml2 and dependencies
  LIBS   += -l:libmmt_core.a -l:libmmt_tcpip.a -l:libmmt_tmobile.a -l:libsctp.a -l:libpcap.a
else
  LIBS   += -l:libmmt_core.so -l:libmmt_tmobile.so -l:libxml2.so -l:libsctp.so -l:libpcap.so -l:libmmt_tcpip.a
endif

CFLAGS   += -fPIC -Wall -DVERSION_NUMBER=\"$(VERSION)\" -DGIT_VERSION=\"$(GIT_VERSION)\" -DLEVEL1_DCACHE_LINESIZE=$(CACHE_LINESIZE) \
				-Wno-unused-variable -Wno-unused-function -Wuninitialized\
				-I/usr/include/libxml2/ -I$(MMT_DPI_DIR)/include -I$(MMT_DPI_DIR)/include/dpi/mobile

CLDFLAGS += -L$(MMT_DPI_DIR)/lib -L./plugins -L/usr/local/lib -L/opt/mmt/plugins

ifdef DEBUG
  CFLAGS   += -g -DDEBUG_MODE -O0 -fstack-protector-all
else
  CFLAGS   += -O3
endif

ifdef VALGRIND
  CFLAGS += -DVALGRIND_MODE
endif

SRCDIR := $(abspath ./src)

# list all .c files inside ./src and its sub-folders
LIB_SRCS  := $(shell find $(SRCDIR)/ -type f -name '*.c')
LIB_OBJS  := $(patsubst %.c,%.o, $(LIB_SRCS))

ifndef VERBOSE
  QUIET := @
endif

# Set default target to build static library
all: $(OUTPUT_LIB)

# Static library target
$(OUTPUT_LIB): $(MMT_DPI_DIR) $(LIB_OBJS)
	@echo "[BUILD] Creating static library $(OUTPUT_LIB)"
	$(QUIET) ar rcs $@ $(LIB_OBJS)

$(MMT_DPI_DIR):
	@echo "ERROR: Not found MMT-DPI at folder $(MMT_DPI_DIR).\n"
	@exit 1
	
%.o: %.c
	@echo "[COMPILE] $(notdir $@)"
	$(QUIET) $(CC) -lm $(CFLAGS) $(CLDFLAGS) -c -o $@ $<

# list of sample rules inside ./rules folder
RULE_XML  := $(sort $(wildcard rules/*.xml))
RULE_OBJS := $(patsubst %.xml,%.so, $(RULE_XML))

rules/%.so: $(OUTPUT_LIB)
	$(QUIET) ./$(OUTPUT) compile rules/$*.so rules/$*.xml
	
sample-rules: $(RULE_OBJS)

clean-rules:
	$(QUIET) $(RM) rules/*.so rules/*.o rules/*.c
	
clean: clean-rules
	$(QUIET) $(RM) $(LIB_OBJS) $(OUTPUT_LIB) test.* $(RULE_OBJS)

# Environment variables
SYS_NAME    = $(shell uname -s)
SYS_VERSION = $(shell uname -p)

ZIP_NAME  ?= 5greplay-$(VERSION)_$(SYS_NAME)_$(SYS_VERSION).tar.gz
DIST_NAME ?= 5greplay-$(VERSION)

dist: sample-rules
	@[ "${STATIC_LINK}" ] || ( echo ">> STATIC_LINK is not set. Do 'make STATIC_LINK=1 dist"; exit 1 )
	$(MKDIR) $(DIST_NAME)
	$(CP) /opt/mmt/plugins ./rules mmt-5greplay.conf $(OUTPUT_LIB) $(DIST_NAME)/
	tar -czf $(ZIP_NAME) $(DIST_NAME)

docker-image:
	docker build --tag ${OUTPUT_LIB}:${VERSION} .
