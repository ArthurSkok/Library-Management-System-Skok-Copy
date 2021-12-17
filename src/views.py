from datetime import date
from flask import Blueprint, render_template, flash, request, session, redirect
from models import db, Books, Borrows, Members
from forms import checkmember, AddBookForm, AddMemberForm, DeleteMemberForm, IssueBookForm, ReturnBookForm, SignUpForm, UserPageForm, SearchBookForm, DeleteBookForm, IssueLateForm
from sqlalchemy import and_, asc

app = Blueprint("app", __name__,template_folder='../templates')

@app.route('/')

@app.route('/user', methods=['GET','POST'])
def userpage():
    userpageform = UserPageForm(request.form)
    email = userpageform.email.data
    password = userpageform.password.data

    if request.method =='POST':
        
        if (email == '') | (password == ''):
            flash("Error! Missing Fields")
            return render_template('login.html')

        member = Members.query.filter(Members.email == email).first()

        if (member is not None) and (member.email == email) and (member.password == password):
            session['username'] = member.username
            return showbooks()

        else:
            flash("Error! Either Member email or Member password or both do not match")
            return render_template('login.html')

    elif 'username' not in session:
        return render_template('login.html')

    else:
        return showbooks()

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    signupform = SignUpForm(request.form)
    username = signupform.username.data
    email = signupform.email.data
    password = signupform.password.data
    confirmpassword = signupform.confirmpassword.data

    if request.method =='POST':

        if (username == '') | (email == '') | (password == '') | (confirmpassword == ''):
            flash("Error! Missing Fields")
            return render_template('index.html')

        member = Members.query.filter(Members.email == email).first()

        if member is None:

            if password == confirmpassword:
                member = Members(username, password, email, cost = 0)
                db.session.add(member)
                db.session.commit()
                return render_template('login.html')

            else:
                flash("Error! Password and Confirm Password are different.")
                return redirect('index')

        else:
            flash('Error! User with the same email already exists.')
            return redirect('index')

    else:
        return redirect('index')

@app.route('/signout')
def signout():
    session.pop('username',None)
    return render_template('login.html')

@app.route('/add_member', methods=['GET','POST'])
def add_member():
    addmemberform = AddMemberForm(request.form)
    email = addmemberform.email.data
    username = addmemberform.username.data
    password = addmemberform.password.data

    if checkmember() == 'No Member':
        return userpage()

    elif checkmember() == 'Not Admin':
        flash("Error! Please Login as Admin to access these functions")
        return render_template('login.html')
        
    if request.method == 'POST':

        if (username == '') | (email == '') | (password == ''):
            flash("Error! Missing Fields")
            return render_template('addmember.html', username = session['username'])

        member = Members.query.filter(Members.email == email).first()

        if member is None:
            member = Members(username, password, email, cost = 0)
            db.session.add(member)
            db.session.commit()
            flash("Successfully Added!")

        else:
            flash("Error! User with the same email already exists.")

    return render_template('addmember.html', username = session['username'])

@app.route('/delete_member', methods=['GET','POST'])
def delete_member():
    deletememberform = DeleteMemberForm(request.form)
    email = deletememberform.email.data

    if checkmember() == 'No Member':
        return userpage()

    elif checkmember() == 'Not Admin':
        flash("Error! Please Login as Admin to access these functions")
        return render_template('login.html')
        
    if request.method == 'POST':

        if (email == ''):
            flash("Error! Missing Fields")
            return render_template('addmember.html', username = session['username'])

        member = Members.query.filter(Members.email == email).first()

        if member is None:
            flash("Error! Could not delete member because user with that email does not exist.")

        else:
            db.session.delete(member)
            db.session.commit()
            flash("Successfully Deleted Member")

    return render_template('addmember.html', username = session['username'])

@app.route('/members', methods=['GET','POST'])
def showmembers():
    if checkmember() == 'No Member':
        return userpage()

    elif checkmember() == 'Not Admin':
        flash("Error! Please Login as Admin to access these functions")
        return render_template('login.html')

    memberlist = db.session.query(Members.username, Members.email).order_by(Members.username.asc(), Members.email.asc()).all()
    return render_template('showmembers.html', memberlist = memberlist, frametitle = "All Members", username = session['username'])

@app.route('/searchbook', methods=['POST'])
def searchbook():
    searchbookform = SearchBookForm(request.form)
    search = searchbookform.search.data

    if checkmember() == 'nomember':
        return userpage()

    else:
        booklist = Books.query.filter((Books.title.like('%' + search + '%')) | (Books.authors.like('%' + search + '%')) | (Books.genre.like('%' + search + '%')) | (Books.availability.like('%' + search + '%'))).order_by(Books.title.asc(), Books.authors.asc()).all()
        return render_template('showbooks.html', booklist = booklist, frametitle = "Search Books", username = session['username'])

@app.route('/issue_book', methods=['GET','POST'])
def issue_book():
    issuebookform = IssueBookForm(request.form)
    title = issuebookform.title.data
    email = issuebookform.email.data

    if checkmember() == 'No Member':
        return userpage()

    elif checkmember() == 'Not Admin':
        flash("Error! Please Login as admin to access these functions")
        return render_template('login.html')

    if request.method == 'POST':

        if (title == '') | (email == ''):
            flash("Error! Missing Fields")
            booklist = db.engine.execute("select title, authors, genre from Books where availability='In Stock';")
            return render_template('issuebook.html', username = session['username'], booklist = booklist, ret = False) 
        
        member = Members.query.filter(Members.email == email).first()
        book = Books.query.filter(and_(Books.title == title, Books.availability == 'In Stock')).first()

        if (member is not None) and (book is not None):
            borrow = Borrows(title, email, date.today(), late = 0, fine = 0)
            db.engine.execute("update Books set availability='Out of Stock' where title='" + title + "';")
            db.session.add(borrow)
            db.session.commit()
            flash("Succesfully Issued Book!")

        else:
            flash("Error! Either the book is not available or the member does not exist.")
    
    booklist = db.engine.execute("select title, authors, genre from Books where availability='In Stock';")
    return render_template('issuebook.html', username = session['username'], booklist = booklist, ret = False)

@app.route('/add_book', methods = ['GET','POST'])
def add_book():
    addbookform = AddBookForm(request.form)
    title = addbookform.title.data
    authors = addbookform.authors.data
    genre = addbookform.genre.data
    availability = addbookform.availability.data

    if checkmember() == 'No Member':
        return userpage()

    elif checkmember() == 'Not Admin':
        flash("Error! Please Login as Admin to access these functions")
        return render_template('login.html')

    if request.method == 'POST':

        if (title == '') | (authors == '') | (genre == '') | (availability == ''):
            flash("Error! Missing Fields")
            return render_template('addbook.html', username = session['username'])
        
        book = Books.query.filter(Books.title == title).first()

        if book is None:
            book = Books(title, authors, genre, availability)
            db.session.add(book)
            db.session.commit()
            flash("Successfully Added!")

        else:
            flash("Error! Book with the same title already exists.")

    return render_template('addbook.html', username = session['username'])

@app.route('/delete_book', methods=['GET','POST'])
def delete_book():
    deletebookform = DeleteBookForm(request.form)
    title = deletebookform.title.data

    if checkmember() == 'No Member':
        return userpage()

    elif checkmember() == 'Not Admin':
        flash("Error! Please Login as Admin to access these functions")
        return render_template('login.html')

    if request.method == 'POST':

        if (title == ''):
            flash("Error! Missing Fields")
            return render_template('addbook.html', username = session['username'])             

        book = Books.query.filter(Books.title == title).first()

        if book is None:
            flash("Error! Could not delete book because it does not exit.")

        else:
            db.session.delete(book)
            db.session.commit()
            flash("Successfully Deleted")

    return render_template('addbook.html', username = session['username'])

@app.route('/return_book', methods=['GET','POST'])
def return_book():
    returnbookform = ReturnBookForm(request.form)
    title = returnbookform.title.data
    email = returnbookform.email.data

    if checkmember() == 'No Member':
        return userpage()

    elif checkmember() == 'Not Admin':
        flash("Error! Please Login as Admin to access these functions")
        return render_template('login.html')

    if request.method == 'POST':
        if (title == '') | (email == ''):
            flash("Error! Missing Fields")
            booklist = db.engine.execute("select title, email, issuedt from Borrows;")
            return render_template('issuebook.html', username = session['username'], booklist = booklist, ret = True)

        book = Borrows.query.filter(and_(Borrows.title == title, Borrows.email == email)).first()
        
        if book is None:
            flash("Error! Book Reservation Data does not exist. ")

        else:
            added = round(book.fine, 2) 
            db.engine.execute("update Books set availability='In Stock' where title='" + title + "';")
            db.engine.execute("delete from Borrows where email='" + email + "' and title='" + title + "';")
            db.engine.execute("update Members set cost = cost + ? where email='" + email + "';", (added),)
            db.session.commit()
            flash("Succesfully Returned Book! ")

    booklist = db.engine.execute("select title, email, issuedt from Borrows;")
    return render_template('issuebook.html', username = session['username'], booklist = booklist, ret = True)

@app.route('/books', methods=['GET','POST'])
def showbooks():
    if checkmember() == 'nomember':
        return userpage()

    booklist = db.session.query(Books.title, Books.authors, Books.genre, Books.availability).order_by(Books.title.asc(), Books.authors.asc()).all()
    return render_template('showbooks.html', booklist = booklist, frametitle = "All Books", username = session['username'])

@app.route('/mybooks', methods=['GET','POST'])
def showmybooks():
    if checkmember() == 'nomember':
        return userpage()

    else:
        member = Members.query.filter(Members.username == session['username']).first()
        raw_cost = db.engine.execute("select cost from Members where username == '" + member.username + "';")
        booklist = db.engine.execute("select title, issuedt from Borrows where email='" + member.email +"';")
        cost = [item[0] for item in raw_cost]
        strippedText = str(cost).replace('[','').replace(']','').replace('\'','').replace('\"','')
        return render_template('showbooks.html', booklist = booklist,  cost = (strippedText), frametitle = "Your Books", username = session['username'])

@app.route('/issue_late', methods=['GET','POST'])
def issue_late():
    issuelateform = IssueLateForm(request.form)
    title = issuelateform.title.data

    if checkmember() == 'No Member':
        return userpage()

    elif checkmember() == 'Not Admin':
        flash("Error! Please Login as Admin to access these functions")
        return render_template('login.html')

    if request.method == 'POST':
        book = Borrows.query.filter(Borrows.title == title).first()

        if book is None:
            flash("Error in processing request! Please try again")

        else:
            db.engine.execute("update Borrows set late = 1 where title='" + title + "';")
            db.session.commit()
            flash("Successfully marked book late!")

    booklist = db.engine.execute("select title, email, issuedt, late from Borrows;")
    return render_template('issuebook.html', username = session['username'], booklist = booklist, ret = True)