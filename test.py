from chatbot import Chatbot
from populate_faiss import ImageFaiss, copy_images_to_matches

cb = Chatbot() 
fai = ImageFaiss() 

res = cb.get_chatbot_reply("I'm a man, want jeans that will go along with a black Tshirt")

print(res)
# copy_images_to_matches(fai.get_k_similar(5, str(res), 0.5))
copy_images_to_matches(fai.get_k_similar(k = 5, text = res))