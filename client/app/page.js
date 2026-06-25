"use client"
import axios from "axios";
import { useState } from "react";



 export default function Page() {
  const [greet, setGreet] = useState(null)

  async function greetUser(e) {
    e.preventDefault()
    const { age } = Object.fromEntries(new FormData(e.currentTarget))
    try {
      const data = {
        user: "Deji",
        age: parseInt(age)
      }
        const rsp = await axios.post(`http://localhost:8000/onboarding`, data)         
         console.log(rsp.data?.name);
         
    } catch (error) {
      console.log(error?.message);
      
    }
    
  }

  return(
    <div >
      <form onSubmit={greetUser} className="border-2 border-white ">
        <input type="number" name="age" id="age"/>
      </form>
      <section>
        <h2 className="text-7xl text-white">{greet}</h2>
      </section>
    </div>
  )
}