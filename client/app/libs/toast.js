"use client"

import { toast } from "sonner"
import "../globals.css"


export  function showToast({ type, title, msg}) {
    if (type === "success") {
        toast.success(title,{
             description: msg, 
             duration: 3000,
             style: {
                color: "green",
                borderLeft: "8px solid green",
             }
        })
    }
    
    else if(type === "warning"){
        toast.warning(title,{ description: msg, duration: 3000})
    }
    else if(type === "error"){
        toast.error(title, {
            description:msg,
            duration:4000,
            style:{
                
                color: "red",
                borderLeft: "8px solid red",
            }
        })
    }
} 