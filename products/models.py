from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    title = models.CharField(max_length=255)
    pub_date = models.DateTimeField()
    body = models.TextField(default="")
    url = models.TextField(default="")
    image = models.ImageField(upload_to='images/')
    icon = models.ImageField(upload_to='images/')
    votes_total = models.IntegerField(default=1)
    hunter = models.ForeignKey(User, on_delete=models.CASCADE)

    @staticmethod
    def get_index_of_last_space(text):
        index = 0
        pom = 0

        for i in text:
            if i.isspace():
                index = pom
            pom += 1
        return index

    # in this function return summary
    # for "fancy" look last chars at the and are "..."
    def summary(self):
        text_summary = self.body[:100]
        index = self.get_index_of_last_space(text_summary)

        if index > 98:
            string = text_summary[0:index - 1]
            index = self.get_index_of_last_space(string)
            text_summary = string[0:index]
            string = text_summary + "..."

        else:
            string = text_summary[0:index]
            string += "..."

        return string

    # customize date and time
    def pub_date_pretty(self):
        return self.pub_type.strftime('%B %e %Y, %H:%M')

    def votes_total(self):
        votes = 0
        for upvote in Upvote.objects.all():
            if upvote.product == self:
                votes += 1
        return votes


class Upvote(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    voter = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField()
    comment_body = models.TextField(default="")

