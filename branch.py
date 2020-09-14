from database import CursorFromConnectionFromPool
class Branch:
    def __init__(self,location,id, address):
        self.location=location
        self.address=address
        self.id=id
    def __repr__(self):
        return "Branch: {}\n{}".format(self.location,self.address)
    def new_branch(self):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('insert into public.branch(branch_name,branch_address) values(%s.%s);',(self.location,self.address))
