# 🎬 Complete AIDA Video Recording Guide

## **🛠️ Recording Tools Now Installed**
- ✅ **SimpleScreenRecorder** - Easy GUI recording
- ✅ **FFmpeg** - Command-line recording
- ✅ **Services Running**: Frontend (3000) + Backend (8000)

---

## **🎥 Option 1: SimpleScreenRecorder (Recommended)**

### **Start Recording:**
```bash
simplescreenrecorder
```

### **Recording Settings:**
- **Input**: Entire screen or select area
- **Video codec**: H.264 
- **Audio**: System audio + microphone
- **Quality**: High (1920x1080, 30fps)
- **Output**: `AIDA_Demo.mp4`

---

## **🎥 Option 2: FFmpeg Command Line**

### **Record Screen + Audio:**
```bash
ffmpeg -f x11grab -s 1920x1080 -r 30 -i :0.0 -f pulse -i default -c:v libx264 -preset medium -crf 23 -c:a aac -b:a 128k AIDA_Demo.mp4
```

### **Record Screen Only:**
```bash
ffmpeg -f x11grab -s 1920x1080 -r 30 -i :0.0 -c:v libx264 -preset medium -crf 23 AIDA_Demo_NoAudio.mp4
```

---

## **📋 Recording Checklist**

### **Before Recording:**
- [ ] Both services running (check with `curl localhost:3000` and `curl localhost:8000`)
- [ ] Browser open to `http://localhost:3000`
- [ ] Second tab open to `http://localhost:8000/docs`
- [ ] Terminal ready with demo commands
- [ ] Screen resolution set to 1920x1080
- [ ] Close unnecessary applications
- [ ] Test microphone audio levels

### **During Recording:**
- [ ] Follow the `VIDEO_DEMO_SCRIPT.md` step by step
- [ ] Speak clearly and at moderate pace
- [ ] Use cursor to highlight important elements
- [ ] Keep terminal commands visible for 2-3 seconds
- [ ] Show API responses in formatted JSON

### **After Recording:**
- [ ] Stop recording and save file
- [ ] Review video for quality
- [ ] Add intro/outro if desired
- [ ] Export in MP4 format

---

## **🎬 Quick Start Recording**

### **1. Start Screen Recorder:**
```bash
# GUI Method
simplescreenrecorder &

# OR Command Line Method  
ffmpeg -f x11grab -s 1920x1080 -r 30 -i :0.0 -f pulse -i default -c:v libx264 -preset medium -crf 23 -c:a aac -b:a 128k AIDA_Demo.mp4 &
```

### **2. Open Required Tabs:**
```bash
# Open browser tabs
xdg-open http://localhost:3000
xdg-open http://localhost:8000/docs
```

### **3. Prepare Demo Commands:**
```bash
# Show available commands
./demo_commands.sh
```

### **4. Start Recording and Follow Script!**
- Use `VIDEO_DEMO_SCRIPT.md` as your guide
- Total duration: 5-7 minutes
- Cover all 9 scenes as outlined

---

## **🎯 Demo Flow Summary**

1. **Introduction** (30s) - Show AIDA homepage
2. **DAO Health** (60s) - 73.6% health score
3. **Treasury** (90s) - $2.5M portfolio analysis  
4. **Governance** (60s) - 45 proposals, 71% success
5. **Cross-Chain** (60s) - $913K across 3 networks
6. **AI Predictions** (45s) - 10 proposals tracked
7. **Automation** (45s) - Execute treasury rebalancing
8. **API Docs** (30s) - Interactive documentation
9. **Conclusion** (30s) - Final dashboard tour

---

## **📁 Output Files**

Your video will be saved as:
- **SimpleScreenRecorder**: `~/Videos/AIDA_Demo.mp4`
- **FFmpeg**: `./AIDA_Demo.mp4` (current directory)

---

## **🚀 Ready to Record!**

### **Final Check:**
```bash
echo "🎬 AIDA Video Recording Ready!"
echo "================================"
echo "✅ Frontend: http://localhost:3000"
echo "✅ Backend: http://localhost:8000" 
echo "✅ API Docs: http://localhost:8000/docs"
echo "✅ Screen Recorder: Installed"
echo "✅ Demo Script: VIDEO_DEMO_SCRIPT.md"
echo "✅ Demo Commands: ./demo_commands.sh"
echo ""
echo "🎥 Start recording and create your AIDA demo!"
```

---

**🎬 Action!** You're all set to create a professional AIDA demo video showcasing all the amazing AI-powered DAO management features!