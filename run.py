import os
from app import app, db

from models import *
from views import *

#----------------------------------------
# launch
#----------------------------------------

if __name__ == "__main__":
	db.create_all()
	port = int(os.environ.get("PORT", 5000))
	app.run(debug=True)
