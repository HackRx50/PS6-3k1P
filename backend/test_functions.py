from utils.functions import *
import asyncio


def test_gen_and_save_srt():
  scripts = [
    {
      "Script": "The entry age for our insurance policies is set at 18 to 65 years for adults and 3 months to 21 years for dependent children. Our policies typically come with a lifetime renewal benefit, ensuring continued coverage under normal circumstances, barring issues related to fraud or moral hazard.",
      "Title": "asdf",
    }
  ]
  processId = '4321'
  gen_and_save_srt(scripts, processId)

async def test_gen_and_save_audio():
  print('asdf')
  script = "The entry age for our insurance policies is set at 18 to 65 years for adults and 3 months to 21 years for dependent children. Our policies typically come with a lifetime renewal benefit, ensuring continued coverage under normal circumstances, barring issues related to fraud or moral hazard."
  file_path = '/temp_imgs/1234/abc'
  language = 'marathi'

  await gen_and_save_audio(script, file_path, language)

async def test_upload_to_s3():
  file = 'Ghidra.pdf'
  await upload_to_s3(file)

async def test_generate_image():
  script = "The entry age for our insurance policies is set at 18 to 65 years for adults and 3 months to 21 years for dependent children. Our policies typically come with a lifetime renewal benefit, ensuring continued coverage under normal circumstances, barring issues related to fraud or moral hazard."
  await generate_image(script, 2, '333', 960, 544)


async def test_translate_text():
  hin = "हम अपनी निजी कार पैकेज पॉलिसी प्रस्तुत करते हैं जो         विशेष रूप से आपके वाहन को विभिन्न अप्रत्याशित घटनाओ      ओं से बचाने के लिए डिज़ाइन की गई है।"
  mar = "तुमच्या वाहनाचे विविध अनपेक्षित घटनांपासून संरक्षण        ण करण्यासाठी आम्ही आमचे खाजगी कार पॅकेज धोरण सादर क    करतो."
  split = hin.split(' ')
  
  split = [word for word in split if word.strip()]
  
  N = 3
  sentences = [' '.join(split[i:i+N]) for i in range(0, len(split), N)]
  print(sentences)
  
  # asyncio.run(test_translate_text())

  ['हम अपनी निजी', 'कार पैकेज पॉलिसी', 'प्रस्तुत करत    ते हैं', 'जो विशेष रूप', 'से आपके वाहन', 'को विभिन्       न अप्रत्याशित', 'घटनाओ ओं से', 'बचाने के लिए', 'डि     िज़ाइन की गई', 'है।']
  ['तुमच्या वाहनाचे विविध', 'अनपेक्षित घटनांपासून सं       रक्षण', 'ण करण्यासाठी आम्ही', 'आमचे खाजगी कार', 'प   पॅकेज धोरण सादर', 'क करतो.']


if __name__=="__main__":
  test_gen_and_save_srt()