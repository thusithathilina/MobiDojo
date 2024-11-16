from flask import Blueprint
from . import function1
from . import function2
from . import function3
from . import function4

function1 = Blueprint('function1', __name__)
function2 = Blueprint('function2', __name__)
function3 = Blueprint('function3', __name__)
function4 = Blueprint('function4', __name__)

