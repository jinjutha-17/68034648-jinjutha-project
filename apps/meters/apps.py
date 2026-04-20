from django.apps import AppConfig

class MetersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.meters'  # <--- ต้องมี apps. นำหน้า
    label = 'meters'      # <--- เพิ่มบรรทัดนี้เข้าไปครับ เพื่อให้มันรู้จักในชื่อสั้นๆ