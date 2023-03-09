
import os
import numpy as np
from datetime import datetime
import pandas as pd
from src.connector import Connector
from src.schemas import Employee,Job,Department
import traceback
 
for elem in Employee, Job, Department:
    this_connector = connector(elem)
    data = os.path.join(bpath, elem.__name__, ".csv")
    data = pd.read_csv(data)
    try:
        data = data.to_dict(orient="records")
        for this_data in data:
            this_connector.write(this_data)
    except ValueError as e:
        print(e, "\n---> ", dataset, "\n", elem)
        traceback.print_exc()    