from iapp.crawler.twitter.tweepy_crawler import UserInfoCrawler


class TestTwitterCrawler:

    def test_user_info_crawl_sync(self):
        uic = UserInfoCrawler()
        user_info, params = uic.crawl(screen_name='JMA_kishou')
        print(user_info)
