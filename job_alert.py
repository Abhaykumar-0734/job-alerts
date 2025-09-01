import smtplib
from email.mime.text import MIMEText
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# =========================
# CONFIGURATION
# =========================
SENDER_EMAIL = "abhay.knam@gmail.com"
SENDER_PASSWORD = "ndgg nmet cevt edbl"  # Gmail App Password
RECEIVER_EMAIL = "abhaykumar0734@gmail.com"

WELLFOUND_URL = "https://wellfound.com/jobs?query=entry%20level%20software&remote=true"

# =========================
# FETCH WELLFOUND JOBS
# =========================
def fetch_wellfound_jobs():
    page = requests.get(WELLFOUND_URL, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(page.text, "html.parser")

    jobs = []
    for job_card in soup.select("a[data-test='startup-link']")[:10]:  # Top 10 results
        title = job_card.get_text(strip=True)
        link = "https://wellfound.com" + job_card["href"]
        jobs.append(f"{title} - {link}")

    return jobs if jobs else ["No Wellfound jobs found today."]

# =========================
# FETCH LINKEDIN JOBS (via Bing Search)
# =========================
def fetch_linkedin_jobs():
    query = "entry level software developer site:linkedin.com/jobs"
    url = f"https://www.bing.com/search?q={query.replace(' ', '+')}"
    page = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(page.text, "html.parser")

    jobs = []
    for item in soup.select("li.b_algo h2 a")[:10]:  # Top 10 results
        title = item.get_text(strip=True)
        link = item["href"]
        jobs.append(f"{title} - {link}")

    return jobs if jobs else ["No LinkedIn jobs found today."]

# =========================
# SEND EMAIL
# =========================
def send_email(all_jobs):
    body = "\n".join(all_jobs)
    msg = MIMEText(body)
    msg["Subject"] = f"Daily Job Results - {datetime.now().strftime('%Y-%m-%d')}"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    wellfound_jobs = fetch_wellfound_jobs()
    linkedin_jobs = fetch_linkedin_jobs()

    all_jobs = (
        ["--- Wellfound Jobs ---"] + wellfound_jobs +
        ["", "--- LinkedIn Jobs ---"] + linkedin_jobs
    )

    send_email(all_jobs)
    print("✅ Job email sent successfully with Wellfound + LinkedIn results!")
    
