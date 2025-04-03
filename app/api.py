from fastapi import FastAPI
from routes.home import home_route
from routes.user import user_route
from routes.models import models_route
from routes.billing import billing_route
from routes.historyOperation import history_operations_route
#from routes.event import event_router
from database.database import init_db
import uvicorn

app = FastAPI()
app.include_router(home_route)
app.include_router(user_route, prefix='/user')
app.include_router(billing_route, prefix='/billing')
app.include_router(models_route, prefix='/models')
app.include_router(history_operations_route, prefix='/history')


@app.on_event("startup") 
def on_startup():
    init_db(demostart = True)
    

if __name__ == '__main__':
    uvicorn.run('api:app', host='0.0.0.0', port=8080, reload=True)