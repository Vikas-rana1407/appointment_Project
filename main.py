from fastapi import FastAPI
#from app.api.routes import router 
from app.api.routes import router
app = FastAPI()

# Register API routes
app.include_router(router)
