from utils.functions import *
import asyncio

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


"Create a colorful picture showing a family of different ages, from a baby to parents in their 30s and 40s, happily discussing insurance with a friendly superhero explaining how their coverage works!"

if __name__=="__main__":
  asyncio.run(test_gen_and_save_audio())