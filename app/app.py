from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from app.schemas import (
    UserRead,
    UserCreate,
    UserUpdate,
    PostCreate,
    PostResponse,
    UploadResponse,
    FeedPostResponse,
    FeedResponse,
    DeleteResponse,
)
from app.db import Post, create_db_and_tables, get_async_session, User
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select
from app.images import imagekit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions # type: ignore
import shutil
import os
import uuid
import tempfile
from app.users import auth_backend, current_active_user, fastapi_users
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", os.getenv("PUBLIC_FRONTEND_URL", "http://localhost:3000")], # Put your frontend URL here
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods (GET, POST, DELETE, etc.)
    allow_headers=["*"], # Allows all headers
)

app.include_router(fastapi_users.get_auth_router(auth_backend), prefix='/auth/jwt', tags=["auth"])
app.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_reset_password_router(), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_verify_router(UserRead), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_users_router(UserRead, UserUpdate), prefix="/users", tags=["users"])

@app.post("/upload", response_model=UploadResponse)
async def upload_file(
        file: UploadFile = File(...),
        caption: str = Form(""),
        user: User = Depends(current_active_user),
        session: AsyncSession = Depends(get_async_session)
):
    temp_file_path = None

    try:
        validated_caption = PostCreate(caption=caption).caption

        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file: # type: ignore
            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)

        upload_result = imagekit.upload_file( 
            file=open(temp_file_path, "rb"),
            file_name=file.filename,
            options=UploadFileRequestOptions(
                use_unique_file_name=True,
                tags=["backend-upload"]
            )
        )

        if upload_result.response_metadata.http_status_code == 200: 
            post = Post(
                user_id=user.id,
                caption=validated_caption,
                url=upload_result.url, 
                file_type="video" if (file.content_type or "").startswith("video/") else "image",
                file_name=upload_result.name
            )
            session.add(post)
            await session.commit()
            await session.refresh(post)
            return UploadResponse(post=PostResponse.model_validate(post))

        raise HTTPException(status_code=502, detail="File upload failed")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        await file.close()

@app.get("/feed", response_model=FeedResponse)
async def get_feed(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_active_user),
):
    posts_result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = posts_result.scalars().all()

    users_result = await session.execute(select(User))
    users = users_result.scalars().all()
    user_dict = {u.id: u.email for u in users}

    posts_data: list[FeedPostResponse] = []
    for post in posts:
        base_post = PostResponse.model_validate(post)
        posts_data.append(
            FeedPostResponse(
                **base_post.model_dump(),
                is_owner=base_post.user_id == user.id,
                email=user_dict.get(base_post.user_id, "Unknown")
            )
        )

    return FeedResponse(posts=posts_data)


@app.delete("/posts/{post_id}", response_model=DeleteResponse)
async def delete_post(
    post_id: uuid.UUID,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    result = await session.execute(select(Post).where(Post.id == post_id))
    post = result.scalars().first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    post_owner_id = PostResponse.model_validate(post).user_id
    if post_owner_id != user.id:
        raise HTTPException(status_code=403, detail="You don't have permission to delete this post")

    await session.delete(post)
    await session.commit()

    return DeleteResponse(success=True, message="Post deleted successfully")
