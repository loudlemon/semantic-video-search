<template>
  <div style="max-width: 400px; margin: 50px auto; font-family: sans-serif; border: 1px solid #ccc; padding: 20px; border-radius: 8px;">
    <h2>Загрузка видео</h2>
    
    <!-- Поле выбора файла -->
    <input type="file" @change="onFileChange" accept="video/*" />
    
    <br><br>
    
    <!-- Кнопка -->
    <button 
      @click="uploadFile" 
      :disabled="!selectedFile" 
      style="width: 100%; padding: 10px; cursor: pointer;"
    >
      {{ loading ? 'Отправка...' : 'Загрузить видео' }}
    </button>

    <p v-if="status" style="margin-top: 15px; color: blue;">{{ status }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const selectedFile = ref(null)
const status = ref('')
const loading = ref(false)

// Функция, которая срабатывает при выборе файла
const onFileChange = (e) => {
  const files = e.target.files
  if (files.length > 0) {
    selectedFile.value = files[0]
    console.log("Файл выбран:", selectedFile.value.name)
  }
}

const uploadFile = async () => {
  console.log("Кнопка нажата, начинаем загрузку...")
  loading.value = true
  status.value = 'Загрузка пошла...'

  const formData = new FormData()
  formData.append('file', selectedFile.value) // Важно: 'file' должно совпадать с именем в FastAPI

  try {
    const response = await fetch('/api/upload', {
      method: 'POST',
      body: formData,
    })

    if (response.ok) {
      const result = await response.json()
      console.log("Ответ сервера:", result)
      status.value = `Успешно! ID: ${result.file_id}`
    } else {
      const errorText = await response.text()
      console.error("Ошибка сервера:", errorText)
      status.value = 'Сервер вернул ошибку: ' + response.status
    }
  } catch (error) {
    console.error("Сетевая ошибка:", error)
    status.value = 'Не удалось связаться с бэкендом.'
  } finally {
    loading.value = false
  }
}
</script>
