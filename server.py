#!/usr/bin/env python3
# TOTO JE DÍLO MICHALA SCHNEIDERA
# VÍCE INFORMACÍ NALEZNETE V README.MD
"""
Local Network Hub Server
Real-time chat and file sharing for local network
"""

from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import os
import json
from datetime import datetime
from werkzeug.utils import secure_filename
import mimetypes
from edupage_api import Edupage
from edupage_api.exceptions import BadCredentialsException, CaptchaException
from datetime import datetime, timedelta, date
from edupage_api.timetables import Timetables
from flask import url_for
import os
from time import sleep
from raspc_notif import notif
from werkzeug.middleware.proxy_fix import ProxyFix

edupage = Edupage()

sender = notif.Sender(apikey = "CHANGE_ME_API_KEY_FOR_RPI_NOTIF_RASPCONTROLLER_ANDROID_APP")

try:
    edupage.login("example@mail.com", "CHANGE_ME_PASSWORD", "school_name")
except BadCredentialsException:
    print("Wrong username or password!")
except CaptchaException:
    print("Captcha required!")

class Edupage: (
request_timeout := 5
)

# Instance pro rozvrhy
timetables = Timetables(edupage)

# Zítřejší datum
tomorrow = date.today() + timedelta(days=1)

# Rozvrh pro zítřek
timetable = timetables.get_my_timetable(tomorrow)


if timetable:
    first_lesson = timetable.get_first_lesson()

    if first_lesson:
        start_time = first_lesson.start_time

        # Kontrola, že start_time je objekt s časem
        from datetime import time, datetime

        if isinstance(start_time, (time, datetime)):
            # Pokud je datetime, vybereme jen čas
            if isinstance(start_time, datetime):
                start_time = start_time.time()
            print("Začátek první hodiny zítra:", start_time.strftime("%H:%M"))
        else:
            print("⚠️ Neplatný formát času pro první hodinu – možná studijní volno nebo chybějící data.")
    else:
        print("Zítra žádná hodina.")
else:
    print("Rozvrh pro zítřek nebyl nalezen.")



def get_next_day_first_lesson(edupage):
    # vytvoříme rozvrhy pro přihlášeného uživatele
    timetables = Timetables(edupage)

    # získáme rozvrh na zítřek
    tomorrow = date.today() + timedelta(days=1)
    timetable = timetables.get_my_timetable(tomorrow)
    
    if not timetable:
        return None

    # najdeme první hodinu
    first = timetable.get_first_lesson()
    if not first:
        return None

    return {
        "date": str(tomorrow),
        "start_time": first.start_time.strftime("%H:%M"),
        "end_time": first.end_time.strftime("%H:%M"),
        "subject": first.subject.name if first.subject else "Neznámý předmět",
        "teacher": first.teachers[0].name if first.teachers else "Neznámý učitel",
        "classroom": first.classrooms[0].name if first.classrooms else "Neznámá učebna",
        "online": first.is_online_lesson(),
    }



def get_next_day_first_lesson(edupage):
    timetable = get_first_lesson()
    if not timetable:
        return None

    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    # vyfiltruj pouze hodiny zítra
    lessons_tomorrow = [
        lesson for lesson in timetable if lesson.get("date") == tomorrow
    ]

    if not lessons_tomorrow:
        return None

    # seřaď podle času začátku
    lessons_tomorrow.sort(key=lambda x: x.get("start"))

    first_lesson = lessons_tomorrow[0]
    return {
        "date": tomorrow,
        "start_time": first_lesson.get("start"),
        "subject": first_lesson.get("subject"),
        "teacher": first_lesson.get("teacher"),
        "classroom": first_lesson.get("classroom"),
    }




app = Flask(__name__)
app.config['SECRET_KEY'] = 'local-network-hub-secret-key'
app.config['UPLOAD_FOLDER'] = 'static'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max file size
# app.config['SERVER_NAME'] = 'hub.lan'
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", max_http_buffer_size=500 * 1024 * 1024)

# Create necessary directories
os.makedirs('files', exist_ok=True)
os.makedirs('data', exist_ok=True)

CHAT_HISTORY_FILE = 'data/chat_history.json'

# Initialize chat history file if it doesn't exist
if not os.path.exists(CHAT_HISTORY_FILE):
    with open(CHAT_HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f)

def load_chat_history():
    """Load chat history from file"""
    try:
        with open(CHAT_HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_chat_history(messages):
    """Save chat history to file"""
    try:
        with open(CHAT_HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving chat history: {e}")

def get_file_icon(filename):
    """Get emoji icon for file type"""
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    icons = {
        
        'pdf': '📄', 'doc': '📄', 'docx': '📄', 'txt': '📄', 'rtf': '📄',
        'xls': '📊', 'xlsx': '📊', 'csv': '📊',
        'mp3': '🎵', 'wav': '🎵', 'ogg': '🎵', 'flac': '🎵',
        'mp4': '🎬', 'avi': '🎬', 'mkv': '🎬', 'mov': '🎬', 'webm': '🎬',
        'zip': '📦', 'rar': '📦', '7z': '📦', 'tar': '📦', 'gz': '📦',
        'py': '🐍', 'js': '📜', 'html': '🌐', 'css': '🎨', 'json': '📋',
    }
    
    if ext in ['png', 'jpg', 'jpeg', 'webp', 'gif']:
        return f'<img src="/static/{filename}" height="64px" width="64px">'
    else:
        return icons.get(ext, '📄')




# WebSocket Events for Chat
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print(f'Client connected: {request.sid}')
    # Send chat history to newly connected client
    emit('chat_history', load_chat_history())

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print(f'Client disconnected: {request.sid}')

@socketio.on('send_message')
def handle_message(data):
    """Handle incoming chat message"""
    message = {
        'id': datetime.now().timestamp(),
        'text': data.get('text', ''),
        'username': data.get('username', 'Anonymous'),
        'timestamp': datetime.now().strftime('%H:%M'),
        'date': datetime.now().strftime('%Y-%m-%d'),
        'type': data.get('type', 'text'),  # text, gif, markdown
        'gif_url': data.get('gif_url', None)
    }
    
    # Save to history
    history = load_chat_history()
    history.append(message)
    # Keep only last 500 messages
    if len(history) > 500:
        history = history[-500:]
    save_chat_history(history)
    
    # Broadcast to all clients
    emit('new_message', message, broadcast=True)

@socketio.on('typing')
def handle_typing(data):
    """Handle typing indicator"""
    emit('user_typing', data, broadcast=True, include_self=False)

# REST API Endpoints for File Management
@app.route('/api/files', methods=['GET'])
def list_files():
    """List all files in the shared folder"""
    try:
        files = []
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.isfile(filepath):
                stat = os.stat(filepath)
                files.append({
                    'name': filename,
                    'size': stat.st_size,
                    'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%d.%m.%Y %H:%M'),
                    'icon': get_file_icon(filename)
                })
        
        # Sort by modification time (newest first)
        files.sort(key=lambda x: x['modified'], reverse=True)
        return jsonify({'success': True, 'files': files})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/files/upload', methods=['POST'])
def upload_file():
    """Upload a file to the shared folder"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Handle duplicate filenames
        base, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(filepath):
            filename = f"{base}_{counter}{ext}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            counter += 1
        
        file.save(filepath)
        
        stat = os.stat(filepath)
        file_info = {
            'name': filename,
            'size': stat.st_size,
            'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%d.%m.%Y %H:%M'),
            'icon': get_file_icon(filename)
        }
        
        # Notify all clients about new file
        socketio.emit('file_uploaded', file_info)
        
        return jsonify({'success': True, 'file': file_info})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/files/download/<filename>', methods=['GET'])
def download_file(filename):
    """Download a file from the shared folder"""
    try:
        return send_from_directory(
            app.config['UPLOAD_FOLDER'],
            filename,
            as_attachment=True
        )
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 404

@app.route('/api/files/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    """Delete a file from the shared folder"""
    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            # Notify all clients about file deletion
            socketio.emit('file_deleted', {'name': filename})
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/chat/history', methods=['GET'])
def get_chat_history():
    """Get chat history"""
    return jsonify({'success': True, 'messages': load_chat_history()})

@app.route('/api/chat/clear', methods=['POST'])
def clear_chat_history():
    """Clear chat history"""
    save_chat_history([])
    socketio.emit('chat_cleared')
    return jsonify({'success': True})

@app.route('/netflix', methods=['GET'])
def netflix():
    """Serve the main NETFLIX KE PITAJI file"""
    return send_from_directory(
            'netflix',
            'index.html'
        )

@app.route('/api/schyr', methods=['GET'])
def get_school_year():
   
    year = edupage.get_school_year()  

    if year is None:
        return jsonify({
            "success": False,
            "message": "Nelze načíst školní rok, asi chyba s přihlášením (nebo jsou prázdniny či nejsi žákem školy)."
        })
    else:
        return jsonify({
            "success": True,
            "year": year
        })

@app.route('/api/zapnoutsvetlo', methods=['GET'])
def lighton():
    os.system("sudo gpioset gpiochip0 17=1") 
    notif_message = f"Svetlo bylo rozsviceno." 
    notification = notif.Notification("Attention!", notif_message, high_priority = True) 
    sender.send_notification(notification)
    return '', 204


@app.route('/api/vypnoutsvetlo', methods=['GET'])
def lightoff():
    os.system("sudo gpioset gpiochip0 17=0")
    return '', 204


@app.route('/api/minutaon', methods=['GET'])
def minutkasv():
	os.system("sudo gpioset gpiochip0 17=1")
	sleep(60)
	os.system("sudo gpioset gpiochip0 17=0")
	return '', 204


@app.route('/api/next_lesson', methods=['GET'])
def next_lesson():
    try:
        timetables = Timetables(edupage)
        tomorrow = date.today() + timedelta(days=1)
        timetable = timetables.get_my_timetable(tomorrow)

        if not timetable:
            return jsonify({"success": False, "message": "Zítra žádná hodina."})

        first_lesson = timetable.get_first_lesson()
        if not first_lesson:
            return jsonify({"success": False, "message": "Zítra žádná hodina."})

        start_time = first_lesson.start_time

        # Kontrola formátu času
        if isinstance(start_time, (time, datetime)):
            if isinstance(start_time, datetime):
                start_time = start_time.time()
            return jsonify({
                "success": True,
                "start_time": start_time.strftime("%H:%M")
            })
        else:
            # start_time není validní formát
            return jsonify({
                "success": True,
                "message": "ZÍTRA NENÍ ŠKOLA/VYUČOVÁNÍ."
            })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/')
def index():
    """Serve the main HTML file"""
    return send_file('index.html')

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})

   

if __name__ == '__main__':
    print("=" * 60)
    print("🏠 Local Network Hub Server")
    print("=" * 60)
    print(f"📁 Files folder: {os.path.abspath(app.config['UPLOAD_FOLDER'])}")
    print(f"💬 Chat history: {os.path.abspath(CHAT_HISTORY_FILE)}")
    print("=" * 60)
    print("🌐 Server starting on http://0.0.0.0:2002")
    print("📱 Access from other devices using your local IP")
    print("=" * 60)
    
    socketio.run( app, host='0.0.0.0', 
    port=2002, 
    debug=True, allow_unsafe_werkzeug=True 
)

