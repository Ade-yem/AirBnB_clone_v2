from models.base_model import BaseModel
from models import storage
from models.state import State

all_objs = storage.all(State)
for obj_id in all_objs.keys():
    obj = all_objs[obj_id]
    print(obj)