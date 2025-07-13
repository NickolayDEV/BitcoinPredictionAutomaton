FROM condaforge/mambaforge

WORKDIR /app

# Копируем YAML-файл окружения
COPY environment.yml .

# Создаём окружение через mamba
RUN mamba env create -f environment.yml && \
    mamba clean -afy && \
    rm -rf ~/.cache/pip

# Копируем весь проект
COPY . .

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED=1 \
    PATH=/opt/conda/envs/btc-env/bin:$PATH

# Запуск с активированным окружением
CMD ["bash", "-c", "conda run --no-capture-output -n btc-env python predict.py >> logs.txt 2>&1"]
