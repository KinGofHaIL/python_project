import cloudinary
from cloudinary.uploader import upload

#cloundinary configuration
cloudinary.config(
    cloud_name = "dyluz1vs1",
    api_key="849388914735729",
    api_secret="gLB2m3aL9u_8ZcNBDPDIvj1z3qg"
)

#util functionn...

async def upload_image(image):
    result = upload(image)
    print("cloundianry response,",result)
    return result["secure_url"] #string
    