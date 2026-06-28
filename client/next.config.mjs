/** @type {import('next').NextConfig} */
const nextConfig = {
  /* config options here */
  async rewrites(){
    return[
      {
        source:"/api/v1/:path*",
        destination:"https://postly-api-axyk.onrender.com/api/v1/:path*"
      }
    ]
  }
};

export default nextConfig;
