// APP.js
import React, { useState, useMemo } from 'react';
import './App.css';

const API_BASE = process.env.REACT_APP_API_BASE || 'http://localhost:8000';




function App() {
  const [lang, setLang] = useState('en');
  const [searchTerm, setSearchTerm] = useState('');
  const [status, setStatus] = useState('System initialized. Ready to load assets.');
  const [isSearching, setIsSearching] = useState(false);
  const [progress, setProgress] = useState(0);
  const videoInputRef = React.useRef(null);
  const etalonInputRef = React.useRef(null);

  // i18n dictionary
  const dict = useMemo(() => ({
    en: {
      title: 'Semantic Video Search Service',
      uploadVideo: 'Upload Video',
      uploadEtalon: 'Upload Etalon Image',
      placeholder: 'Enter semantic query here...',
      search: 'Search',
      processing: 'Processing...',
      statusLabel: 'Status',
      statusInit: 'System initialized. Ready to load assets.',
      uploading: (type, file) => `Uploading ${type} file: ${file}...`,
      uploadOk: (file) => `${file} uploaded successfully. Ready to search.`,
      uploadErr: (type) => `Error uploading ${type}: Check console.`,
      emptyQuery: 'Error: Search term cannot be empty.',
      executing: (q) => `Executing semantic search for: "${q}"...`,
      searchOk: 'Search complete. Found 12 relevant semantic matches.',
      searchErr: 'Search failed. Backend error.'
    },
    ru: {
      title: 'Сервис Семантического Поиска по Видео',
      uploadVideo: 'Загрузить Видео',
      uploadEtalon: 'Загрузить Эталонное Изображение',
      placeholder: 'Введите семантический запрос...',
      search: 'Искать',
      processing: 'Обработка...',
      statusLabel: 'Статус',
      statusInit: 'Система инициализирована. Готово к загрузке данных.',
      uploading: (type, file) => `Загрузка файла (${type}): ${file}...`,
      uploadOk: (file) => `${file} успешно загружен. Можно начинать поиск.`,
      uploadErr: (type) => `Ошибка загрузки (${type}): смотрите консоль.`,
      emptyQuery: 'Ошибка: строка поиска не может быть пустой.',
      executing: (q) => `Выполнение семантического поиска: "${q}"...`,
      searchOk: 'Поиск завершён. Найдено 12 релевантных совпадений.',
      searchErr: 'Сбой поиска. Ошибка бэкенда.'
    }
  }), []);

  const t = useMemo(() => dict[lang], [dict, lang]);

  const updateStatus = (message) => {
    setStatus(message);
    console.log(`STATUS UPDATE: ${message}`);
  };

  // --- Handlers ---

  const runWithProgress = async (label, fn) => {
    updateStatus(label);
    setProgress(10);
    const timer = setInterval(() => {
      setProgress((p) => (p < 90 ? p + 5 : p));
    }, 120);
    try {
      const res = await fn();
      setProgress(100);
      return res;
    } finally {
      clearInterval(timer);
      setTimeout(() => setProgress(0), 600);
    }
  };

  const handleFileUpload = async (type) => {
    const inputRef = type === 'video' ? videoInputRef : etalonInputRef;
    if (!inputRef.current || !inputRef.current.files || inputRef.current.files.length === 0) {
      updateStatus(t.uploadErr(type));
      return;
    }
    const file = inputRef.current.files[0];
    const formData = new FormData();
    const fieldName = type === 'video' ? 'video_file' : 'image_file';
    formData.append(fieldName, file);

    const endpoint = type === 'video' ? '/upload/video' : '/upload/etalon_image';
    await runWithProgress(t.uploading(type, file.name), async () => {
      const resp = await fetch(`${API_BASE}${endpoint}`, { method: 'POST', body: formData });
      if (!resp.ok) throw new Error('Upload failed');
      const data = await resp.json();
      
      // Use the message returned from the server instead of the client-side template
      updateStatus(data.message);
      return data;
    });
  };

  const handleSearch = async () => {
    if (!searchTerm.trim()) {
      updateStatus(t.emptyQuery);
      return;
    }
    
    setIsSearching(true);
    await runWithProgress(t.executing(searchTerm), async () => {
      const form = new FormData();
      form.append('query', searchTerm);
      const resp = await fetch(`${API_BASE}/search`, { method: 'POST', body: form });
      if (!resp.ok) throw new Error('Search failed');
      const data = await resp.json();
      if (data.status === 'success') updateStatus(t.searchOk); else updateStatus(t.searchErr);
      return data;
    });
    try {
      // no-op
    } finally {
      setIsSearching(false);
    }
  };

  return (
    <div className="app-container">
      <video
        className="bg-video"
        src="/test_video.mp4"
        autoPlay
        muted
        loop
        playsInline
      />
      <div className="lang-switcher">
        <button
          className={`lang-btn ${lang === 'en' ? 'active' : ''}`}
          onClick={() => setLang('en')}
          aria-label="Switch to English"
        >
          <span className="flag-emoji" role="img" aria-label="English">🇬🇧</span>
          EN
        </button>
        <button
          className={`lang-btn ${lang === 'ru' ? 'active' : ''}`}
          onClick={() => setLang('ru')}
          aria-label="Переключить на Русский"
        >
          <span className="flag-emoji" role="img" aria-label="Русский">🇷🇺</span>
          RU
        </button>
      </div>
      <div className="content-area">
        
        {/* 1. Title */}
        <h1 className="app-title">{t.title}</h1>

        {/* 2. Upload Controls (Above Search Bar) */}
        <div className="upload-controls">
          <input ref={videoInputRef} type="file" accept="video/*" style={{ display: 'none' }} onChange={() => handleFileUpload('video')} />
          <input ref={etalonInputRef} type="file" accept="image/*" style={{ display: 'none' }} onChange={() => handleFileUpload('etalon_image')} />
          <button 
            className="menu-button upload-button" 
            onClick={() => videoInputRef.current && videoInputRef.current.click()}
            disabled={isSearching}
          >
            {t.uploadVideo}
          </button>
          <button 
            className="menu-button upload-button" 
            onClick={() => etalonInputRef.current && etalonInputRef.current.click()}
            disabled={isSearching}
          >
            {t.uploadEtalon}
          </button>
        </div>

        {/* 3. Search Bar & Button */}
        <div className="search-area">
          <input
            type="text"
            className="search-input"
            placeholder={t.placeholder}
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            onKeyDown={(e) => {
                if (e.key === 'Enter' && !isSearching) {
                    handleSearch();
                }
            }}
            disabled={isSearching}
          />
          <button 
            className="menu-button"
            onClick={handleSearch}
            disabled={isSearching}
          >
            {isSearching ? t.processing : t.search}
          </button>
        </div>

        {/* 4. Status Bar */}
        <div className="status-bar">
          {t.statusLabel}: {status}
        </div>

        {progress > 0 && (
          <div className="progress-container">
            <div className="progress-bar" style={{ width: `${progress}%` }} />
          </div>
        )}

      </div>
    </div>
  );
}

export default App;
