from llvmlite import ir

class SymbolTable:
    def __init__(self):
        self.Table = [{}]
        self.CurrentLevel = 0  

    def GetItem(self, item):
        i = self.CurrentLevel
        while i >= 0:
            TheItemList = self.Table[i]
            if item in TheItemList:
                return TheItemList[item]
            i -= 1
        return None

    def AddItem(self, key, value):
        if key in self.Table[self.CurrentLevel]:
            Result = {"result":"fail", "reason":'重复定义'}
            return Result
        self.Table[self.CurrentLevel][key] = value
        return {"result":"success"}

    def JudgeExist(self, item):
        i = self.CurrentLevel
        while i >= 0:
            if item in self.Table[i]:
                return True
            i -= 1
        return False

    def EnterScope(self):
        self.CurrentLevel += 1
        self.Table.append({})

    def QuitScope(self):
        if self.CurrentLevel == 0:
            return
        self.Table.pop(-1)
        self.CurrentLevel -= 1
    
    def JudgeWhetherGlobal(self):
        if len(self.Table) == 1:
            return True
        else:
            return False

class Structure:
    def __init__(self):
        self.List = {}
    
    def AddItem(self, Name, MemberList, TypeList):
        #todo:处理这个错误
        if Name in self.List:
            Result = {"result":"fail", "reason":'重复定义'}
            return Result
        NewStruct = {}
        NewStruct["Members"] = MemberList
        NewStruct["Type"] = ir.LiteralStructType(TypeList)
        self.List[Name] = NewStruct
        return {"result":"success"}

    def GetMemberType(self, Name, Member):
        if Name not in self.List:
            return None
        StructItem = self.List[Name]
        TheIndex = StructItem["Members"].index(Member)
        TheType = StructItem["Type"].elements[TheIndex]
        return TheType

    def GetMemberIndex(self, Name, Member):
        if Name not in self.List:
            return None
        StructItem = self.List[Name]["Members"]
        TheIndex = StructItem.index(Member)
        return TheIndex
