# Инструкция по развертыванию сайта "Визитка"

Этот репозиторий содержит исходный код сайта "Визитка". Ниже приведены инструкции по развертыванию сайта на локальном компьютере.

## Развертывание

1. **Клонирование репозитория:**
   Сначала склонируйте репозиторий с помощью команды `git clone`:
   ```bash
   git clone https://github.com/Eprotsky/postcard
2. **Переход в директорию с проектом:**
    Перейдите в директорию с загруженным проектом:
    ```bash
    cd postcard
3. **Настройка контейнера Docker**
    Настройте контейнер Docker с вашим приложением. 
    ```bash
   docker build -t postcard .
4. **Запуск контейнера Docker:**
    Запустите контейнер Docker с вашим приложением:
    ```bash
    docker run -p 5000:5000 -v "$(pwd)"/feedback.json:/app/feedback.json postcard
5. **Доступ к приложению:**
    После успешного запуска контейнера вы сможете получить доступ к вашему приложению, перейдя по адресу http://localhost:5000 в вашем веб-браузере.
