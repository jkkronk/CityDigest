from pydantic import BaseModel, Field
from openai import OpenAI
import instructor
from typing import Optional

from pdf_content import pdf_to_string, get_all_pdfs_in_directory

class Article(BaseModel):
    title: str = Field(..., description="The title of the article.")
    abstract: str = Field(..., description="The abstract of the article.")
    reference: str = Field(..., description="The reference of the article.")
    image_prompt: Optional[str] = Field(..., description="An optional image prompt of the article.")

class Newletter(BaseModel):
    title: str = Field(..., description="The title of todays newsletter.")
    introduction: str = Field(..., description="A digestible easygoing introduction of todays newsletter.")
    sections: list[Article] = Field(..., description="The sections of todays newsletter.")
    funny_fact: str = Field(..., description="A funny fact about city to end todays newsletter.")

def newsletter_mdformat(newsletter: Newletter):
    text = ""
    text += f"# {newsletter.title}\n"
    text += f"__{newsletter.introduction}__\n"
    for section in newsletter.sections:
        if section.image_prompt:
            text += f"\n__IMAGE WITH PROMT {section.image_prompt}__\n \n"
        text += f"## {section.title} \n"
        text += f"{section.abstract} \n \n "
        text += f"*REFERENCE: {section.reference}*\n"

    text += f"## Funny fact\n"
    text += f"**{newsletter.funny_fact}**\n"

    return text

def save_newsletter_mdformat(newsletter: Newletter, path: str):
    with open(path, "w") as f:
        f.write(newsletter_mdformat(newsletter))

def get_newsletter(pdfs_directory, openai_api_key, country="Switzerland", city="Zurich", level="don't know much") -> Newletter:
    pdf_paths = get_all_pdfs_in_directory(pdfs_directory)

    pdf_text = ""
    for pdf_path in pdf_paths:
        pdf_text += pdf_to_string(pdf_path)

    client = instructor.patch(OpenAI(api_key=openai_api_key))
    prompt = f"""
    You are a newsletter producer that has been asked to summarize a couple of articles into very short newsletter.
    The newsletter should only consist of news from {country} and {city}. The newsletter should be very short and easy to read.
    The newsletter should be written for someone {level} about {country} and {city}.
    The newsletter should be have 5 articles. And each article should maximum be 10 sentences long.
    Write the newsletter with very personal and easygoing language. The newletter is called "Echo Echo {city}".
    
    Provide references to the articles given the input. 
    Add a prompt for an image that would be shown for some of the articles if you find it fitting.
    
    Additionally, add a funny fact about {city} to end the newsletter.
    
    Here is the text you should summarize:
    {pdf_text}
    """
    print(f"Prompt: {prompt}")
    overview: Newletter = client.chat.completions.create(
        model="gpt-4-1106-preview",
        response_model=Newletter,
        messages=[
            {"role": "user", "content": prompt},
        ],
        max_retries=2,
    )
    print(f"Overview: {overview}")
    return overview



