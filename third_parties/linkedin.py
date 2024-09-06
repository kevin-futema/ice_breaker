import os 
import requests
from dotenv import load_dotenv

load_dotenv()

def scrape_linkedin_profile(linkedin_url: str, mock: bool = False):
    if mock:
        url = "https://gist.githubusercontent.com/kevin-futema/25dda6488a072959ed4831b77f2400e0/raw/2ee4691c288faa40826d507f016eca92bf2484c7/gistfile1.json"
        response = requests.get(
            url,
            timeout=10 
        )
    else:
        api_key = os.environ.get("PROXYCURL_API_KEY")
        headers = {'Authorization': 'Bearer ' + api_key}
        api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
        params = {
            'url': linkedin_url
        }
        response = requests.get(api_endpoint,
                                params=params,
                                headers=headers)
    data = response.json()

    data = {
        k: v
        for k,v in data.items()
        if v not in [{},"",[],None] and k not in ["people_also_viewed","certifications"]
    }
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")
    return data
        
if __name__=="__main__":
    print(
        scrape_linkedin_profile(linkedin_url="https://www.linkedin.com/in/kevin-futema-646483186/",mock=True)
    )