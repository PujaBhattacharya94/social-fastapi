from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schemas, oauth
from ..database import get_db



router = APIRouter(prefix="/posts", tags=['Posts'])

my_posts = [{"title" : "title for post 1", "content":"content for post 1","id" : 1},{"title" : "Favourite Foods","content" : "i love biriyani", "id" : 2}]


# @router.get("/", response_model = List[schemas.PostResponse])
@router.get("/", response_model = List[schemas.PostResponseVote])
def post_data(db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)
              ,limit : int = 15, skip : int = 0, search : Optional[str] = ""):

    #limit parameter is used to set the number of post you want to see
    print(limit)

    #user can only retrive post which has his id
    # print(current_user.id)
    # sqlalchemy_post = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    # print(sqlalchemy_post)

    #limit parameter is used to set the number of post you want to see
    # sqlalchemy_post = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # return{"data":sqlalchemy_post}
    # print(search)

    sqlalchemy_vote = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,
                                                  models.Vote.post_id==models.Post.id,
                                                  isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    sqlalchemy_vote = list ( map (lambda x : x._mapping, sqlalchemy_vote) )
    
    return sqlalchemy_vote
    # return sqlalchemy_post
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # print(posts)
    #return{"data":my_posts}
    # return {"data": posts}


@router.get("/")
def root():
    return {"message": "Hello API World!!"}

#testing sqlachemy connectivity
# @xyz.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     sqlalchemy_post = db.query(models.Post).all()
#     return{"data":sqlalchemy_post}
    #prints the ql query that is used
    # sqlalchemy_post = db.query(models.Post)
    # print(sqlalchemy_post)
    


@router.post("/", status_code = status.HTTP_201_CREATED, response_model= schemas.PostResponse)
def create_post(new_publish_post : schemas.PostCreate,
                db: Session = Depends(get_db), 
                current_user: int = Depends(oauth.get_current_user)):
    
    # new_publish_post_dict = new_publish_post.dict()
    # new_publish_post_dict['id'] = randrange(0,10000)
    # my_posts.append(new_publish_post_dict)

    # cursor.execute("""INSERT INTO posts (title, content,published) VALUES(%s, %s,%s) RETURNING * """,
    #                (new_publish_post.title, new_publish_post.content, new_publish_post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # return{"data" : new_post}

    # sqlalchemy_create_post = models.Post(title = new_publish_post.title, 
                                        #  content = new_publish_post.content, 
                                        #  published = new_publish_post.published)

    #In case of too many columns you should not write all columns instead  convert new_publish_post into dictationary
    print(current_user.email)
    print(current_user.id)
    sqlalchemy_create_post = models.Post(owner_id = current_user.id ,**new_publish_post.dict())
    db.add(sqlalchemy_create_post)
    db.commit()
    db.refresh(sqlalchemy_create_post)
    # return{"data" : sqlalchemy_create_post}
    return sqlalchemy_create_post
    

#title str, content str, bool published/draft

# @xyz.get("/posts/{id}")
# def get_post(id):
#     print(id)
#     return{"post_detail" : f"This is the post - {id}"}

@router.get("/{id}", response_model = schemas.PostResponseVote)
def get_post(id : int, db: Session = Depends(get_db),current_user: int = Depends(oauth.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """,(id,))
    # db_post = cursor.fetchone()  
    # print(db_post)
    # if not db_post:
    #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
    #                         detail = f"post with id :{id} was not found")

    # sqlalchemy_one_post = db.query(models.Post).filter(models.Post.id == id).first()
    # print(sqlalchemy_one_post)

    sqlalchemy_one_post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,
                                                  models.Vote.post_id==models.Post.id,
                                                  isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not sqlalchemy_one_post:
         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                             detail = f"post with id :{id} was not found")
    
    #code to check that retrieve only his/her post
    # if sqlalchemy_one_post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                          detail="No authorized to perform requested action")

    # def get_post(id : int, response : Response):
        # single_post = find_post(id)
        # print(single_post)
        # if not single_post:
        #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
        #                         detail = f"post with id :{id} was not found")
        #     response.status_code = status.HTTP_404_NOT_FOUND
        #     return{'message' : f"post with id :{id} was not found"}
    # return{"post_detail" : sqlalchemy_one_post}
    return sqlalchemy_one_post


@router.get("/posts/latest")
def get_latest_post():
    latest_post = my_posts[len(my_posts)-1]
    print(latest_post)
    return latest_post

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),current_user: int = Depends(oauth.get_current_user)):
    sqlalchemy_delete_post_query = db.query(models.Post).filter(models.Post.id == id)
    sqlalchemy_delete_post = sqlalchemy_delete_post_query.first()

    if sqlalchemy_delete_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id :{id} does not exist")
    
    #code to check that user deletes only his/her post
    if sqlalchemy_delete_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                             detail="No authorized to perform requested action")
    

    sqlalchemy_delete_post_query.delete(synchronize_session = False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)

    # cursor.execute("""DELETE FROM posts WHERE id = %s returning * """,(id,))
    # delete_post = cursor.fetchone()
    # conn.commit()
    # print(delete_post)
    # if not delete_post:
    #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
    #     detail = f"post with id :{id} was not found")
    # return Response(status_code = status.HTTP_204_NO_CONTENT)

    #find the index in the array that has required ID
    # index = find_post_index(id)
    # if  index == None:
    #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
    #                         detail = f"post with id :{id} was not found")
    # my_posts.pop(index)
    #return{"message" : f"the post with {id} is successfully deleted."}
    # return Response(status_code = status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model = schemas.PostResponse)
def update_post(id:int, update_publish_post : schemas.PostCreate,db: Session = Depends(get_db)
                ,current_user: int = Depends(oauth.get_current_user)):
    sqlalchemy_update_post = db.query(models.Post).filter(models.Post.id == id)
    sqlalchemy_update = sqlalchemy_update_post.first()
    if sqlalchemy_update == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id :{id} was not found")
    # sqlalchemy_update_post.update({'title':'this is my updated title',
    #                                'content':'this is my updated content'},
    #                                synchronize_session=False)

    #code to check that user update only his/her post
    if sqlalchemy_update.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                             detail="No authorized to perform requested action")

    sqlalchemy_update_post.update(update_publish_post.dict(),synchronize_session = False)
    db.commit()
    # return {'data' : sqlalchemy_update_post.first()}
    return sqlalchemy_update_post.first()

    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """
    # ,(update_publish_post.title, update_publish_post.content,update_publish_post.published,(str(id,))))
    # update_db_post = cursor.fetchone()
    # conn.commit()
    # if update_db_post == None:
    #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
    #     detail = f"post with id :{id} was not found")
    # return{"message" : update_db_post}


    # index = find_post_index(id)
    # if index == None:
    #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
    #                         detail = f"post with id :{id} was not found")
    # update_publish_post_dict = update_publish_post.dict()
    # update_publish_post_dict['id'] = id
    # my_posts[index] = update_publish_post_dict
    # print(update_publish_post_dict)
    # return{"message" : update_publish_post_dict}