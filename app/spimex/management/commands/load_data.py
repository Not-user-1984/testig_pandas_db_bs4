import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from spimex.models import SpimexTradingResults

class Command(BaseCommand):
    help = 'Load data from CSV file into SpimexTradingResults model'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        try:
            with open(csv_file, newline='', encoding='utf-8') as csvfile:
                csvreader = csv.reader(csvfile)
                headers = next(csvreader)  # Skip the header row
                for row in csvreader:
                    try:
                        # Проверяем, что строка содержит данные для обработки
                        if not row[1] or not row[2] or not row[3]:
                            self.stdout.write(self.style.WARNING(f'Skipping row with missing data: {row}'))
                            continue

                        # Преобразуем дату из формата "12.12.2024_4173" в объект datetime
                        date_str = row[10].split('_')[0]  # Берем только "12.12.2024"
                        date = datetime.strptime(date_str, '%d.%m.%Y').date()

                        # Преобразуем числовые поля, обрабатываем пустые значения
                        volume = int(row[7]) if row[7] else 0  # Если пусто, используем 0
                        total = int(row[8]) if row[8] else 0  # Если пусто, используем 0
                        count = int(row[9]) if row[9] else 0  # Если пусто, используем 0

                        # Создаём объект модели
                        data = {
                            'exchange_product_id': row[1],
                            'exchange_product_name': row[2],
                            'oil_id': row[3],
                            'delivery_basis_id': row[4],
                            'delivery_basis_name': row[5],
                            'delivery_type_id': row[6],
                            'volume': volume,
                            'total': total,
                            'count': count,
                            'date': date,
                        }
                        SpimexTradingResults.objects.create(**data)
                    except ValueError as e:
                        self.stdout.write(self.style.ERROR(f'Error processing row {row}: {e}'))
                        continue
            self.stdout.write(self.style.SUCCESS('Data loaded successfully'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))