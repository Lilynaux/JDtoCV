import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

DATA_DIR = BASE_DIR / "data"
JD_DIR = DATA_DIR / "jd"
KNOWLEDGE_BASE_DIR = BASE_DIR / "knowledge_base"
OUTPUTS_DIR = BASE_DIR / "outputs"
PDF_DIR = OUTPUTS_DIR / "pdf"
PROMPTS_DIR = BASE_DIR / "prompts"

MASTER_RESUME_CN = DATA_DIR / "master_resume_cn.tex"
MASTER_RESUME_EN = DATA_DIR / "master_resume_en.tex"

OUTPUT_JD_ANALYSIS = OUTPUTS_DIR / "jd_analysis.md"
OUTPUT_MATCH_REPORT = OUTPUTS_DIR / "match_report.md"
OUTPUT_RESUME_CN = OUTPUTS_DIR / "resume_cn.tex"
OUTPUT_RESUME_EN = OUTPUTS_DIR / "resume_en.tex"
