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
                    # Преобразование строк в соответствующие типы
                    try:
                        # Преобразуем дату из формата "12.12.2024_4173" в объект datetime
                        date_str = row[11].split('_')[0]  # Берем только "12.12.2024"
                        date = datetime.strptime(date_str, '%d.%m.%Y').date()

                        # Преобразуем created_on и updated_on в объекты datetime
                        created_on = datetime.strptime(row[12], '%Y-%m-%d %H:%M:%S.%f')
                        updated_on = datetime.strptime(row[13], '%Y-%m-%d %H:%M:%S.%f')

                        data = {
                            'exchange_product_id': row[1],
                            'exchange_product_name': row[2],
                            'oil_id': row[3],
                            'delivery_basis_id': row[4],
                            'delivery_basis_name': row[5],
                            'delivery_type_id': row[6],
                            'volume': int(row[8]),  # Преобразуем volume в целое число
                            'total': int(row[9]),  # Преобразуем total в целое число
                            'count': int(row[10]),  # Преобразуем count в целое число
                            'date': date,  # Используем преобразованную дату
                            'created_on': created_on,
                            'updated_on': updated_on,
                        }
                        SpimexTradingResults.objects.create(**data)
                    except ValueError as e:
                        self.stdout.write(self.style.ERROR(f'Error processing row {row}: {e}'))
                        continue
            self.stdout.write(self.style.SUCCESS('Data loaded successfully'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))