# 🔧 Excel Agent Troubleshooting Guide

## 🚨 **Common Issues & Solutions**

### **Port 5000 Already in Use**
**Problem:** `Address already in use` or `Port 5000 is in use`

**Solutions:**
1. **Automatic Fix:** The launcher now automatically finds an available port
2. **Manual Fix:** Disable AirPlay Receiver in System Preferences
3. **Alternative:** Use a different port by setting `EXCEL_AGENT_PORT=5002`

### **HTTP 403 Forbidden Error**
**Problem:** `Access to localhost was denied` or `HTTP ERROR 403`

**Solutions:**
1. **Check URL:** Make sure you're using the correct port (5001, 5002, etc.)
2. **Clear Browser Cache:** Refresh the page or clear cache
3. **Try Different Browser:** Chrome, Firefox, Safari
4. **Check Firewall:** Ensure localhost connections are allowed

### **"Module not found" Errors**
**Problem:** `ModuleNotFoundError: No module named 'flask'`

**Solutions:**
1. **Activate Virtual Environment:**
   ```bash
   source venv/bin/activate
   pip install flask flask-socketio pandas openpyxl
   ```

2. **Recreate Virtual Environment:**
   ```bash
   rm -rf venv
   python3 -m venv venv
   source venv/bin/activate
   pip install flask flask-socketio pandas openpyxl
   ```

### **File Upload Issues**
**Problem:** Files not uploading or processing

**Solutions:**
1. **Check File Format:** Only .xlsx and .xls files are supported
2. **Check File Size:** Large files may take time to process
3. **Check Permissions:** Ensure uploads folder is writable
4. **Clear Uploads:** Delete files in uploads/ folder if needed

### **Chat Not Responding**
**Problem:** AI chat not working or no responses

**Solutions:**
1. **Refresh Page:** Reload the browser page
2. **Check Console:** Look for JavaScript errors in browser console
3. **Restart Server:** Stop and restart the dashboard
4. **Check Connection:** Ensure WebSocket connection is active

### **Analysis Not Running**
**Problem:** Analysis button not working or stuck

**Solutions:**
1. **Check Files:** Ensure Excel files are uploaded
2. **Check Dependencies:** Verify all Python packages are installed
3. **Check Logs:** Look for error messages in terminal
4. **Restart System:** Stop and restart the entire system

## 🛠️ **Advanced Troubleshooting**

### **System Requirements**
- **Python 3.7+** - Required for the system
- **macOS 10.14+** - For optimal performance
- **4GB RAM** - Minimum recommended
- **1GB Disk Space** - For virtual environment and files

### **Port Management**
```bash
# Check what's using a port
lsof -i :5000

# Kill process on port
lsof -ti:5000 | xargs kill -9

# Find available port
for port in {5001..5010}; do
    if ! lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo "Port $port is available"
        break
    fi
done
```

### **Virtual Environment Issues**
```bash
# Check if virtual environment exists
ls -la venv/

# Recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install flask flask-socketio pandas openpyxl

# Check installed packages
pip list
```

### **File Permission Issues**
```bash
# Fix file permissions
chmod +x Launch_Unified_Dashboard.command
chmod -R 755 uploads/
chmod -R 755 data/
chmod -R 755 templates/
```

### **Network Issues**
```bash
# Test localhost connection
curl http://localhost:5001

# Check if port is listening
netstat -an | grep 5001

# Test WebSocket connection
# (Use browser developer tools Network tab)
```

## 🔍 **Debugging Steps**

### **Step 1: Check System Status**
```bash
cd "/Users/mr.adams/Desktop/Excel Agent"
python3 test_system.py
```

### **Step 2: Check Logs**
```bash
# Look for error messages in terminal output
# Check browser console for JavaScript errors
# Check network tab for failed requests
```

### **Step 3: Test Components**
```bash
# Test Python dependencies
python3 -c "import flask, flask_socketio, pandas, openpyxl; print('OK')"

# Test file upload
# Test chat functionality
# Test analysis process
```

### **Step 4: Reset System**
```bash
# Stop all processes
pkill -f unified_dashboard.py

# Clear temporary files
rm -rf uploads/*
rm -rf data/*
rm -rf templates/unified_dashboard.html

# Restart system
./Launch_Unified_Dashboard.command
```

## 📞 **Getting Help**

### **Quick Fixes**
1. **Restart System:** Stop and restart the dashboard
2. **Clear Cache:** Clear browser cache and cookies
3. **Check Port:** Use the port shown in terminal output
4. **Update Dependencies:** Reinstall Python packages

### **System Information**
When reporting issues, include:
- **macOS Version:** `sw_vers`
- **Python Version:** `python3 --version`
- **Error Messages:** Full terminal output
- **Browser:** Chrome/Firefox/Safari version
- **Port Used:** The port shown in terminal

### **Contact Information**
- **System Administrator:** Check with IT support
- **Technical Support:** Review error logs
- **Community Help:** Check user forums
- **Documentation:** Read README files

## 🎯 **Prevention Tips**

### **Regular Maintenance**
- **Update Dependencies:** Keep Python packages current
- **Clear Cache:** Regularly clear browser cache
- **Monitor Ports:** Check for port conflicts
- **Backup Data:** Keep important files backed up

### **Best Practices**
- **Use Virtual Environment:** Always activate venv
- **Check Logs:** Monitor terminal output
- **Test Regularly:** Run system tests
- **Keep Updated:** Update system components

---

**🚀 Need more help? Check the README files or contact system administrator!**
