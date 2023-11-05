import scrapy
import pandas as pd

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    start_urls = [
        "https://store.playstation.com/en-id/category/05a2d027-cedc-4ac0-abeb-8fc26fec7180/"
    ]

    def parse(self, response):
        games = response.css('div.psw-product-tile.psw-interactive-root')

        data = []

        for game in games:
            judul = game.css('span.psw-t-body.psw-c-t-1.psw-t-truncate-2::text').extract_first()
            harga = game.css('div.psw-fill-x.psw-price.psw-l-inline.psw-l-line-left-top > div > span::text').extract_first()

            if judul and harga:
                harga_bersih = harga.replace("Rp", "").replace("\xa0", "").strip()
                data.append({
                    "Judul": judul,
                    "Harga": "Rp " + harga_bersih
                })

        # Menyimpan data dalam file CSV
        df = pd.DataFrame(data)
        df.to_csv("output.csv", index=False)

        print(df)
