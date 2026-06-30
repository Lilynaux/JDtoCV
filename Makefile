# CV per-job build system
# Usage:
#   make compile JOB=ai_pm LANG=cn    编译指定岗位的指定语言简历
#   make compile JOB=ai_pm LANG=en
#   make all     JOB=ai_pm            编译指定岗位的中英文简历
#   make new     JOB=risk_control     从 templates/ 创建新岗位目录
#   make clean   JOB=ai_pm            清理编译产物
#   make list                         列出所有岗位

TEMPLATES := templates
JOBS      := jobs

.PHONY: compile all new clean list

compile:
	@test -n "$(JOB)"  || { echo "Usage: make compile JOB=<name> LANG=cn|en"; exit 1; }
	@test -n "$(LANG)" || { echo "Usage: make compile JOB=<name> LANG=cn|en"; exit 1; }
	cd $(JOBS)/$(JOB) && xelatex resume_$(LANG).tex

all:
	@test -n "$(JOB)" || { echo "Usage: make all JOB=<name>"; exit 1; }
	cd $(JOBS)/$(JOB) && xelatex resume_cn.tex && xelatex resume_en.tex

new:
	@test -n "$(JOB)" || { echo "Usage: make new JOB=<name>"; exit 1; }
	@test ! -d $(JOBS)/$(JOB) || { echo "Error: $(JOBS)/$(JOB) already exists"; exit 1; }
	mkdir -p $(JOBS)/$(JOB)
	cp $(TEMPLATES)/resume_cn.tex $(JOBS)/$(JOB)/
	cp $(TEMPLATES)/resume_en.tex $(JOBS)/$(JOB)/
	@echo "# Paste JD here" > $(JOBS)/$(JOB)/jd.txt
	@echo ""
	@echo "Created $(JOBS)/$(JOB)/"
	@echo "  1. Paste JD into $(JOBS)/$(JOB)/jd.txt"
	@echo "  2. Edit resume_cn.tex / resume_en.tex"
	@echo "  3. make compile JOB=$(JOB) LANG=cn"

clean:
	@test -n "$(JOB)" || { echo "Usage: make clean JOB=<name>"; exit 1; }
	cd $(JOBS)/$(JOB) && rm -f *.aux *.log *.out *.synctex.gz *.fls *.fdb_latexmk *.xdv

list:
	@echo "Available jobs:"
	@ls -1 $(JOBS)/ 2>/dev/null | while read d; do echo "  - $$d"; done
