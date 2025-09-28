from fastapi import APIRouter , Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from fastapi_jwt_auth import AuthJWT
from models.models import Blog
from uuid import UUID
from schemas.schema import BlogCreateSchema , BlogCreateSchemaResponse,MyBlogCreateSchema

Blog_router = APIRouter(
    prefix="/api/v1",
    tags=["Blog"]
)



@Blog_router.post("/create-blog", response_model=BlogCreateSchemaResponse , status_code=status.HTTP_201_CREATED)
def Create_blog(data:BlogCreateSchema ,db:Session =Depends(get_db), Authorize:AuthJWT=Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()

    new_blog = Blog(title= data.title , body=data.body ,owner_id=current_user)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog
    




@Blog_router.get("/get_all_blogs" ,response_model=list[BlogCreateSchemaResponse], status_code=status.HTTP_200_OK)
def Get_all_blogs(db:Session=Depends(get_db)):
    all_blogs =db.query(Blog).all()
    return all_blogs





@Blog_router.get("/get_my_blogs" , response_model=list[MyBlogCreateSchema] , status_code=status.HTTP_200_OK)
def Get_my_blogs(  db:Session=Depends(get_db) , Authorize:AuthJWT=Depends()):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    my_blogs = db.query(Blog).filter(Blog.owner_id == current_user_id).all()
    return my_blogs



@Blog_router.get("/get_one_blog/{id}" , response_model=BlogCreateSchemaResponse , status_code=status.HTTP_200_OK)
def Get_one_blog(id:UUID ,db:Session=Depends(get_db) ):
    blog= db.get(Blog, id)
    if not blog:
        raise HTTPException(status_code=401 , detail="no blog found with this id")
    return blog



@Blog_router.put("/update_blog/{id}")
def Update_blog(id:UUID , data:BlogCreateSchema, db:Session=Depends(get_db) , Authorize:AuthJWT=Depends()):
    Authorize.jwt_required()
    current_user_id =  UUID(Authorize.get_jwt_subject())


    blog = db.query(Blog).filter(Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404 , detail=f"blog not found with the id of {id}")
    is_my_blog = blog.owner_id == current_user_id
    if not is_my_blog:
        raise HTTPException(status_code=401 , detail="you can only update your Blog. ")
    blog.title=data.title
    blog.body=data.body
    db.commit()
    return {
        "data":{
            "title":f"{data.title}", "body":f"{data.body}"
        }
    }

@Blog_router.delete("/delete_blog/{id}")
def Delete_blog(id:UUID ,db:Session=Depends(get_db), Authorize:AuthJWT=Depends()):
    Authorize.jwt_required()

    current_user_id = UUID(Authorize.get_jwt_subject())

    to_be_deleted_blog = db.get(Blog , id)
    if not to_be_deleted_blog:
        raise HTTPException(status_code=404 , detail=f"blog not found with the id of {id}")


    if not current_user_id == to_be_deleted_blog.owner_id:
         raise HTTPException(status_code=401 , detail=f"you can only delete your blog")
    db.delete(to_be_deleted_blog) 
    return {"blog succesfully deleted"}





