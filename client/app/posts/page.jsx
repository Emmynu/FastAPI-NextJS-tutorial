"use client"
import { showToast } from "../libs/toast"
import { usePosts } from "./api/posts"
import Link from "next/link"
import PostButton from "../libs/button"
import { useAuth } from "../auth/api/auth"
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { useEffect } from "react"

export default  function Posts() {
    const { createPost, getPost } =  usePosts()
    const { isLoading, signOut, getCurrentUser } = useAuth()
    const queryClient = useQueryClient()

    const { data, isLoading:isFetching} = useQuery({
        queryKey: ["Get Posts"],
        queryFn: async ()=>{
            const uid = localStorage.getItem("user") || (await getCurrentUser()).data?.uid
            return {
                posts: await getPost(uid),
                uid,
            }
        },
        staleTime: 0,
        retry: 0
    })
    

    useEffect(()=>{
        if (data?.posts?.error) {
        showToast({ type: "error", title: "Failed to fetch posts", msg:data?.error})
    }
    },[data?.posts?.error])

    
    const mutation = useMutation({
        mutationFn:async(data)=>{
            const resp = await createPost(data)
             if (resp?.status === 201) {
                showToast({type: "success", title: "Post created succesfully!",msg:null})
            }else{
                showToast({type: "error", title: "Failed to create post", msg: resp?.error})
            }
            
            return resp
        },
        onSuccess:()=>{
            queryClient.invalidateQueries({queryKey:["Get Posts"]})
        }
    })

    async function handleCreatePost(e) {
        e.preventDefault()
        const { post } =  Object.fromEntries(new FormData(e.currentTarget))
        
        if(post.length > 1){

            const data = {
            title: post,
            body: post}

            mutation.mutate(data)
            e.currentTarget.reset()
        }
        else{
            showToast({type: "error", title: "Invalid input", msg: "Please provide a valid input"})
        }
       
        
        
    }

    async function handleLogout() {
        await signOut()
        window.location = "/auth/login"
    }

    
    return (
        <main className="max-w-4xl m-8">
            <section >
                <form onSubmit={handleCreatePost}  className="flex items-center">
                    <input type="text" name="post" id="post" className="border-2 border-white"/>
                    <button type="submit" className="btn btn-warning" disabled={mutation.isPending}>{mutation.isPending ? <h2><span className="loading loading-spinner mr-1"></span>Loading</h2>: "Create Post"}</button>
                </form>
                    <button  className="btn btn-md bg-red-700 ml-1" onClick={handleLogout} disabled={isLoading}>
                        {isLoading ? <h2><span className="loading loading-spinner mr-1"></span>Loading</h2>: "Logout"}
                    </button>
            </section>
            <section className="my-10">
                {data?.posts?.error ? <>
                    <h2>No Book Found</h2>
                </>
                
            : 
            isFetching ? <h2>Loading...</h2> : data?.posts?.data.map(post =>{
                    return (
                       <article  key={post?.uid} className="my-5">
                        <Link href={`/posts/${post?.uid}`}>
                            <div className="mb-2">
                                <h2 className="text-xl mb-0.5">{post?.title}</h2>
                                <p className="text-xs font-thin text-warning">{post?.body}</p>
                            </div>
                        </Link>
                        <PostButton postId={post?.uid} userId={data?.uid}/>
                       </article>
            )})
            }
            </section>
        </main>
    )
}