from database.db import get_database
def search_local(term,limit=10):
    p="%"+term+"%"
    with get_database() as db:
        rows=db.execute("SELECT title,url,summary,score,source_type,query FROM research WHERE title LIKE ? OR snippet LIKE ? OR content LIKE ? OR summary LIKE ? ORDER BY score DESC,created_at DESC LIMIT ?",(p,p,p,p,limit)).fetchall()
    return [{"title":r[0],"url":r[1],"summary":r[2],"score":r[3],"source_type":r[4],"query":r[5]} for r in rows]
