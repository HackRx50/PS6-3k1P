import os

from functions import create_video

file = "uploads\Personal_Accident_brochure.pdf"

# create_video(file)

print(os.environ['FLUX_API_KEY'])

# print('clearing temp folders')
# IMGS_FOLDER = 'temp_imgs'
# AUDS_FOLDER = 'temp_auds'

# if os.path.exists(IMGS_FOLDER):
#     for file in os.listdir(IMGS_FOLDER):
#         os.remove(os.path.join(IMGS_FOLDER, file))
# else:
#     os.makedirs(IMGS_FOLDER)

# if os.path.exists(AUDS_FOLDER):
#     for file in os.listdir(AUDS_FOLDER):
#         os.remove(os.path.join(AUDS_FOLDER, file))
# else:
#     os.makedirs(AUDS_FOLDER)
