from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'hostel_management_secret_key_123'

# Store data in memory (for demo)
students = {}
requests = []
reviews = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin_login', methods=['POST'])
def admin_login():
    username = request.form['username']
    password = request.form['password']
    
    if username == 'admin' and password == 'admin123':
        session['user_type'] = 'admin'
        session['logged_in'] = True
        return redirect(url_for('admin_dashboard'))
    else:
        return "Invalid credentials! Try: admin / admin123"

@app.route('/admin_dashboard')
def admin_dashboard():
    if not session.get('logged_in') or session.get('user_type') != 'admin':
        return redirect('/')
    return render_template('admin.html')

@app.route('/student_login', methods=['POST'])
def student_login():
    roll = request.form['roll']
    password = request.form['password']
    
    if roll in students and students[roll]['password'] == password:
        session['user_type'] = 'student'
        session['logged_in'] = True
        session['roll'] = roll
        session['name'] = students[roll]['name']
        return redirect(url_for('student_dashboard'))
    else:
        return "Invalid roll number or password!"

@app.route('/student_register', methods=['POST'])
def student_register():
    name = request.form['name']
    roll = request.form['roll']
    password = request.form['password']
    
    if roll in students:
        return "Student already registered! Please login instead."
    
    students[roll] = {
        'name': name,
        'password': password,
        'roll': roll
    }
    
    session['user_type'] = 'student'
    session['logged_in'] = True
    session['roll'] = roll
    session['name'] = name
    
    return redirect(url_for('student_dashboard'))

@app.route('/student_dashboard')
def student_dashboard():
    if not session.get('logged_in') or session.get('user_type') != 'student':
        return redirect('/')
    return render_template('student.html', 
                         name=session.get('name', 'Student'),
                         roll=session.get('roll', ''))

@app.route('/manage_requests')
def manage_requests():
    if not session.get('logged_in') or session.get('user_type') != 'admin':
        return redirect('/')
    
    pending_requests = [req for req in requests if req['status'] == 'Pending']
    
    if not pending_requests:
        return """
        <html>
            <head><title>Manage Requests</title></head>
            <body>
                <h1>Manage Requests (0 pending)</h1>
                <a href="/admin_dashboard">Back to Dashboard</a>
                <br><br>
                <p>No pending requests!</p>
            </body>
        </html>
        """
    
    requests_html = ""
    for req in pending_requests:
        requests_html += f"""
            <div style="border:1px solid #ccc; padding:10px; margin:10px;">
                <h3>Request from {req['name']} ({req['roll']})</h3>
                <p>Hostel: {req['hostel']} | Room: {req['room']}</p>
                <p>Occupancy: {req['occupancy']} | Washroom: {req['washroom']}</p>
                <p>Status: <strong>{req['status']}</strong></p>
                <a href="/approve_request/{req['id']}">Approve</a> | 
                <a href="/reject_request/{req['id']}">Reject</a>
            </div>
        """
    
    return f"""
    <html>
        <head><title>Manage Requests</title></head>
        <body>
            <h1>Manage Requests ({len(pending_requests)} pending)</h1>
            <a href="/admin_dashboard">Back to Dashboard</a>
            <br><br>
            {requests_html}
        </body>
    </html>
    """

@app.route('/view_requests')
def view_requests():
    if not session.get('logged_in') or session.get('user_type') != 'admin':
        return redirect('/')
    
    if not requests:
        return """
        <html>
            <head><title>All Requests</title></head>
            <body>
                <h1>All Hostel Requests (0 total)</h1>
                <a href="/admin_dashboard">Back to Dashboard</a>
                <br><br>
                <p>No requests found!</p>
            </body>
        </html>
        """
    
    requests_html = ""
    for req in requests:
        color = 'green' if req['status'] == 'Approved' else 'red' if req['status'] == 'Rejected' else 'orange'
        requests_html += f"""
            <div style="border:1px solid #ccc; padding:10px; margin:10px;">
                <h3>{req['name']} ({req['roll']})</h3>
                <p>Hostel: {req['hostel']} | Room: {req['room']}</p>
                <p>Occupancy: {req['occupancy']} | Washroom: {req['washroom']}</p>
                <p>Status: <strong style="color:{color}">{req['status']}</strong></p>
            </div>
        """
    
    return f"""
    <html>
        <head><title>All Requests</title></head>
        <body>
            <h1>All Hostel Requests ({len(requests)} total)</h1>
            <a href="/admin_dashboard">Back to Dashboard</a>
            <br><br>
            {requests_html}
        </body>
    </html>
    """

@app.route('/view_reviews')
def view_reviews():
    if not session.get('logged_in') or session.get('user_type') != 'admin':
        return redirect('/')
    
    if not reviews:
        return """
        <html>
            <head><title>Student Reviews</title></head>
            <body>
                <h1>Student Reviews (0 total)</h1>
                <a href="/admin_dashboard">Back to Dashboard</a>
                <br><br>
                <p>No reviews yet!</p>
            </body>
        </html>
        """
    
    reviews_html = ""
    for i, rev in enumerate(reviews):
        reviews_html += f"""
            <div style="border:1px solid #ccc; padding:10px; margin:10px;">
                <h3>Review #{i+1}</h3>
                <p>Mess: {rev['mess']}/5 | Laundry: {rev['laundry']}/5 | Playground: {rev['playground']}/5</p>
                <p>Water: {rev['water']}/5 | WiFi: {rev['wifi']}/5 | Gym: {rev['gym']}/5</p>
                <p><strong>Comment:</strong> {rev['comment']}</p>
            </div>
        """
    
    return f"""
    <html>
        <head><title>Student Reviews</title></head>
        <body>
            <h1>Student Reviews ({len(reviews)} total)</h1>
            <a href="/admin_dashboard">Back to Dashboard</a>
            <br><br>
            {reviews_html}
        </body>
    </html>
    """

@app.route('/submit_request')
def submit_request():
    if not session.get('logged_in') or session.get('user_type') != 'student':
        return redirect('/')
    
    return """
    <html>
        <head><title>Submit Request</title></head>
        <body>
            <h1>Submit Hostel Request</h1>
            <a href="/student_dashboard">Back to Dashboard</a>
            <br><br>
            <form action="/submit_request_action" method="POST">
                <label>Hostel Type:</label><br>
                <input type="radio" name="hostel" value="In Campus" required> In Campus
                <input type="radio" name="hostel" value="Out Campus"> Out Campus<br><br>
                
                <label>Room Type:</label><br>
                <input type="radio" name="room" value="AC" required> AC
                <input type="radio" name="room" value="Non-AC"> Non-AC<br><br>
                
                <label>Occupancy:</label><br>
                <input type="radio" name="occupancy" value="Single" required> Single
                <input type="radio" name="occupancy" value="Double"> Double
                <input type="radio" name="occupancy" value="Triple"> Triple<br><br>
                
                <label>Washroom:</label><br>
                <input type="radio" name="washroom" value="With" required> With
                <input type="radio" name="washroom" value="Without"> Without<br><br>
                
                <button type="submit">Submit Request</button>
            </form>
        </body>
    </html>
    """

@app.route('/submit_request_action', methods=['POST'])
def submit_request_action():
    if not session.get('logged_in') or session.get('user_type') != 'student':
        return redirect('/')
    
    new_request = {
        'id': len(requests) + 1,
        'name': session['name'],
        'roll': session['roll'],
        'hostel': request.form['hostel'],
        'room': request.form['room'],
        'occupancy': request.form['occupancy'],
        'washroom': request.form['washroom'],
        'status': 'Pending'
    }
    requests.append(new_request)
    
    return """
    <html>
        <head><title>Request Submitted</title></head>
        <body>
            <h1>Request Submitted Successfully!</h1>
            <p>Your hostel request has been submitted and is pending approval.</p>
            <a href="/student_dashboard">Back to Dashboard</a>
        </body>
    </html>
    """

@app.route('/submit_review')
def submit_review():
    if not session.get('logged_in') or session.get('user_type') != 'student':
        return redirect('/')
    
    return """
    <html>
        <head><title>Submit Review</title></head>
        <body>
            <h1>Submit Facility Review</h1>
            <a href="/student_dashboard">Back to Dashboard</a>
            <br><br>
            <form action="/submit_review_action" method="POST">
                <label>Rate facilities (1-5):</label><br><br>
                
                Mess Service: <input type="number" name="mess" min="1" max="5" required><br>
                Laundry Service: <input type="number" name="laundry" min="1" max="5" required><br>
                Playground: <input type="number" name="playground" min="1" max="5" required><br>
                Water Services: <input type="number" name="water" min="1" max="5" required><br>
                WiFi: <input type="number" name="wifi" min="1" max="5" required><br>
                Gym: <input type="number" name="gym" min="1" max="5" required><br><br>
                
                <label>Comments:</label><br>
                <textarea name="comment" rows="4" cols="50" required></textarea><br><br>
                
                <button type="submit">Submit Review</button>
            </form>
        </body>
    </html>
    """

@app.route('/submit_review_action', methods=['POST'])
def submit_review_action():
    if not session.get('logged_in') or session.get('user_type') != 'student':
        return redirect('/')
    
    new_review = {
        'mess': int(request.form['mess']),
        'laundry': int(request.form['laundry']),
        'playground': int(request.form['playground']),
        'water': int(request.form['water']),
        'wifi': int(request.form['wifi']),
        'gym': int(request.form['gym']),
        'comment': request.form['comment']
    }
    reviews.append(new_review)
    
    return """
    <html>
        <head><title>Review Submitted</title></head>
        <body>
            <h1>Review Submitted Successfully!</h1>
            <p>Thank you for your valuable feedback.</p>
            <a href="/student_dashboard">Back to Dashboard</a>
        </body>
    </html>
    """

@app.route('/check_status')
def check_status():
    if not session.get('logged_in') or session.get('user_type') != 'student':
        return redirect('/')
    
    user_requests = [req for req in requests if req['roll'] == session['roll']]
    
    if not user_requests:
        return """
        <html>
            <head><title>Check Status</title></head>
            <body>
                <h1>Your Request Status</h1>
                <a href="/student_dashboard">Back to Dashboard</a>
                <br><br>
                <p>No requests found! <a href="/submit_request">Submit a request</a></p>
            </body>
        </html>
        """
    
    requests_html = ""
    for req in user_requests:
        color = 'green' if req['status'] == 'Approved' else 'red' if req['status'] == 'Rejected' else 'orange'
        requests_html += f"""
            <div style="border:1px solid #ccc; padding:10px; margin:10px;">
                <h3>Request #{req['id']}</h3>
                <p>Hostel: {req['hostel']} | Room: {req['room']}</p>
                <p>Occupancy: {req['occupancy']} | Washroom: {req['washroom']}</p>
                <p>Status: <strong style="color:{color}">{req['status']}</strong></p>
            </div>
        """
    
    return f"""
    <html>
        <head><title>Check Status</title></head>
        <body>
            <h1>Your Request Status</h1>
            <a href="/student_dashboard">Back to Dashboard</a>
            <br><br>
            {requests_html}
        </body>
    </html>
    """

@app.route('/approve_request/<int:request_id>')
def approve_request(request_id):
    if not session.get('logged_in') or session.get('user_type') != 'admin':
        return redirect('/')
    
    for req in requests:
        if req['id'] == request_id:
            req['status'] = 'Approved'
            break
    
    return redirect('/manage_requests')

@app.route('/reject_request/<int:request_id>')
def reject_request(request_id):
    if not session.get('logged_in') or session.get('user_type') != 'admin':
        return redirect('/')
    
    for req in requests:
        if req['id'] == request_id:
            req['status'] = 'Rejected'
            break
    
    return redirect('/manage_requests')

if __name__ == '__main__':
    print("Starting Hostel Management System...")
    print("Access the application at: http://localhost:5000")
    print("Admin Login: admin / admin123")
    app.run(debug=True, port=5000)