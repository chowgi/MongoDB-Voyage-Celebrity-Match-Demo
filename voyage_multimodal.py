import voyageai
import PIL 

vo = voyageai.Client()
# This will automatically use the environment variable VOYAGE_API_KEY.
# Alternatively, you can use vo = voyageai.Client(api_key="<your secret key>")

# Example input containing a text string and PIL image object
inputs = [
    ["This is a banana.", PIL.Image.open('banana.jpg')]
]

# Vectorize inputs
result = vo.multimodal_embed(inputs, model="voyage-multimodal-3")
print(result.embeddings)