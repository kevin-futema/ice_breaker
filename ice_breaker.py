from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from typing import Tuple
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from output_parsers import summary_parser, Summary

def ice_break_with(name: str, mock = True) -> Tuple[Summary, str]:
    linkedin_url = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_url=linkedin_url, mock=mock)

    summary_template = """
        given the Linkedin information {information} about a person from I want you to create:
        1. A short summary
        2. Two interesting facts about them

    \n{format_instructions}
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template,
        partial_variables={"format_instructions":summary_parser.get_format_instructions()}
    )

    llm = ChatOpenAI(temperature=0, name="gpt-4o-2024-08-06")
    # llm = ChatOllama(model="mistral")
    chain = summary_prompt_template | llm | summary_parser

    res = chain.invoke({"information": linkedin_data})
    print(res)
    print(linkedin_data.get("profile_pic_url"))
    return res, linkedin_data.get("profile_pic_url")

if __name__ == "__main__":
    load_dotenv()
    print("Initializing Ice Breaker")
    ice_break_with("Kevin Futema Itau", mock = False)
