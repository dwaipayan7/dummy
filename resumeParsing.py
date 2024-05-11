# --------------------------------------------------------------------------------------
from pyresparser import ResumeParser
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from pyresparser import ResumeParser
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# ----------------------------------------------------------------------------------------

# resume_path1 = "resume.pdf"
# resume_path2 = "Alice Clark CV.pdf"
# resume_path3 = "Smith Resume.pdf"
# resume_path4 = "myres.pdf"

def matchingPer(resume, job_desc):
    def info_extraction(resume_path, info):
        try:
            # Parse resume directly from PDF
            data = ResumeParser(resume_path).get_extracted_data()
            if 'skills' in data:
                return data[info]
            else:
                print("Skills not found in the resume.")
        except Exception as e:
            print(f"Error parsing resume: {e}")

    def resumeMatchingPercentage(text):
        tfidf = TfidfVectorizer(stop_words='english')
        count_mat = tfidf.fit_transform(text)
        mat_per = cosine_similarity(count_mat)[0][1] * 100
        return mat_per

    def extract_skills(job_description):
        # Define a regex pattern to match the skills section
        skills_pattern = re.compile(r'Skills Required:(.*?)\n\nEligibility:', re.DOTALL)

        # Search for the skills using the pattern
        skills_match = skills_pattern.search(job_description)

        # Extract and return the skills
        if skills_match:
            skills_section = skills_match.group(1).strip()
            # Split the skills into individual lines
            skills_list = [skill.strip() for skill in skills_section.split('\n') if skill.strip()]
            return skills_list
        else:
            return []

    skills = extract_skills(job_desc)

    # Print the extracted skills
    job_desc_str = ''
    for skill in skills:
        job_desc_str += skill
        job_desc_str += ' '
    # print("\n\n\n\n",job_desc_str)

    data = ResumeParser(resume).get_extracted_data()
    res_skills = data['skills']

    ##### ------------- fetching resume skills as a string --------------
    res_skills_str = ''
    for skill in res_skills:
        res_skills_str += skill
        res_skills_str += ' '
    # print("\n\n\n\n",res_skills_str)
    # print("\n\n\n\n",info_extraction(resume_path1, 'name'))

    matching_skills = [job_desc_str.lower()] + [res_skills_str.lower()]
    full_match = [job_desc.lower()] + [resume.lower()]
    return {
            'per': int(float(resumeMatchingPercentage(matching_skills))*3 + float(resumeMatchingPercentage(full_match))*3), 
            'name': info_extraction(resume, 'name')             
        }

# print(matchingPer(resume_path1))