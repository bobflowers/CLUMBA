

class Utils:

    @staticmethod
    def delListItem(lst, itemForDelete):
        if type(lst) != list:
            return lst

        for i in range(len(lst)):
            if i >= len(lst):
                return lst
            if lst[i] == itemForDelete:
                del lst[i]                

        return lst
        
