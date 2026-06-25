"use client"
import { useQuery } from "@tanstack/react-query"
import Link from "next/link"
import { useParams, useRouter } from "next/navigation"
import { usePosts } from "../api/posts"
import { useAuth } from "@/app/auth/api/auth"


export default function Post() {
    const { uid: postId  } = useParams()
    console.log(postId);
    
    const  { getSinglePost } =  usePosts()
    const { getCurrentUser } =  useAuth()

    const { data:post, isLoading } = useQuery({
        queryKey: ["Get Single Post"],
        queryFn:async () => {
            const uid = localStorage.getItem("user") || (await getCurrentUser()).data?.uid
            return (await getSinglePost(postId, uid))
        },
        staleTime: 0,
        retry: 0
    })
    
    if (isLoading) {
        return <h2>Loading.....</h2>
    }

    console.log(post);
    

    return (
    
        <div className="mx-5 my-10">
           {post?.error ? <>
            <h2 className="text-error text-xl font-semibold">{post?.error}</h2>
           </> :<>
                <h2 className="text-xl ">{post?.data?.title}</h2>
                <h3 className="text-sm my-1 text-warning italic">{post?.data?.body}</h3>

                <footer>
                    <p className="text-xs mt-1 mb-2">Created By: {post?.data?.userId}</p>
                    

                    <section>
                        <h2>Reviews</h2>
                        {post?.data?.reviews?.map(r=>{
                            return (
                                <h3 key={r.uid}>{r?.title}</h3>
                            )
                        })}
                    </section>

                    <button className="btn btn-warning font-extrabold mr-1"><Link href={"/posts"}>Back</Link></button>
                    <button className="btn btn-error  font-extrabold ml-1">Delete</button>
                </footer>
           </>}
        </div>
    )
}