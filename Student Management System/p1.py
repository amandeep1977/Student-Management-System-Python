from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from sqlite3 import *
import pandas as pd
import matplotlib.pyplot as plt
import bs4
import requests
	
def add():
	add_window.deiconify()
	main_window.withdraw()

def view():
	view_window.deiconify()
	main_window.withdraw()	
	view_window_student_data.delete(1.0, END)
	info=""
	con=None
	try:
		con=connect('Student_table.db')
		cursor=con.cursor()
		sql = "select * from student"
		cursor.execute(sql)
		data = cursor.fetchall()
		for d in data:
			info = info + "Roll no: " + str(d[0]) +"\t\tName: "+ str(d[1]) + "\t\tMarks: " + str(d[2]) + '\n'
		print(info)
		view_window_student_data.insert(INSERT, info)
	except Exception as e:
		showerror('Failure', e)
	finally:
		if con is not None:
			con.close()
			




def update():
	update_window.deiconify()
	main_window.withdraw()

def delete():
	delete_window.deiconify()
	main_window.withdraw()

def save(num):
	if num == 1:
		con=None
		try:
			con=connect('Student_table.db')
			cursor=con.cursor()
			sql = "insert into student values ('%d', '%s', '%d')"
			r = int(add_window_ent_rno.get())
			n = add_window_ent_name.get()
			m = int(add_window_ent_marks.get())
			
			if r <= 0:
				showerror('Failure', 'Roll No cannot be negative')
			elif (len(n) < 2) or (not n.isalpha()):
				showerror('Failure','Invalid name')
			elif (m < 0) or (m > 100):
				showerror('Failure', 'Invalid marks')
			else:
				cursor.execute(sql % (r, n, m))
				con.commit()
				showinfo('Success', 'Record Added')
		except ValueError:
			showerror('Failure', "Rno and marks cannot be empty")
		except Exception as e:
			showerror("Failure", e)
		finally:
			if con is not None:
				con.close()
	
	elif num == 2:
		con=None
		try:
			con=connect('Student_table.db')
			cursor=con.cursor()
			sql = "update student set name = '%s', marks='%d' where rno = '%d'"
			rno = int(update_window_ent_rno.get())
			name = update_window_ent_name.get()
			marks = int(update_window_ent_marks.get())
			cursor.execute(sql % (name, marks, rno))
			if rno <= 0:
				showerror('Failure', 'Roll No cannot be negative')
			elif (len(name) < 2) or (not name.isalpha()):
				showerror('Failure','Invalid name')
			elif (marks < 0) or (marks > 100):
				showerror('Failure', 'Invalid marks')
			elif cursor.rowcount > 0:
				showinfo('Success', "Record Updated")
				con.commit()
			else:
				showerror("Warning", "Record does not exist")
		except ValueError:
			showerror('Failure', "Rno and marks cannot be empty")
		except Exception as e:
			showerror("Failure", e)
			con.rollback()
		finally:
			if con is not None:
				con.close()

	elif num == 3:
		con=None
		try:
			con = connect('Student_table.db')
			cursor = con.cursor()
			sql = "delete from student where rno = '%d'"
			rno = int(delete_window_ent_rno.get())
			cursor.execute(sql % (rno))
			if rno <= 0:
				showerror('Failure', 'Roll No cannot be negative')
			elif cursor.rowcount > 0:
				showinfo('Success', 'Record deleted')
				con.commit()
			else:
				showerror('Check', 'Record does not exist')
		except ValueError:
			showerror('Failure', "Rno cannot be empty")
		except Exception as e:
			showerror('Issue', e)
		finally:
			if con is not None:
				con.close()
	
		
		

def back(num):
	if num == 1:
		main_window.deiconify()
		add_window.withdraw()
	elif num == 2:
		main_window.deiconify()
		view_window.withdraw()
	elif num == 3:
		main_window.deiconify()
		update_window.withdraw()
	elif num == 4:
		main_window.deiconify()
		delete_window.withdraw()
	else:
		print('Invalid')
	
def charts():
	try:
		con = connect('Student_table.db')
		cursor = con.cursor()
		sql = "select * from student"
		cursor.execute(sql)
		data = cursor.fetchall()
		df = pd.DataFrame(data)
		df.columns = ['Roll No','Name','Marks']

		Name = df["Name"].tolist()
		Marks= df['Marks'].tolist()

		plt.bar(Name,Marks,color=['red','green','brown'])

		plt.title("BATCH INFORMATION!")
		plt.xlabel("Student Names")
		plt.ylabel("Marks")
		plt.show()
	except Exception as e:
		showerror("Failed",e)
	finally:
		if con is not None:
			con.close()


try:
	wa = "https://ipinfo.io/"
	res = requests.get(wa)
	data = res.json()
	city_name = data['city']
	a1 = "http://api.openweathermap.org/data/2.5/weather?units=metric"+"&q="+city_name
	a2 = "&appid=" + "f6e4d787873078dad37e5bdce4c3e4cd"
	web_add = a1+a2
	res = requests.get(web_add)
	data = res.json()	
	temperature = data['main']
	temp = str(temperature['temp']) + "\u2103"
#QOTD
	wa = "https://www.brainyquote.com/quote_of_the_day"
	res = requests.get(wa)
	data = bs4.BeautifulSoup(res.text, 'html.parser')
	info = data.find('img',{'class':'p-qotd'})
	msg = info['alt']
except Exception as e:
	print("issue",e)




main_window = Tk()
main_window.title('S.M.S')
main_window.geometry('500x500+400+100')
main_window.configure(bg='light yellow')

f = ('Calibri', 20, 'bold')
add_button = Button(main_window, text="Add", width=10, font=f,bg='maroon',fg='dark orange', command=add)
view_button = Button(main_window, text = "View", width=10, font=f,bg='maroon',fg='dark orange', command=view)
update_button = Button(main_window, text = "Update", width=10, font=f,bg='maroon',fg='dark orange', command=update)
delete_button = Button(main_window, text = "Delete", width=10, font=f,bg='maroon',fg='dark orange', command=delete)
charts_button = Button(main_window, text = "Charts", width=10, font=f,bg='maroon',fg='dark orange', command=charts)
loc_label = Label(main_window, text="Location:" + city_name, font=f,fg='dark blue')
temp_label = Label(main_window, text="Temp: " +temp, font=f,fg='dark blue')
#qotd_label = Label(main_window, text='QOTD: ' + msg , font=f,fg='dark blue')

add_button.pack(pady=10)
view_button.pack(pady=10)
update_button.pack(pady=10)
delete_button.pack(pady=10)
charts_button.pack(pady=10)
loc_label.place(x=20, y=400)
temp_label.place(x=350,y=400)
#qotd_label.place(x=20,y=450)

add_window = Toplevel(main_window)
add_window.title('Add St.')
add_window.geometry('500x550+500+100')
add_window.configure(bg='light yellow')

add_window_lbl_rno = Label(add_window, text="Enter rno:",fg='dark blue', font=f)
add_window_ent_rno = Entry(add_window, bd=5, font=f,fg='dark blue')
add_window_lbl_name = Label(add_window, text="Enter name:",fg='dark blue', font=f)
add_window_ent_name = Entry(add_window, bd=5, font=f,fg='dark blue')
add_window_lbl_marks = Label(add_window, text="Enter marks:",fg='dark blue', font=f)
add_window_ent_marks = Entry(add_window, bd=5, font=f,fg='dark blue')
add_window_btn_save = Button(add_window, text="Save", width=10, font=f,bg='maroon',fg='dark orange', command=lambda:save(1))
add_window_btn_back = Button(add_window, text="Back", width=10, font=f,bg='maroon',fg='dark orange', command=lambda:back(1))

add_window_lbl_rno.pack(pady=10)
add_window_ent_rno.pack(pady=10)
add_window_lbl_name.pack(pady=10)
add_window_ent_name.pack(pady=10)
add_window_lbl_marks.pack(pady=10)
add_window_ent_marks.pack(pady=10) 
add_window_btn_save.pack(pady=10)
add_window_btn_back.pack(pady=10)
add_window.withdraw()



view_window = Toplevel(main_window)
view_window.title('View St.')
view_window.geometry('700x500+400+100')

view_window_student_data = ScrolledText(view_window, width=70, height=10,font=('Arial', 20, 'bold'))
view_window_btn_back = Button(view_window, text='Back',font=('Arial', 20, 'bold'), command=lambda:back(2))

view_window_student_data.pack(pady=10)
view_window_btn_back.pack(pady=10)
view_window.withdraw()



update_window = Toplevel(main_window)
update_window.title('Update St.')
update_window.geometry('500x550+500+100')
update_window.configure(bg='light yellow')

update_window_lbl_rno = Label(update_window, text="Enter rno:",fg='dark blue', font=f)
update_window_ent_rno = Entry(update_window, bd=5, font=f,fg='dark blue')
update_window_lbl_name = Label(update_window, text="Enter name:",fg='dark blue', font=f)
update_window_ent_name = Entry(update_window, bd=5, font=f,fg='dark blue')
update_window_lbl_marks = Label(update_window, text="Enter marks:",fg='dark blue', font=f)
update_window_ent_marks = Entry(update_window, bd=5, font=f,fg='dark blue')
update_window_btn_save = Button(update_window, text="Save", width=10, font=f,bg='maroon',fg='dark orange', command=lambda:save(2))
update_window_btn_back = Button(update_window, text="Back", width=10, font=f,bg='maroon',fg='dark orange', command=lambda:back(3))


update_window_lbl_rno.pack(pady=10)
update_window_ent_rno.pack(pady=10)
update_window_lbl_name.pack(pady=10)
update_window_ent_name.pack(pady=10)
update_window_lbl_marks.pack(pady=10)
update_window_ent_marks.pack(pady=10) 
update_window_btn_save.pack(pady=10)
update_window_btn_back.pack(pady=10)
update_window.withdraw()



delete_window = Toplevel(main_window)
delete_window.title('Delete St.')
delete_window.geometry('500x500+400+100')
delete_window.configure(bg='light yellow')

delete_window_lbl_rno = Label(delete_window, text="Enter rno:", font=f,fg='dark blue')
delete_window_ent_rno = Entry(delete_window, bd=5, font=f,fg='dark blue')

delete_window_btn_save = Button(delete_window, text="Save", width=10, font=f,bg='maroon',fg='dark orange', command=lambda:save(3))
delete_window_btn_back = Button(delete_window, text="Back", width=10, font=f,bg='maroon',fg='dark orange', command=lambda:back(4))

delete_window_lbl_rno.pack(pady=10)
delete_window_ent_rno.pack(pady=10)
delete_window_btn_save.pack(pady=10)
delete_window_btn_back.pack(pady=10)
delete_window.withdraw()


main_window.mainloop()