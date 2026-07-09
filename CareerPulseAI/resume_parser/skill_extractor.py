"""Enhanced Skill Extractor for CareerPulse AI"""
import logging
from typing import List, Set, Optional
import spacy
from spacy.matcher import PhraseMatcher
logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)
SKILL_TAXONOMY=sorted(set(["Python","SQL","Excel","Power BI","Tableau","Spark","PySpark","AWS","Azure","GCP","Machine Learning","Deep Learning","Generative AI","LLMs","NLP","Airflow","Pandas","NumPy","Docker","Kubernetes","Git","GitHub","TensorFlow","PyTorch","Scikit-learn","XGBoost","R","Java","Scala","MongoDB","PostgreSQL","MySQL","Oracle","SQLite","Hadoop","Kafka","Looker","Snowflake","BigQuery","Redshift","REST API","FastAPI","Flask","Django","Statistics","A/B Testing","Data Visualization","ETL","Data Warehousing","Business Intelligence","Excel VBA","Data Analysis","Data Cleaning","Data Mining","Data Modeling","Feature Engineering","EDA","Forecasting","Regression","Classification","Clustering","Time Series","Linux","Jupyter","VS Code","Databricks","Hive","Prompt Engineering","OpenAI","Gemini","LangChain","FAISS","ChromaDB","Communication"]))
SKILL_ALIASES={"MS Excel":"Excel","Microsoft Excel":"Excel","PowerBI":"Power BI","Power-BI":"Power BI","Microsoft Power BI":"Power BI","Postgres":"PostgreSQL","Postgre SQL":"PostgreSQL","Sklearn":"Scikit-learn","Scikit Learn":"Scikit-learn","Artificial Intelligence":"Generative AI","ML":"Machine Learning","Google Cloud":"GCP","Google Cloud Platform":"GCP","Amazon Web Services":"AWS","Natural Language Processing":"NLP"}
class SkillExtractor:
    def __init__(self,model:str="en_core_web_sm"):
        try:self.nlp=spacy.load(model)
        except OSError:
            logger.warning("spaCy model not found");self.nlp=spacy.blank("en")
        self.matcher=PhraseMatcher(self.nlp.vocab,attr="LOWER")
        pats=[self.nlp.make_doc(s) for s in SKILL_TAXONOMY]+[self.nlp.make_doc(a) for a in SKILL_ALIASES]
        self.matcher.add("SKILLS",pats)
    def extract(self,text:str)->List[str]:
        if not text.strip():return []
        doc=self.nlp(text);found:Set[str]=set()
        for _,s,e in self.matcher(doc):
            val=doc[s:e].text.strip();canon=SKILL_ALIASES.get(val,val)
            for sk in SKILL_TAXONOMY:
                if sk.lower()==canon.lower():canon=sk;break
            found.add(canon)
        low=text.lower()
        for a,c in SKILL_ALIASES.items():
            if a.lower() in low:found.add(c)
        return sorted(found)
    def extract_skills(self,text:str)->List[str]:
        return self.extract(text)
    def extract_with_confidence(self,text:str)->dict:
        skills=self.extract(text);w=max(len(text.split()),1);low=text.lower();d={}
        for sk in skills:d[sk]=round(min(1.0,0.5+(low.count(sk.lower())/w)*20),3)
        return d
def compare_resume_to_job(resume_text:str,job_description:str,extractor:Optional[SkillExtractor]=None)->dict:
    extractor=extractor or SkillExtractor();r=set(extractor.extract(resume_text));j=set(extractor.extract(job_description));m=r&j;miss=j-r;p=round((len(m)/len(j))*100,1) if j else 0.0
    return {"resume_skills":sorted(r),"required_skills":sorted(j),"matched_skills":sorted(m),"missing_skills":sorted(miss),"match_percentage":p}
def compute_career_score(match_pct:float,years_experience:float,num_skills:int)->float:
    return round(0.4*match_pct+0.3*min(years_experience/10,1)*100+0.3*min(num_skills/15,1)*100,1)
