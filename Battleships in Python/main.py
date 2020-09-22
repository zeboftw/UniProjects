from UIs.class_GUI import GUI
from Services.class_Service import Service
from class_UI import UI
from Tests.test_class_AI import test_class_AI
from Tests.test_class_Service import test_class_Service
import unittest

if __name__=='__main__':
    unittest.main(exit=False)
    
    service = Service()
    gui = GUI(service)
    
    service = Service()
    ui = UI(service)
    ui.run()
    
    
#===============================================================================
# --------------------DEBUG----------------
# ship_type=0
# dir_x=-1 dir_y=0
# length=3,x=5 y=3
# --------------------DEBUG----------------
# ship_type=1
# dir_x=-1 dir_y=0
# length=2,x=5 y=6
# --------------------DEBUG----------------
# ship_type=2
# dir_x=0 dir_y=-1
# length=1,x=6 y=2
#===============================================================================