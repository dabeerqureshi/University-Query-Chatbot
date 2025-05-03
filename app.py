import streamlit as st
import os
from chatbot import create_chatbot_from_pdf
from fuzzywuzzy import process
from utils import search_wikipedia
from googletrans import Translator

# Set page configuration
st.set_page_config(
    page_title="University Admission Chatbot",
    page_icon="🎓",
    layout="centered"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

UNIVERSITY_URL = "https://nust.edu.pk/"

def initialize_chatbot():
    if "chatbot" not in st.session_state:
        if os.path.exists("data/university_info.pdf"):
            with st.spinner("Initializing chatbot..."):
                st.session_state.chatbot = create_chatbot_from_pdf("data/university_info.pdf")
            st.success("Chatbot initialized successfully!")
        else:
            st.warning("Please upload a university information PDF first.")

def process_basic_responses(prompt):
    greetings = ["hi", "hello", "how are you"]
    if any(greeting in prompt.lower() for greeting in greetings):
        return "Hello! How can I assist you with university admissions today?"
    elif "thank you" in prompt.lower():
        return "You're welcome! If you have any more questions, feel free to ask. Have a great day!"
    return None

def correct_spelling(prompt):
    common_mistakes = {
        "admissiom": "admission",
        "admisson": "admission",
        "admision": "admission",
        "universiy": "university",
        "unversity": "university",
        "univercity": "university",
        "inquiri": "inquiry",
        "inquirie": "inquiry",
        "enquery": "inquiry",
        "scholership": "scholarship",
        "schollarship": "scholarship",
        "scholarhip": "scholarship",
        "departmant": "department",
        "depatment": "department",
        "faculity": "faculty",
        "facalty": "faculty",
        "fess": "fees",
        "feez": "fees",
        "semister": "semester",
        "semestre": "semester",
        "regstration": "registration",
        "regestration": "registration",
        "registation": "registration",
        "cours": "course",
        "corse": "course",
        "curce": "course",
        "timimg": "timing",
        "timingss": "timing",
        "libary": "library",
        "liberary": "library",
        "accomodation": "accommodation",
        "acommodation": "accommodation",
        "hostal": "hostel",
        "hostle": "hostel",
        "carriculum": "curriculum",
        "cirriculum": "curriculum",
        "credts": "credits",
        "creditz": "credits",
        "schedual": "schedule",
        "shedul": "schedule",
        "acadamic": "academic",
        "acadamics": "academics",
        "reserch": "research",
        "reseach": "research",
        "reaserch": "research",
        "assigment": "assignment",
        "assiggnment": "assignment",
        "lectur": "lecture",
        "lecutre": "lecture",
        "bachelorz": "bachelors",
        "bechlors": "bachelors",
        "bachlors": "bachelors",
        "mastars": "masters",
        "mastrs": "masters",
        "libreary": "library",
        "sylabus": "syllabus",
        "syllubus": "syllabus",
        "camapus": "campus",
        "campuss": "campus",
        "clg": "college",
        "collage": "college",
        "adviser": "advisor",
        "proffesor": "professor",
        "professer": "professor",
        "deanery": "dean",
        "dormetry": "dormitory",
        "registror": "registrar",
        "enrolllment": "enrollment",
        "refference": "reference",
        "referance": "reference",
        "assistence": "assistance",
        "assisstance": "assistance",
        "interveiw": "interview",
        "intervieu": "interview",
        "secratary": "secretary",
        "secretery": "secretary",
        "evalution": "evaluation",
        "evaluaton": "evaluation",
        "oppurtunity": "opportunity",
        "oppourtunity": "opportunity",
        "experiance": "experience",
        "experiances": "experience",
        "traning": "training",
        "traing": "training",
        "aplication": "application",
        "applcation": "application",
        "eligiblity": "eligibility",
        "eligibillity": "eligibility",
        "orintation": "orientation",
        "orienation": "orientation",
        "councelling": "counseling",
        "counselling": "counseling",
        "seminar": "seminar",
        "semminar": "seminar",
        "librian": "librarian",
        "liberian": "librarian",
        "departement": "department",
        "requirments": "requirements",
        "requirment": "requirement",
        "accademic": "academic",
        "colege": "college",
        "colledge": "college",
        "accomodate": "accommodate",
        "postgraduation": "postgraduation",
        "undergarduate": "undergraduate",
        "undergrduate": "undergraduate",
        "feild": "field",
        "scolar": "scholar",
        "gradution": "graduation",
        "grduation": "graduation",
        "transcriptt": "transcript",
        "transkrip": "transcript"
    }
    for wrong, correct in common_mistakes.items():
        prompt = prompt.lower().replace(wrong, correct)
    return prompt

def get_intent(prompt):
    intent_map = {
        "course": ["course info", "subjects", "syllabus"],
        "faculty": ["faculty", "professor contact", "teacher"],
        "calendar": ["academic calendar", "term dates", "semester"],
        "exam": ["exam schedule", "tests", "midterm", "final exam"],
        "fees": ["fee structure", "tuition", "payment"],
        "admission": ["admission criteria", "apply", "eligibility"],
        "registration": ["register", "course registration"],
        "scholarship": ["scholarship", "financial aid"],
        "faq": ["faq", "policy", "rules"],
        "events": ["event", "seminar", "campus activity"],
        "hostel": ["hostel", "accommodation", "stay"],
        "library": ["library", "books", "resources"],
        "student_life": ["student life", "clubs", "activities"],
        "assignments": ["assignment", "deadline", "submission"],
        "career": ["internship", "career", "job", "placement"],
        "it_support": ["it support", "wifi", "technical issue"],
        "transport": ["bus", "transport", "shuttle"],
        "portal": ["portal", "student login", "dashboard"],
        "extracurricular": ["sports", "music", "dance", "club"],
        "helpdesk": ["helpdesk", "contact", "support"],
        "alerts": ["notification", "alert"],
        "feedback": ["feedback", "suggestion"],
        "multilingual": ["language", "urdu", "hindi", "english"],
        "personalized": ["my profile", "my info", "my timetable"],
    }

    for intent, keywords in intent_map.items():
        for keyword in keywords:
            if keyword in prompt.lower():
                return intent
    return "default"

def handle_intent(intent, prompt):
    responses = {
        "course": "You can find detailed course info in the academic section of the portal or ask about a specific course.",
        "faculty": "Faculty contacts are listed in the university directory or departmental pages.",
        "calendar": "The academic calendar is available on the university website under Academic > Calendar.",
        "exam": "Exam schedules are usually posted on the portal. Please log in to check yours.",
        "fees": "The tuition fee structure is based on your program. Please visit the Finance section of the website.",
        "admission": "Admission criteria include academic qualifications, entrance tests, and interviews where applicable.",
        "registration": "You can register for courses through the student portal during the registration window.",
        "scholarship": "Scholarship and financial aid info is available under the Financial Aid section of the university site.",
        "faq": "Common university policies are listed in the Student Handbook or FAQs page.",
        "events": "Campus events are posted on the homepage or sent via student email.",
        "hostel": "Hostel details, fees, and application process are available under the Campus Life section.",
        "library": "You can access library resources via the Library Portal. Log in with your student credentials.",
        "student_life": "Student life includes clubs, societies, and events. Check the Student Life page for more.",
        "assignments": "Assignment tracking is available in your LMS or student portal under 'My Courses'.",
        "career": "Internship and career support is provided by the Career Services department.",
        "it_support": "For IT help, contact it.support@university.edu or visit the IT Helpdesk.",
        "transport": "University shuttles run on fixed schedules. Check the Transport section for timings.",
        "portal": "The student portal can be accessed via portal.university.edu. Use your student ID to log in.",
        "extracurricular": "Extracurriculars include sports, dance, drama, and music clubs. Join via the student club portal.",
        "helpdesk": "For complex issues, contact the university helpdesk at helpdesk@university.edu.",
        "alerts": "Real-time alerts are sent via SMS and email. Please keep your contact details updated.",
        "feedback": "Thanks for your feedback! We value your input.",
        "multilingual": "Multilingual support is enabled. You can chat in English or Urdu!",
        "personalized": "Personalized responses will be enabled once you’re logged into the student portal.",
    }
    response = responses.get(intent, "Let me check on that for you...")
    return response + f" For more info, visit: {UNIVERSITY_URL}"

def translate_prompt(prompt, target_lang="en"):
    translator = Translator()
    try:
        translated = translator.translate(prompt, dest=target_lang)
        return translated.text
    except Exception:
        return prompt

def main():
    st.title("🎓 University Admission Chatbot")

    with st.sidebar:
        st.header("Setup")
        uploaded_file = st.file_uploader("Upload University PDF", type="pdf")

        if uploaded_file:
            os.makedirs("data", exist_ok=True)
            with open("data/university_info.pdf", "wb") as f:
                f.write(uploaded_file.getvalue())
            st.success("PDF uploaded successfully!")
            if st.button("Initialize Chatbot"):
                initialize_chatbot()

        st.header("Language")
        language = st.selectbox("Choose language", ["English", "Urdu"])

        st.header("Feedback")
        with st.form(key="feedback_form"):
            feedback_text = st.text_area("Your suggestions or feedback")
            submit_feedback = st.form_submit_button("Submit")

            if submit_feedback:
                os.makedirs("feedback", exist_ok=True)
                with open("feedback/feedback.txt", "a", encoding="utf-8") as f:
                    f.write(feedback_text + "\n---\n")
                st.success("Thanks for your feedback!")

    if "chatbot" not in st.session_state and os.path.exists("data/university_info.pdf"):
        initialize_chatbot()

    st.markdown("### 💬 Chat History")
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"**User**: {message['content']}")
        else:
            st.markdown(f"**Assistant**: {message['content']}")

    prompt = st.text_input("Ask about university admissions...")

    if prompt:
        # Translate input if Urdu
        if language == "Urdu":
            prompt = translate_prompt(prompt, target_lang="en")

        corrected_prompt = correct_spelling(prompt)
        st.session_state.messages.append({"role": "user", "content": corrected_prompt})
        st.markdown(f"**User**: {corrected_prompt}")

        basic_response = process_basic_responses(corrected_prompt)
        if basic_response:
            response = basic_response
        else:
            intent = get_intent(corrected_prompt)

            if intent != "default":
                response = handle_intent(intent, corrected_prompt)
            elif "chatbot" in st.session_state:
                with st.spinner("Thinking..."):
                    response = st.session_state.chatbot.get_answer(corrected_prompt)
                if not response or response.lower().strip() in ["i don't know", "i'm not sure", "sorry, i couldn't find that."]:
                    st.info("Checking Wikipedia for more info...")
                    response = search_wikipedia(corrected_prompt)
            else:
                response = "Please upload a university information PDF and initialize the chatbot first."

        # Translate output if Urdu
        if language == "Urdu":
            response = translate_prompt(response, target_lang="ur")

        st.markdown(f"**Assistant**: {response}")
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
