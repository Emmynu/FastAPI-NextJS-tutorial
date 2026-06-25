import { api } from "@/app/libs/api-client";


export function usePosts() {
    return {
        async createPost(data) {
            const response = await api.post("/posts", data)
            return (response);            
        },

        async getPost(userId){
            const response =  await api.get(`/posts/${userId}`)

            return response
        },
        async getSinglePost(id, userId){
            const resp = await api.get(`/posts/${userId}/${id}`)
            
            return resp
        },
        async deletePost(postId, userId){
            const resp = await api.delete(`/posts/${userId}/${postId}`)
            return resp
        }
    }
}