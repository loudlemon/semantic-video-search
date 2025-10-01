// APP.js
import React, { useState, useMemo } from 'react';
import './App.css';

// --- Utility for simulating API calls ---
const simulateApiCall = (endpoint, data) => {
  console.log(`[API SIM] Request to /${endpoint} with data:`, data);
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({ success: true, message: `Operation successful on ${endpoint}` });
    }, 1500); // Simulate network latency
  });
};


function App() {
  const [lang, setLang] = useState('en');
  const [searchTerm, setSearchTerm] = useState('');
  const [status, setStatus] = useState('System initialized. Ready to load assets.');
  const [isSearching, setIsSearching] = useState(false);

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

  const handleFileUpload = async (type) => {
    const fileName = type === 'video' ? 'TestVideo.mp4' : 'EtalonImage.jpg';
    updateStatus(t.uploading(type, fileName));
    
    try {
      const result = await simulateApiCall('upload', { file_name: fileName, type });
      if (result.success) {
        updateStatus(t.uploadOk(fileName));
      }
    } catch (error) {
      updateStatus(t.uploadErr(type));
      console.error(error);
    }
  };

  const handleSearch = async () => {
    if (!searchTerm.trim()) {
      updateStatus(t.emptyQuery);
      return;
    }
    
    setIsSearching(true);
    updateStatus(`Executing semantic search for: "${searchTerm}"...`);

    try {
      const result = await simulateApiCall('search', { query: searchTerm });
      if (result.success) {
        updateStatus(t.searchOk);
      }
    } catch (error) {
      updateStatus(t.searchErr);
      console.error(error);
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
          <button 
            className="menu-button upload-button" 
            onClick={() => handleFileUpload('video')}
            disabled={isSearching}
          >
            {t.uploadVideo}
          </button>
          <button 
            className="menu-button upload-button" 
            onClick={() => handleFileUpload('etalon_image')}
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

      </div>
    </div>
  );
}

export default App;
