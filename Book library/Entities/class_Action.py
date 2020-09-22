class Action(object):
    
    
    def __init__(self, object_on_wich_to_apply, undo_action, redo_action, object_to_aply):
        self.__object_on_wich_to_apply = object_on_wich_to_apply
        self.__undo_action = undo_action
        self.__redo_action = redo_action
        self.__object_to_aply = object_to_aply
    
    def execute(self):
        self.__undo_action(self.__object_on_wich_to_apply, self.__object_to_aply)
        
    def dexecute(self):
        self.__redo_action(self.__object_on_wich_to_apply, self.__object_to_aply)


class ComplexAction(Action):
    
    
    def __init__(self):
        self.__action_list = []
    
    def add_action(self, action):
        self.__action_list.append(action)

    def execute(self):
        for i in range(len(self.__action_list)):
            print(str(i))
            Action.execute(self.__action_list[i])

    def dexecute(self):
        for i in range(len(self.__action_list)-1, -1, -1):
            Action.dexecute(self.__action_list[i])
