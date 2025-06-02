from tkinter import *
from random import *
from math import *
global root, canvas, Type_Dict, Side_Dict, Size_Cell, Reverse_Branch, Class_Dict, Gas_Death_Level, Org_Death_Level, L, N, width_walls

N = 256
Blocks = 4
width_walls = 1

L = 3*(N+(Blocks*width_walls))
root = Tk()
root.minsize(L+300,L)
root.maxsize(L+300,L)
canvas = Canvas(root, width=L, height=L, bg='white')
canvas.pack()
Type_Dict = {0:'R',1:'O',2:'Y',3:'B',4:'G',5:'T',6:'T',7:'-'}
Class_Dict = {'R':'Red_Triangle_Cell', 'O':'Orange_Square_Cell', 'Y':'Yellow_Circle_Cell', 'G':'Green_Carnivor_Cell', 'B':'Blue_Pentagon_Cell', 'T':'Transport_Cell'}
Side_Dict = {'U':[0,-1], 'D':[0,1], 'L':[-1,0], 'R':[1,0]}
Reverse_Branch = {'U':'D','D':'U','L':'R','R':'L'}
Size_Cell = 3

Gas_Death_Level = 500
Org_Death_Level = 2000

def Bin_To_Int(string):
    while string[0] == '0' and len(string)>1:
        string = string[1:]
    return string

class Empty(object):
    def __init__(self):
        self.Energy = 0
        self.Amins = 0
        self.Type = 'E'
    
    def View(self,a,b):
        pass
    
    
    def Step(self, g):
        return 'Pass',0

    def Spend_and_Check(self, g):
        return 'Norm'


class Cell(object):
    def __init__(self,genom,epigenom, branches=None):
        self.Type = 'C'
        self.Energy = 32
        self.Amins = 8
        self.Energy_Spend = 4
        self.Genom = genom
        self.Age = 0
        self.Mitosis_Count = 0
        self.Turn = epigenom[0]
        self.Vegetation_Count = epigenom[1]
        self.Branches = []
        if branches != None:
            self.Branches.append(Reverse_Branch[branches])

        self.Vegeta = {}
        self.Counter_Branches = {i:0 for i in ['R','U','L','D']}
        
        for side in range(4):
            self.Vegeta[['R','U','L','D'][(side+self.Turn)%4]]=Type_Dict[int(Bin_To_Int(self.Genom[3*side:3*side+3]), 2)]

        self.Active_Turn = int(Bin_To_Int(self.Genom[12:14]), 2)
        self.Carnivor = int(Bin_To_Int(self.Genom[14:17]), 2)
        self.Max_Age = (int(Bin_To_Int(self.Genom[17:19]), 2)+1)*16
        self.Freq_Generation = (int(Bin_To_Int(self.Genom[19:21]), 2)+1)*8
        self.Mutations = int(Bin_To_Int(self.Genom[21:]), 2)+1



    def View_Branches(self,x,y):
        for i in self.Branches:
            coords = Side_Dict[i]
            canvas.create_line(x,y,x+(Size_Cell/2)*coords[0], y+(Size_Cell/2)*coords[1], width=round(Size_Cell/10), fill='brown')

    def Spend_and_Check(self, Ground):
        self.Age += 1
        self.Energy -= self.Energy_Spend

        if self.Energy <= 0 or self.Age >= self.Max_Age or Ground['Walls'] > 0 or (self.Type not in ['O','B','P'] and Ground['Gas']>=Gas_Death_Level) or (self.Type not in ['Y','B','P'] and Ground['Org']>=Org_Death_Level):
            self.Energy = max(self.Energy, 0)
            return 'Death'
        elif self.Energy >= 40 and self.Amins >= 16 and (self.Vegetation_Count+1)%self.Freq_Generation != 0:
            return 'Vegeta'

        elif self.Energy >= 104 and self.Amins >= 48 and (self.Vegetation_Count+1)%self.Freq_Generation == 0:
            return 'Generation'
            
        return 'Live'
        

        
class Red_Triangle_Cell(Cell):
    def __init__(self, genom, epigenom,branches):
        super().__init__(genom,epigenom,branches)
        self.Type = 'R'

    def Step(self, Ground):
        self.Energy += 36
        return '.',0

    def View(self, x, y):
        self.View_Branches(x,y)
        canvas.create_polygon(round(cos(pi/6)*(Size_Cell/4)+x), round(sin(pi/6)*(Size_Cell/4)+y), round(cos(-pi/2)*(Size_Cell/4)+x), round(sin(-pi/2)*(Size_Cell/4)+y), round(cos(5*pi/6)*(Size_Cell/4)+x), round(sin(5*pi/6)*(Size_Cell/4)+y), fill='red', outline='red', width=1)


class Yellow_Circle_Cell(Cell):
    def __init__(self, genom, epigenom,branches):
        super().__init__(genom,epigenom,branches)
        self.Type = 'Y'

    def Step(self, Ground):
        inc = min(Ground['Org'], 48)
        self.Amins+= inc 
        return 'Live_Y', inc

    def View(self, x, y):
        self.View_Branches(x,y)
        canvas.create_oval(round(x-Size_Cell/4),round(y-Size_Cell/4),round(x+Size_Cell/4),round(y+Size_Cell/4),fill='yellow', outline='yellow', width=1)

class Orange_Square_Cell(Cell):
    def __init__(self, genom, epigenom,branches):
        super().__init__(genom,epigenom,branches)
        self.Type = 'O'

    def Step(self, Ground):
        inc = min(Ground['Gas'], 48)
        self.Energy += inc
        return 'Live_O', inc

    def View(self, x, y):
        self.View_Branches(x,y)
        canvas.create_rectangle(round(x-Size_Cell/4),round(y-Size_Cell/4),round(x+Size_Cell/4),round(y+Size_Cell/4),fill='orange', outline='orange', width=1)



class Green_Carnivor_Cell(Cell):
    def __init__(self, genom, epigenom,branches):
        super().__init__(genom,epigenom,branches)
        self.Type = 'G'

    def Step(self, Ground):
        return 'Live_G',0

    def View(self, x, y):
        self.View_Branches(x,y)
        canvas.create_rectangle(round(x-Size_Cell/4),round(y-Size_Cell/4),round(x+Size_Cell/4),round(y+Size_Cell/4),fill='#66ff66', outline='#66ff66', width=1)
        canvas.create_oval(round(x-Size_Cell/4),round(y-Size_Cell/4),round(x+Size_Cell/4),round(y+Size_Cell/4),fill='green', outline='green', width=1)
        canvas.create_polygon(round(x-Size_Cell/4),round(y-Size_Cell/4),round(x),round(y),round(x-Size_Cell/4),round(y+Size_Cell/4),fill='#66ff66', outline='#66ff66', width=1)


class Blue_Pentagon_Cell(Cell):
    def __init__(self, genom, epigenom,branches):
        super().__init__(genom,epigenom,branches)
        self.Type = 'B'

    def Step(self, Ground):
        if self.Energy - 2*self.Amins >= 8:
            self.Energy -= 8
            self.Amins += 8
        elif self.Energy - 2*self.Amins <= -16:
            self.Energy += 8
            self.Amins -= 8
        return '.',0

    def View(self, x, y):
        self.View_Branches(x,y)
        Massive = [[round(cos((-pi/2)+(2*pi*i/5))*(Size_Cell/4)+x), round(sin((-pi/2)+(2*pi*i/5))*(Size_Cell/4)+y)] for i in range(5)]
        Massive=[Massive[i//2][i%2] for i in range(10)]
        canvas.create_polygon(Massive,fill='blue', outline='blue', width=1)

class Purple_Seed(Cell):
    def __init__(self, genom, epigenom, branches):
        super().__init__(genom,epigenom,branches)
        self.Type = 'P'
        self.Energy = 96
        self.Amins = 48
        self.Energy_Spend = 1

    def Step(self, Ground):
            return '.',0

    def View(self, x, y):
        self.View_Branches(x,y)
        
        canvas.create_oval(round(x-Size_Cell/4),round(y-Size_Cell/4),round(x+Size_Cell/4),round(y+Size_Cell/4),fill='purple', outline='purple', width=1)


class Transport_Cell(Cell):
    def __init__(self, genom, epigenom, branches):
        super().__init__(genom,epigenom,branches)
        self.Type='T'
        self.Energy_Spend = 1

    def Step(self, Ground):
            return '.',0

    def View(self, x, y):
        self.View_Branches(x,y)
    
    

class Field(object):
    def __init__(self, dim, dim_Block):
        self.dim = dim+dim_Block*width_walls
        self.size_Block = self.dim//dim_Block+width_walls
        self.field = [[Empty() for i in range(self.dim)] for ii in range(self.dim)]
        self.Ground = [[{'Org':384,'Gas':192, 'Walls':{True:4, False:0}[(i%self.size_Block < width_walls) or (ii%self.size_Block < width_walls)]} for i in range(self.dim)] for ii in range(self.dim)]
        self.Counter_Steps = 0
        self.Coords = [self.dim//2, self.dim//2]
        self.dim_Vis = (L//Size_Cell)
        self.Mode = 0
        self.Freq_of_Render = 0
        self.Pause = True

        self.Label_Steps = Label(root, text='Steps: '+str(self.Counter_Steps), fg='red', bg='black', height=2, width=17)
        self.Label_Steps.place(x=L+160,y=(3*L)//8)
        self.Label_Speed = Label(root, text = 'Speed: x'+str(2**self.Freq_of_Render), fg='orange', bg='black', height=2, width=17)
        self.Label_Speed.place(x=L+160,y=(4*L)//8)
        self.Label_Size = Label(root, text = 'Side: '+str(self.dim_Vis)+'x'+str(self.dim_Vis), fg='yellow', bg='black', height=2, width=17)
        self.Label_Size.place(x=L+160,y=(5*L)//8)
        self.Label_Stop = Label(root, text = 'Step Mode', fg='#44ff44', bg='black', height=2, width=17)
        self.Label_Stop.place(x=L+160,y=(6*L)//8)

        Grad_Org = [[str(hex(round(255 - (255-ii)*(i/15))))[-2:].replace('x','0') for ii in [87, 64, 39]] for i in range(15,-1,-1)]

        self.Gradient_Org = {i:'#'+Grad_Org[i][0]+Grad_Org[i][1]+Grad_Org[i][2] for i in range(16)}

        Grad_Gas = [[str(hex(round(i*ii/15)))[-2:].replace('x','0') for ii in [255, 255, 255]] for i in range(16)]

        self.Gradient_Gas = {i:'#'+Grad_Gas[i][0]+Grad_Gas[i][1]+Grad_Gas[i][2] for i in range(16)}

        for iX in range(self.dim):
            for iY in range(self.dim):
                if iX % self.size_Block >= width_walls and iY % self.size_Block >= width_walls:
                    r = randint(1,9)
                    if r==1:
                        genom = ''
                        for i in range(23):
                            genom += str(randint(0,1))
                        self.field[iX][iY] = Purple_Seed(genom, [0,0], None)


    def View_Labels(self):
        self.Label_Steps.config(text = 'Steps: '+str(self.Counter_Steps))
        self.Label_Speed.config(text = 'Speed: x'+str(2**self.Freq_of_Render))
        self.Label_Size.config(text = 'Side: '+str(self.dim_Vis)+'x'+str(self.dim_Vis))
        self.Label_Stop.config(text = {True:'Step Mode', False:'Run Mode'}[self.Pause])


    def View_Walls(self):
        for iX in range(-self.dim_Vis//2, self.dim_Vis//2+1):
            for iY in range(-self.dim_Vis//2, self.dim_Vis//2+1):
                iiX = (iX+self.Coords[0])%self.dim
                iiY = (iY+self.Coords[1])%self.dim
                if self.Ground[iiX][iiY]['Walls'] > 0:
                    x = iX*Size_Cell+L/2
                    y = iY*Size_Cell+L/2
                    for i in range(self.Ground[iiX][iiY]['Walls']):
                        canvas.create_line(round(x),round(y),round(x + ((sqrt(2)/2)*Size_Cell*cos(-(pi/4)-(i*pi/2)))), round(y + ((sqrt(2)/2)*Size_Cell*sin(-(pi/4)-(i*pi/2)))), fill='black', width=max(Size_Cell//5,1))                        
                
                

    def View(self):
        canvas.delete('all')


        if self.Mode == 1:
            for iX in range(-self.dim_Vis//2, self.dim_Vis//2+1):
                for iY in range(-self.dim_Vis//2, self.dim_Vis//2+1):
                    iiX = (iX+self.Coords[0])%self.dim
                    iiY = (iY+self.Coords[1])%self.dim
                    number = self.Ground[iiX][iiY]['Org']
                    grad = hex(ceil(min(15, max(0, 15-(15*number/Org_Death_Level)))))
                    colour = self.Gradient_Org[ceil(min(15, max(0, 15-(15*number/Org_Death_Level))))]
                    x = (iX)*Size_Cell+L/2
                    y = (iY)*Size_Cell+L/2
                    canvas.create_rectangle(round(x-Size_Cell/2),round(y-Size_Cell/2),round(x+Size_Cell/2),round(y+Size_Cell/2),fill=colour, outline=colour, width=1)
        
        elif self.Mode == 2:
            for iX in range(-self.dim_Vis//2, self.dim_Vis//2+1):
                for iY in range(-self.dim_Vis//2, self.dim_Vis//2+1):
                    iiX = (iX+self.Coords[0])%self.dim
                    iiY = (iY+self.Coords[1])%self.dim
                    number = self.Ground[iiX][iiY]['Gas']
                    colour = self.Gradient_Gas[ceil(min(15, max(0, 15-(15*number/Gas_Death_Level))))]
                    x = (iX)*Size_Cell+L/2
                    y = (iY)*Size_Cell+L/2
                    canvas.create_rectangle(round(x-Size_Cell/2),round(y-Size_Cell/2),round(x+Size_Cell/2),round(y+Size_Cell/2),fill=colour, outline=colour, width=1)
            
        self.View_Walls()


        for iX in range(-self.dim_Vis//2, self.dim_Vis//2+1):
            for iY in range(-self.dim_Vis//2, self.dim_Vis//2+1):
                X = (iX)*Size_Cell+L/2
                Y = (iY)*Size_Cell+L/2
                self.field[(iX+self.Coords[0])%self.dim][(iY+self.Coords[1])%self.dim].View(X, Y)

        self.View_Labels()

    def Move(self, event, direct):
        coords = Side_Dict[direct]
        self.Coords[0] += coords[0]
        self.Coords[1] += coords[1]

        self.View()

    def Size(self, event, inc):
        global Size_Cell
        Size_Cell *= inc
        if Size_Cell < 2 or Size_Cell > L//8:
            Size_Cell /= inc
        Size_Cell = round(Size_Cell)
        self.dim_Vis = L//Size_Cell

        self.View()

    def Change_Mode(self, event):
        self.Mode += 1
        self.Mode %= 3
        self.View()


    def Change_Freq(self, event, inc):
        self.Freq_of_Render =  min(max(0,self.Freq_of_Render+inc),5)
        self.View()


    def Change_Pause(self, event):
        self.Pause = not self.Pause
        self.View()
            
            


    def Step(self, event):
        self.Counter_Steps += 1

        Exchange = [[0 for i in range(self.dim)] for ii in range(self.dim)]
        for iX in range(self.dim):
            for iY in range(self.dim):
                if self.Ground[iX][iY]['Walls'] == 0:
                    gas = self.Ground[iX][iY]['Gas']
                    if gas >= 80:
                        for i in ['U','L','D','R']:
                            shift = Side_Dict[i]
                            iiX = (iX+shift[0])%self.dim
                            iiY = (iY+shift[1])%self.dim
                            if self.Ground[iiX][iiY]['Walls'] == 0:
                                Exchange[iiX][iiY] += 16
                                self.Ground[iX][iY]['Gas'] -= 16

        
        for iX in range(self.dim):
            for iY in range(self.dim):
                self.Ground[iX][iY]['Gas'] += Exchange[iX][iY]
        
                        
                
        
        for iX in range(self.dim):
            for iY in range(self.dim):
                cell = self.field[iX][iY]
                Event, inc = cell.Step(self.Ground[iX][iY])
                if Event == 'Live_Y':
                    self.Ground[iX][iY]['Org'] -= inc
                elif Event == 'Live_O':
                    self.Ground[iX][iY]['Gas'] -= inc
                elif Event == 'Live_G':
                    for iiX in range(-1,2):
                        for iiY in range(-1,2):
                            if iiY != 0 or iiX != 0:
                                cell_victim = self.field[(iX+iiX)%self.dim][(iY+iiY)%self.dim]
                                if cell_victim.Type != 'E':
                                    counter = 0
                                    for ind in range(23):
                                        if cell_victim.Genom[ind] != cell.Genom[ind]:
                                            counter += 1
                                    if counter >= cell.Carnivor:
                                        self.field[iX][iY].Energy += self.field[(iX+iiX)%self.dim][(iY+iiY)%self.dim].Energy
                                        self.field[iX][iY].Amins += self.field[(iX+iiX)%self.dim][(iY+iiY)%self.dim].Amins
                                        self.field[(iX+iiX)%self.dim][(iY+iiY)%self.dim] = Empty()
                                        break



        Exchange = [[[0,0] for i in range(self.dim)] for ii in range(self.dim)]
        for iX in range(self.dim):
            for iY in range(self.dim):
                cell = self.field[iX][iY]
                if cell.Energy >= 72:
                    for branch in cell.Branches:
                        shift = Side_Dict[branch]
                        iiX = (iX+shift[0])%self.dim
                        iiY = (iY+shift[1])%self.dim
                        cell_2 = self.field[iiX][iiY]
                        if cell_2.Type != 'E':
                            if Reverse_Branch[branch] in cell_2.Branches:
                                Exchange[iiX][iiY][0] += 16
                                self.field[iX][iY].Energy -= 16

                elif cell.Amins >= 40:
                    for branch in cell.Branches:
                        shift = Side_Dict[branch]
                        iiX = (iX+shift[0])%self.dim
                        iiY = (iY+shift[1])%self.dim
                        cell_2 = self.field[iiX][iiY]
                        if cell_2.Type != 'E':
                            if Reverse_Branch[branch] in cell_2.Branches:
                                Exchange[iiX][iiY][1] += 8
                                self.field[iX][iY].Amins -= 8
                                
        for iX in range(self.dim):
            for iY in range(self.dim):
                self.field[iX][iY].Energy += Exchange[iX][iY][0]
                self.field[iX][iY].Amins += Exchange[iX][iY][1]
            
                

        for iX in range(self.dim):
            for iY in range(self.dim):
                cell = self.field[iX][iY]
                Event = cell.Spend_and_Check(self.Ground[iX][iY])
                if Event == 'Death':
                    self.Ground[iX][iY]['Org'] += self.field[iX][iY].Energy + self.field[iX][iY].Amins + 8
                    self.Ground[iX][iY]['Walls'] = max(0, self.Ground[iX][iY]['Walls']-1)
                    self.field[iX][iY] = Empty()
                elif Event == 'Vegeta':
                    options = []
                    for ind in range(4):
                        branch = ['U', 'L', 'R', 'D'][ind]
                        Clas = cell.Vegeta[['U', 'L', 'R', 'D'][(ind+cell.Counter_Branches[branch])%4]]
                        if branch not in cell.Branches and Clas != '-':
                            shift = Side_Dict[branch]
                            if self.field[(iX+shift[0])%self.dim][(iY+shift[1])%self.dim].Type == 'E':
                                options += [[shift, branch, Clas]]
                    if options != []:
                        side = choice(options)
                        self.field[(iX+side[0][0])%self.dim][(iY+side[0][1])%self.dim] = eval(Class_Dict[side[2]]+'(cell.Genom, [(cell.Turn+cell.Active_Turn)%4, cell.Vegetation_Count+1],side[1])')
                        self.field[iX][iY].Mitosis_Count += 1
                        self.field[iX][iY].Counter_Branches[side[1]] += 1
                        self.field[iX][iY].Counter_Branches[side[1]] %= 4
                        self.field[iX][iY].Branches.append(side[1])
                        self.field[iX][iY].Energy -= 32
                        self.field[iX][iY].Amins -= 16
                elif Event == 'Live':
                    if cell.Type != 'O':
                        self.Ground[iX][iY]['Gas'] += cell.Energy_Spend
                    

                elif Event == 'Generation':
                    options = []
                    for branch in ['U', 'L', 'R', 'D']:
                        if branch not in cell.Branches:
                            shift = Side_Dict[branch]
                            if self.field[(iX+shift[0])%self.dim][(iY+shift[1])%self.dim].Type == 'E':
                                options += [[shift, branch]]
                    if options != []:
                        side = choice(options)
                        genom = cell.Genom
                        indexes = [i for i in range(23)]
                        for i in range(cell.Mutations):
                            ind = choice(indexes)
                            indexes.remove(ind)
                            genom =  genom[:ind] + str(1-int(genom[ind])) + genom[ind+1:]
                            
                            
                        self.field[(iX+side[0][0])%self.dim][(iY+side[0][1])%self.dim] = Purple_Seed(genom, [0,0], side[1])
                        self.field[iX][iY].Mitosis_Count += 1
                        self.field[iX][iY].Branches.append(side[1])
                        self.field[iX][iY].Energy -= 96
                        self.field[iX][iY].Amins -= 48
                        
        if self.Counter_Steps%(2**self.Freq_of_Render) == 0:
            self.View()
        if not self.Pause:
            root.after(500, lambda e='<Return>': self.Step(e))
                    
        
            
        
        
Game = Field(N, Blocks)
Game.View()
root.bind('<Return>',Game.Step)

root.bind('<Up>', lambda e,d='U': Game.Move(e,d))
root.bind('<Down>', lambda e,d='D': Game.Move(e,d))
root.bind('<Left>', lambda e,d='L': Game.Move(e,d))
root.bind('<Right>', lambda e,d='R': Game.Move(e,d))

root.bind('+', lambda e,d=2 : Game.Size(e,d))
root.bind('-', lambda e,d=1/2 : Game.Size(e,d))

root.bind('f', lambda e,d=1 : Game.Change_Freq(e,d))
root.bind('s', lambda e,d=1-1 : Game.Change_Freq(e,d))

root.bind('*', Game.Change_Mode)

root.bind('=', Game.Change_Pause)

root.mainloop()
