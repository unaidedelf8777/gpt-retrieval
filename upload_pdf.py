from upload import upload_from_pdf_url 
import arxiv
import json
import time

base_query = "cat:cs.AI AND submittedDate:[20210101 TO 20230513]"
max_results = 300000
start = 0
data_json = []

while True:
    try:
        query = f"{base_query}&start={start}&max_results={max_results}"
        search = arxiv.Search(query=query, max_results=max_results)
        

        results = list(search.results())
        if not results:
            break

        for result in results:
            form = {
                "entry": {
                    "title": result.title,
                    "published_date": result.published.isoformat(),
                    "pdf_url": result.pdf_url
                }
            }
            pdf_url = result.pdf_url
            upload_from_pdf_url(str(pdf_url))
            print(form)
            data_json.append(form)

        start += max_results

    except arxiv.arxiv.UnexpectedEmptyPageError as e:
        print(f"Unexpected empty page error: {e}")
        time.sleep(10)  # Wait 60 seconds before retrying
        break
