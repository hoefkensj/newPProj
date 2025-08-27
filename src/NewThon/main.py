#!/usr/bin/env python
import signal
from dataclasses import dataclass,field
from evHID import KBEV
from Clict import Clict
import click as C
import readline,os
import sys , time
from subprocess import getoutput
from pynput import keyboard
from evHID.Types.term.posix import Term


from string import ascii_uppercase





class Cell():
	def __init__(__s,*a,**k):
		__s.id=a[0]
		__s.xy=None
		__s.width=1
		__s.rsibl=[]
		__s.csibl=[]
		__s.markup=None
		__s._data=None
		__s.edit=False
		__s._str='{XY}{M}{data}{reset}'
		__s.__kwargs__(**k)
		__s.__update__()
	def __kwargs__(__s, **k):
		__s._data=k.get('data')
		__s.width=k.get('w',1)
		__s.offset=k.get('offset',Coord(1,1))

	def setoffset(__s,offset):
		x=offset.x+(__s.id.c*__s.width)
		y=offset.y+(__s.id.r)
		__s.xy=Coord(x,y)
	def __str__(__s):
		data=__s.data if __s.data is not None else '_'
		cellstr=__s._str.format(M='{M}',XY=__s.xy,data=data,reset='\x1b[m')
		return cellstr
	@property
	def data(__s):
		return __s._data
		
	@data.setter
	def data(__s,data):
		__s._data = data
		__s.__update__()

	def __update__(s):
		s.setoffset(s.offset)


def Selector(id, **k):
	def selector_r(i):
		nonlocal selection
		row=wrap(selection.r + i)+1
		selection=ID(selection.c,row)

	def selector_c(i):
		nonlocal selection
		if selection.c==id.c:
			selector_r(1)
		col=wrap(selection.c + i)
		selection=ID(col,selection.r)+1
		return selection

	def setval(i):
		nonlocal selection
		selection = i
		return selection

	selection = k.get('start', ID(0,0))
	wrap = lambda s: ~(~s * -~-id.c)+1 % id.c
	slct = Clict()
	slct.prev = lambda: selector_c(-1)
	slct.next = lambda: selector_c(1)
	slct.read = lambda: selector_c(0)
	slct.write = setval
	return slct
	
@dataclass
class Coord:
	x:int
	y:int
	def __str__(__s):
		return f'\x1b[{__s.y};{__s.x}H'
	
@dataclass(frozen=True)
class ID:
	c:int
	r:int
	@property
	def id(__s):
		if __s.c <= 25:
			return '{C}{R}'.format(C=__s.col,R=__s.row)
	@property
	def row(__s):
		return __s.r
	@property
	def col(__s):
		return ['0',*ascii_uppercase][__s.c]
	def __str__(__s):
		return __s.id

	
class InlineTable(Clict):
	def __init__(__s,*a,**k):
		__s.term=k.get('term',Term())
		__s.keyout=keyboard.Controller()
		__s.col=Clict()
		__s.row=Clict()
		__s.data.raw=None
		__s.table=Clict()
		__s.ansi=Clict()
		__s.offset=Coord(1,1)
		__s.xy=__s.offset
		__s.rendered=Clict()
		__s._selected=[]
		__s._focused=None
		__s._markup=[]
		__s._focus
		__s.ansi.markup=''
		__s.ansi.selected=f'\x1b[48;2;196;196;196;38;2;0;0;0m'
		__s.ansi.focused=f'\x1b[53;4;3;5;1;6m'
		__s.__kwargs__(**k)
		__s.maketable()
		if __s.data.raw is not None:
			__s.setdata( __s.data.raw)
		__s.render()

	
	def __kwargs__(__s,**k):
		__s.dim.table.c=k.get('c')
		__s.dim.table.r=k.get('r')
		__s.dim.cell.w=k.get('w')
		__s.dim.widths=k.get('widths')
		__s.dim.cell.h=k.get('h')
		__s.data.raw=k.get('data',[[]])
		__s.offset=k.get('offset',__s.offset)

	def maketable(__s):
		for r in range(1,__s.dim.table.r+1):
			for c in range(1,__s.dim.table.c+1):
				id=ID(c,r)
				__s.table[id]=Cell(id,w=20,offset=__s.offset)
				__s.row[r][c]=__s.table[id]
				__s.col[c][r]=__s.table[id]
			for row in __s.row:
				for cell in __s.row[row]:
					cell.rsibl=[*__s.row[row].values()]



	def setdata(__s,data):
		__s.data.raw=data
		for r,row in enumerate(data):
			for c,col in enumerate(row):
				id=ID(c+1,r+1)
				__s.table[id].data=col

	def markup(__s,id):
		comb=''
		for a,m in zip(__s.ansi,['_markup','_selected']):
			if id in getattr(__s,m):
				comb+=__s.ansi[a]
			else:
				comb+=''
		if id == __s._focused:
			comb+=__s.ansi.focused
			# print('\x1b[20;20H',id,__s.ansi[a],m)
		return comb
	
	
	def debug(__s):
		for cell in __s.table:
			time.sleep(1)
			print(cell, __s.table[cell].format(DATA=__s.data.get(cell,'.')))
				
	def render(__s):
		# Render the whole table
		for id in __s.table:
			__s.rendered[id]=str(__s.table[id]).format(M=__s.markup(id))
		return ''.join(__s.rendered.values())
		
	def redraw(__s,row,col):
		id=ID(row,col)
		print(str(__s.table[id]).format(M=''))
		print(f'\x1b[{__s.ch};1H')

	def update(__s, row, col, content):
		xy=f'x{col}_y{row}'
		__s.data[xy] = content
		# Print the updated cell
		print(__s.table[xy].format(DATA=__s.data.get(xy,'?')))
		print(f'\x1b[{__s.ch};1H')
		
	def edit(__s,row,col):
		__s.T.mode('normal')
		cr=f'x{col}y{row}'
		cc=__s.cx[col]#+len(__s.data[cr])
		xy=f'\x1b[{__s.ry[row]};{cc}H'
		print(xy,end='')
		os.system(f"printf '\x1b[1m{__s.data[cr]}\x1b[m' >> {__s.T.tty}")
		newdata = input()
		ndata=f'\x1b[1;32m{newdata}\x1b[m'.ljust(__s.cw)
		__s.update(row,col,str(ndata))
		
	def edit_selected(__s):
		x,y,data=__s.selected
		cr = f'x{x}_y{y}'
		cc = __s.cx[x]
		xy=f'\x1b[{__s.ry[y]};{cc}H'
		# __s.T.mode('normal')
		print(xy,end='')
		print('\x1b[33,1m')
		keyboard.Controller().type(data)
		newdata=input(xy)
		# newdata =f'{xy}\x1b[33,1m'
		ndata=f'\x1b[1;32m{newdata}\x1b[m'.ljust(__s.cw)
		__s.update(y,x,str(ndata))
		
	def setcr(__s, x=0, y=0):
		ret = '\x1b[m'

		xy = f'\x1b[{__s.ry[y]};{__s.cx[x]}H'
		mk=__s.prop.markup.focus
		__s.rendered[C(x,y)] = __s.table[C(x,y)].format(
														PROP=mk,
														DATA=__s.data.get(C(x,y), '.').ljust(__s.cw),
														RET=ret)
		__s._focus[1] = [x, y, xy, mk, (__s.data[C(x,y)])]
		__s.redraw(y,x)

	def movfc(__s,n):
		x=__s._focus[1][0]+n
		y=__s._focus[1][1]
		__s.setcr(x, y)
	
	def movcr(__s,n):
		__s._cursor[1]

	def focus(s,*id):
		if len(id)>0:
			id=id[0]
			s._focused=id
			# s.update(id)
		return s._focused


	def deselect(__s):
			x,y,data=__s.selected
			cr = f'x{x}_y{y}'
			cc = __s.cx[x]
			xy=f'\x1b[{__s.ry[y]};{cc}H'
			__s.selected=[x,y]
			print(xy,end='')
			print(f'\x1b[m{__s.data[cr]}\x1b[m')
	def focus_move(__s,n=1):
		if isinstance(n,complex):
			n=int(n.imag+n.imag*(__s.dim.table.c))
		current=[*__s.table.keys()].index(__s._focused)
		newfocus=__s.table.keys()[(current+n)%len(__s.table.keys())]
		__s.focus(newfocus)

	def confirm(__s):
		if   __s.mode == 0 :  #Display Mode
			__s.mode=1
			__s.setcr()         #Select Mode

		elif __s.mode == 1:  # Display Mode
			__s.mode=2





# table.update(1, 1, 'test')
# table.update(1, 3, 'ikkel')
# table.update(4, 3, 'ikkel')
# term=Term()


# def handle_ctl(signum, stack):
# 			key = __s.dev.key()
# 			__s.clearstdin(key)
# 			__s._key = key
# 			__s._event = True
#
# 	__s.s1 = signal(SIGUSR1, receive_dev)

class Tablectl(Clict):
	def __missing__(__s,k):
		return __s.other



TableCtl=Tablectl()
TableCtl.tab   = lambda : table.focus_move(1)
TableCtl.left  = lambda : table.focus_move(-1)
TableCtl.right = lambda : table.focus_move(1)
TableCtl.up    = lambda : table.focus_move(-1j)
TableCtl.down  = lambda : table.focus_move(1j)
TableCtl.enter = lambda : table.confirm()
TableCtl.other = lambda: ...


cols=int(input('colums? '))
rows=int(input('rows? '))
initdata=[[f'c{i}r{j}' for i in range(1,cols)] for j in range(1,rows)]
with KBEV() as kb:
	table = InlineTable(c=cols,r=rows,w=15,h=1, data=initdata,term=kb.term)
	tctl = TableCtl
	
	print(table.render())
	table._selected+=[ID(4,2)]
	focus=ID(4,1)
	table.focus(focus)
	print(table.render())

	while True:
		if kb.event():
			key=kb.key
			print(f'\x1b[{rows+3};1Hkey: ',key)


		signal.pause()
		

# table.edit(2,2)

#
#
# def main():
# 	t=Term()
# 	pass
#
#
# if __name__ == '__main__':
# 	main()
# gh_asks=['repo name','owner','description','visibility=[public,private,internal]','README?','gitignore?->Python','licence? ->MIT',]
'''GNU Affero General Public License v3.0
  Apache License 2.0
  BSD 2-Clause "Simplified" License
  BSD 3-Clause "New" or "Revised" License
  Boost Software License 1.0
  Creative Commons Zero v1.0 Universal
  Eclipse Public License 2.0
  GNU General Public License v2.0
  GNU General Public License v3.0
  GNU Lesser General Public License v2.1
  MIT License
  Mozilla Public License 2.0
  The Unlicense'''
