from django.db import models

class Report(models.Model):
    REPORT_TYPE_CHOICES = [
        ('focus', 'Foco de Dengue'),
        ('case', 'Caso de Dengue em Casa'),
    ]

    STATUS_CHOICES = [
        ('open', 'Aberto'),
        ('resolved', 'Resolvido'),
    ]

    report_type = models.CharField(
        max_length=10,
        choices=REPORT_TYPE_CHOICES,
        verbose_name="Tipo de Denúncia",
        default='focus'
    )
    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(verbose_name="Descrição")
    location = models.CharField(max_length=255, verbose_name="Localização", blank=True, null=True)
    latitude = models.FloatField(verbose_name="Latitude", blank=True, null=True)
    longitude = models.FloatField(verbose_name="Longitude", blank=True, null=True)
    image = models.ImageField(upload_to='reports/', blank=True, null=True, verbose_name="Imagem")
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='open',
        verbose_name="Status"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")

    def __str__(self):
        return self.title
