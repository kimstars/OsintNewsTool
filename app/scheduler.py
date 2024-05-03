from app.admin.model_detect.crawlData import crawl_rss
from app.base.models import RssPaper
from apscheduler.schedulers.background import BackgroundScheduler


def job_function():


    all_rss = RssPaper.query.all()  
    import time
    for item in all_rss:
        try:
            print(f'Bắt đầu cập nhật từ RSS: {item.url}')
            cate_id = item.category.id
            listNews = crawl_rss(item.url, cate_id)
            time.sleep(300) # nghỉ 5 phút
            print(f'Cập nhật thành công RSS_URL: {item.url} => số lượng {len(listNews)}')
            
        except Exception as e:
            print(f'Error synchronizing URL {item.url}: {str(e)}')




scheduler = BackgroundScheduler()
scheduler.add_job(job_function, 'interval', seconds=3)
scheduler.start()