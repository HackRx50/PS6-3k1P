import asyncio
from functions import *
from dotenv import load_dotenv  # Correct import
import os
from openai import OpenAI
import time

load_dotenv()

client = OpenAI()

pages = [{'Title': 'Introduction to Bajaj Allianz', 'Script': 'Bajaj Allianz is a joint venture between Bajaj Finserv Limited and Allianz SE, combining the global expertise of Allianz with the local market knowledge of Bajaj. The company is known for its competitive pricing and quick response times, earning significant trust from customers in a short period of time.'}, {'Title': 'Entry Age Criteria', 'Script': 'The entry age for adults is from 18 to 65 years, while dependent children can be covered from 3 months to 21 years old. This ensures that you can secure health coverage for your entire family.'}, {'Title': 'Renewal Age Benefits', 'Script': 'Bajaj Allianz offers a lifetime renewal benefit under most circumstances, ensuring that you can renew your policy as long as you meet the guidelines and do not have issues related to fraud or misrepresentation.'}, {'Title': 'Sum Insured Options', 'Script': 'Bajaj Allianz provides various sum insured options for the Hospital Cash Daily Allowance Policy, allowing customers to choose a coverage amount that suits their needs. Options include daily benefits of Rs 500, Rs 1000, Rs 2000, and Rs 2500.'}, {'Title': 'Hospital Cash Daily Allowance Policy', 'Script': 'This policy provides a daily benefit amount during hospitalization, helping to cover incidental expenses. It guards against the financial burden during hospital stays, with specific terms for ICU admissions where benefits can be doubled.'}, {
    'Title': 'Policy Period and Discounts', 'Script': 'The policy can be taken for a period of 1, 2, or 3 years. A Long Term Policy Discount of 4% is available for a 2-year policy, and an 8% discount applies for a 3-year policy.'}, {'Title': 'Exclusions Under the Policy', 'Script': 'The policy has certain exclusions, including treatment for pre-existing diseases, specified disease/procedure waiting periods, and general exclusions like investigation and evaluation, which are important to understand before purchasing.'}, {'Title': 'Free Look Period and Grace Period', 'Script': 'Bajaj Allianz offers a 30-day free look period for new policies, allowing customers to review the terms. A grace period of 30 days is also available for policy renewals, ensuring continuity of benefits.'}, {'Title': 'Cancellation and Portability Options', 'Script': 'Policyholders can cancel their policy with a 7-day written notice. The premium will be refunded on a pro-rata basis if no claims have been made. Additionally, the policy can be ported to other insurers, providing flexibility.'}, {'Title': 'Contact Information', 'Script': 'For any queries, you can contact Bajaj Allianz via their toll-free numbers 1800-209-0144 or 1800-209-5858. You can also visit their website for more information or support.'}]

for i in range(len(pages)):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user",
              "content": "give just a short suitable prompt to give to an image generator as if talking to a 10 year old to create an image for the slide with this content: " + pages[i]["Script"]}
        ]
    )
    ans = completion.choices[0].message.content
    pages[i]['image'] = ans

print(pages)

# async def wait(t):
#     await asyncio.sleep(t)
#     print(t, 'done')


# async def main():
#     s = time.time()
#     await asyncio.gather(

#     )
#     e = time.time()
#     print(e-s)

# if __name__ == "__main__":
#     asyncio.run(main())
