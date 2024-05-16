from django.db import models

# Create your models here.
class Organization(models.Model):
    full_name = models.CharField('Полное наименование', max_length=250)
    short_name = models.CharField('Краткое наименование', max_length=250)
    inn = models.IntegerField('ИНН')
    kpp = models.IntegerField('КПП')
    ur_adres = models.TextField('Юридический адрес')
    management_full_name = models.CharField('Управляющее лицо', max_length=250)
    management_post = models.CharField('Должность управляющего лица', max_length=250)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Юридическое лицо"
        verbose_name_plural = "Юридические лица"

class Service_type(models.Model):
    service_type = models.CharField('Название направления оказываемых услуг', max_length=250)
    regular = models.BooleanField('Регулярная услуга, нужно выставлять ежемесячный счет')

    def __str__(self):
        return self.service_type

    class Meta:
        verbose_name = "Направление услуги"
        verbose_name_plural = "Направления услуг"

class Dogovor(models.Model):
    nomer_dogovora = models.CharField('Номер договора', max_length=250)
    date_of_signing = models.DateField('Дата начала действия договора')
    web_site = models.CharField('Веб сайт', max_length=250)
    contract_completed = models.BooleanField('Договор завершен')
    service_type = models.ForeignKey(Service_type, on_delete=models.DO_NOTHING)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        Field_in_django = (f'{self.nomer_dogovora} от {self.date_of_signing} - {self.organization}')
        return Field_in_django

    # def get_absolute_url(self):
    #     from django.urls import reverse
    #
    #     return reverse("dogovor-detail", kwargs={"pk": self.id})

    class Meta:
        verbose_name = "Договор"
        verbose_name_plural = "Договоры"


class Service(models.Model):
    service_name = models.CharField('Название оказываемой услуги', max_length=250)
    date_start = models.DateField('Дата начала оказания услуги')
    date_end = models.DateField('Дата окончания оказания услуги')
    price = models.IntegerField('Оплата за услугу')
    payment_made = models.IntegerField('Сумма частичной оплаты счета', db_default=0)
    dogovor = models.ForeignKey(Dogovor, on_delete=models.CASCADE)
    full_payment = models.BooleanField('Счет полностью оплачен')
    act_approved = models.BooleanField("Акт подписан")

    def __str__(self):
        return (f'{self.service_name} | {self.dogovor} | {self.dogovor.organization}')

    class Meta:
        verbose_name = "Услуга (локализованный этап)"
        verbose_name_plural = "Услуги (локализованные этапы)"



