import { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import { 
  Send, Upload, FileText, Bot, User, Zap, BrainCircuit, Sparkles, Plus, Paperclip, Library 
} from 'lucide-react';
import './App.css';

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [files, setFiles] = useState([]); 
  const [mode, setMode] = useState("quick"); 
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const handleFileSelect = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      handleUpload(e.target.files);
    }
  };

  const handleUpload = async (selectedFiles) => {
    const fileArray = Array.from(selectedFiles);
    setFiles(prev => [...prev, ...fileArray]);

    const formData = new FormData();
    fileArray.forEach(file => formData.append("files", file));

    setMessages(prev => [...prev, { 
      role: 'system', 
      content: `Uploading ${fileArray.length} file(s)...` 
    }]);

    try {
      const res = await axios.post(`${API_URL}/ingest`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      
      const successCount = res.data.report.filter(r => r.status === 'success').length;
      
      setMessages(prev => [
        ...prev.slice(0, -1), 
        { role: 'system', content: `✅ Added ${successCount} documents to Mindoc.` }
      ]);
    } catch (err) {
      console.error(err);
      setMessages(prev => [...prev, { role: 'system', content: "❌ Upload failed." }]);
    }
  };

  const openPdf = (sourcePath, pageIndex, contentText) => {
    const filename = sourcePath.split(/[/\\]/).pop();
    const pageNumber = (pageIndex || 0) + 1;
    const searchPhrase = contentText
      .replace(/\n/g, " ")
      .replace(/[^\w\s]/gi, '')
      .split(" ")
      .slice(0, 6)
      .join(" ");
    
    window.open(`${API_URL}/files/${filename}#page=${pageNumber}&search="${searchPhrase}"`, '_blank');
  };

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userText = input;
    setInput("");
    
    setMessages(prev => [...prev, { role: 'user', content: userText }]);
    setLoading(true);

    try {
      const res = await axios.get(`${API_URL}/query`, { 
        params: { q: userText, mode: mode } 
      });

      setMessages(prev => [...prev, { 
        role: 'ai', 
        content: res.data.answer,
        sources: res.data.results
      }]);

    } catch (err) {
      setMessages(prev => [...prev, { role: 'ai', content: "Mindoc is offline or unreachable." }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      
      {/* --- SIDEBAR --- */}
      <aside className="sidebar">
        {/* BRAND NAME: MINDOC */}
        <div className="brand">
          <Library size={28} color="#4c8bf5" />
          <span>Mindoc</span>
        </div>
        
        <input 
          id="file-upload" 
          type="file" 
          accept=".pdf,.ppt,.pptx" 
          multiple 
          hidden 
          onChange={handleFileSelect} 
        />

        {files.length === 0 ? (
          <div className="upload-zone" onClick={() => document.getElementById('file-upload').click()}>
            <Upload size={32} />
            <span style={{fontSize:'0.9rem'}}>Add Knowledge</span>
            <span style={{fontSize:'0.75rem', opacity:0.6}}>PDF, PPTX supported</span>
          </div>
        ) : (
          <div style={{display:'flex', flexDirection:'column', height:'100%'}}>
            <div className="file-list">
              {files.map((f, i) => (
                <div key={i} className="file-item">
                  <FileText size={16} color="#4c8bf5"/>
                  <span style={{flex:1, overflow:'hidden', textOverflow:'ellipsis', whiteSpace:'nowrap'}}>
                    {f.name}
                  </span>
                </div>
              ))}
            </div>
            
            <button 
              className="add-more-btn"
              onClick={() => document.getElementById('file-upload').click()}
            >
              <Plus size={18} /> Add Documents
            </button>
          </div>
        )}

        <div style={{marginTop: 'auto', paddingTop: '1rem', borderTop: '1px solid #2d2e30'}}>
           <p style={{fontSize: '0.75rem', color: '#666', textAlign:'center'}}>
             {loading ? 'Thinking...' : '● Mindoc Ready'}
           </p>
        </div>
      </aside>

      {/* --- CHAT MAIN --- */}
      <main className="chat-area">
        
        {messages.length === 0 ? (
          <div className="welcome-screen">
            <Sparkles size={48} color="#4c8bf5" style={{marginBottom:'1rem'}}/>
            <h1>Welcome to Mindoc</h1>
            <p>Your private, offline knowledge assistant.</p>
          </div>
        ) : (
          <div className="messages-wrapper">
            {messages.map((msg, idx) => (
              <div key={idx} className={`message-row ${msg.role}`}>
                
                {msg.role !== 'system' && (
                  <div className={`avatar ${msg.role}`}>
                    {msg.role === 'ai' ? <Sparkles size={18} /> : <User size={18} />}
                  </div>
                )}

                <div className="bubble">
                  {msg.role === 'system' ? (
                    <em style={{color: '#888', fontSize: '0.9rem'}}>{msg.content}</em>
                  ) : (
                    <>
                      <ReactMarkdown>{msg.content}</ReactMarkdown>
                      
                      {msg.sources && (
                        <div className="sources">
                          {msg.sources.map((src, i) => (
                            <div 
                              key={i} 
                              className="source-chip" 
                              onClick={() => openPdf(src.metadata.source, src.metadata.page, src.content)}
                              title={src.metadata.source}
                            >
                              <FileText size={12} />
                              Page {(src.metadata.page || 0) + 1}
                            </div>
                          ))}
                        </div>
                      )}
                    </>
                  )}
                </div>
              </div>
            ))}
            
            {loading && (
              <div className="message-row ai">
                <div className="avatar ai"><Sparkles size={18} /></div>
                <div className="typing">
                  <div className="dot"></div>
                  <div className="dot"></div>
                  <div className="dot"></div>
                </div>
              </div>
            )}
            <div ref={chatEndRef} />
          </div>
        )}

        {/* --- INPUT AREA --- */}
        <div className="input-wrapper">
          <div className="input-container">
  {/* Left Action: Upload */}
  <button 
    type="button" 
    className="icon-btn"
    onClick={() => document.getElementById('file-upload').click()}
    title="Upload File"
  >
    <Paperclip size={20} />
  </button>

  {/* Main Input */}
  <form style={{flex:1, display:'flex'}} onSubmit={handleSend}>
    <input 
      className="chat-input" 
      placeholder={`Ask Mindoc (${mode === 'quick' ? 'Fast' : 'Deep Research'})...`} 
      value={input}
      onChange={(e) => setInput(e.target.value)}
    />
  </form>

  {/* --- NEW SEGMENTED TOGGLE --- */}
  <div className="toggle-wrapper">
    <div 
      className={`toggle-option quick ${mode === 'quick' ? 'active' : ''}`}
      onClick={() => setMode('quick')}
      title="Fast response (2 documents)"
    >
      <Zap size={14} />
      <span>Quick</span>
    </div>
    
    <div 
      className={`toggle-option deep ${mode === 'deep' ? 'active' : ''}`}
      onClick={() => setMode('deep')}
      title="Comprehensive Map-Reduce summary (4 documents)"
    >
      <BrainCircuit size={14} />
      <span>Deep</span>
    </div>
  </div>

  {/* Send Button */}
  <button onClick={handleSend} className="send-btn">
    <Send size={18} />
  </button>
</div>
        </div>

      </main>
    </div>
  );
}


export default App;