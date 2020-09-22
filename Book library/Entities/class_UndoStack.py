from Entities.class_CustomError import CustomError
class UndoStack(object):

    def __init__(self):
        self.__undo_stack = []
        self.__index = 0
        self.__top_index = 0

    def dig(self):
        if self.__index <= 0:
            raise CustomError('no more actions to undo!')
        self.__index -= 1
        return self.__undo_stack[self.__index]
        
    def rise(self):
        if self.__index >= self.__top_index:
            raise CustomError('no more actions to redo!')
        self.__index += 1
        return self.__undo_stack[self.__index-1]
    
    def add(self, action):
        if self.__index == len(self.__undo_stack):
            self.__undo_stack.append(action)
        else:
            self.__undo_stack[self.__index] = action
        self.__index += 1
        self.__top_index = self.__index