class UndoService(object):
    
    def __init__(self, undo_stack):
        self.__undo_stack = undo_stack
    
    def undo(self):
        self.__undo_stack.dig().execute()
        
    def redo(self):
        self.__undo_stack.rise().dexecute()
