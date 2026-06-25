"use client"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { usePosts } from "../posts/api/posts"
import { showToast } from "./toast"

export default function PostButton({ postId, userId }) {
   const { deletePost } =  usePosts()
   const queryClient = useQueryClient()

    const mutation =  useMutation({
     mutationFn:async()=>{
          const result =  await deletePost(postId, userId)
          console.log(result);
          
          if (result?.status === 200) {
               showToast({type: "success", title: "Post deleted succesfully!",msg:null})
          }else{
               showToast({type: "error", title: "Failed to delete post", msg: result?.error})
          }
          return result
     },
     onSuccess:()=>{
          queryClient.invalidateQueries({queryKey:["Get Posts"]})
     }
    })
     
    async function handlDeletePost() {
          mutation.mutate()
    }

//      async function updatePost() {
//          const data = {
//                 title: "grace",
//                 body: "eos voluptas et aut odit natus earum\naspernatur fuga molestiae ullam\ndeserunt ratione qui eos\nqui nihil ratione nemo "
//          }
//        try {
//             const res = await axios.patch(PATH, data, { headers: {"Content-Type": "application/json"}, withCredentials:true}).then(router.refresh())
            
            
//        } catch (error) {
//             console.log(error?.response?.data?.detail);
            
//        }
//     }

    return (
       <>
         <button className="btn bg-amber-500 mr-1 text-black">Update</button>
         <button className="btn btn-error" onClick={handlDeletePost}>Delete</button>
       </>
    )
}