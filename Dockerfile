# Используем образ Ubuntu 22.04
FROM ubuntu:22.04

# Устанавливаем переменные окружения для автоматизации
ENV DEBIAN_FRONTEND=noninteractive

# Открываем порт 4444 для Selenium
EXPOSE 4444

# Устанавливаем необходимые зависимости
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg2 \
    software-properties-common \
    unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN add-apt-repository ppa:saiarcot895/chromium-dev -y
RUN apt install chromium-browser -y

RUN add-apt-repository ppa:deadsnakes/ppa && apt-get update

# Устанавливаем Python 3.12 и pip
RUN apt-get update && apt-get install -y \
    python3.12 \
    python3.12-venv \
    python3.12-distutils \
    python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Selenium
RUN pip3 install selenium

# Создаем виртуальное окружение
RUN python3.12 -m venv /src/venv

# Устанавливаем pip в виртуальном окружении
RUN /src/venv/bin/python -m pip install --upgrade pip

# Устанавливаем рабочую директорию
WORKDIR /src

# Копируем исходный код и requirements.txt
COPY src/ /src
COPY requirements.txt /src/

# Устанавливаем зависимости в виртуальном окружении
RUN /src/venv/bin/python -m pip install -r requirements.txt

# Команда по умолчанию
CMD ["/src/venv/bin/python", "bot.py"]
