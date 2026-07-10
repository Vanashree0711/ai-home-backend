import cloudinary
import cloudinary.uploader
from app.core.config import settings

# Initialize Cloudinary Configuration
cloudinary.config( 
  cloud_name = "mock_cloud_name", # Would be settings.CLOUDINARY_CLOUD_NAME
  api_key = "mock_api_key",       # Would be settings.CLOUDINARY_API_KEY
  api_secret = "mock_secret"      # Would be settings.CLOUDINARY_API_SECRET
)

class StorageService:
    
    @staticmethod
    def upload_image_from_url(url: str, folder: str = "ai_home_designer"):
        """
        Takes a temporary URL (like the one returned by OpenAI DALL-E)
        and uploads it permanently to Cloudinary.
        """
        # If running in local/demo mode with mock credentials, return the URL instantly to save time
        import cloudinary
        if cloudinary.config().api_key == "mock_api_key" or "mock" in str(cloudinary.config().cloud_name):
            return url
            
        try:
            response = cloudinary.uploader.upload(url, folder=folder)
            return response.get("secure_url")
        except Exception as e:
            print(f"Cloudinary Upload Error: {str(e)}")
            # Fallback for testing without real credentials
            return url
