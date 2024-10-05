from functions import *

scripts = [{'Title': 'Introduction to Bajaj Allianz',
  'Script': 'Welcome to Bajaj Allianz General Insurance Company Limited, a renowned joint venture between Bajaj Finserv Limited and Allianz SE. With a legacy of over 110 years of expertise from Allianz and local market knowledge from Bajaj, we offer comprehensive and innovative insurance solutions that build trust and market leadership.'},
 {'Title': 'The Bajaj Allianz Advantage',
  'Script': "At Bajaj Allianz, we prioritize customer satisfaction through competitive pricing, quick and honest responses, and a commitment to providing peace of mind. Through our Personal Accident Insurance policy, we ensure that life's uncertainties don't translate into financial distress for families."},
 {'Title': 'Entry and Renewal Age',
  'Script': 'Our Personal Accident Insurance policy welcomes proposers and spouses aged 18 to 65 years, while dependent children can be covered from ages 5 to 21. Additionally, we offer lifetime renewal benefits under normal circumstances, ensuring continued coverage.'},
 {'Title': 'Policy Period and Premium Payment',
  'Script': 'The policy is available for periods of 1, 2, or 3 years. You can choose to pay the premium on an installment basis, available options include annual, half yearly, quarterly, or monthly payments.'},
 {'Title': 'Coverage Details',
  'Script': 'Our Personal Accident Insurance policy covers various scenarios including death, permanent total disability, and hospital confinement allowance. We have defined comprehensive, wider, and basic coverage options tailored to meet different needs.'},
 {'Title': 'Policy Benefits',
  'Script': 'Key benefits include 100% compensation for accidental death, provisions for education fees for dependent children, and a cumulative bonus for claim-free years. Additionally, reimbursement for medical expenses due to accidental injuries is included.'},
]

input_file = 'vids/Loan-Care-Brochure.mp4'
gen_and_save_srt(scripts, 'Loan-Care-Brochure')

add_subtitle(input_file, 'tmp/Loan-Care-Brochure.srt', 'vids/Loan-Care-Brochure_caps.mp4')
